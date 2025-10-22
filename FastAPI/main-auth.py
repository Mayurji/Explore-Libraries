from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

# Libraries for FastAPI, Security, and Models
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext

# Libraries for JWT handling
from jose import JWTError, jwt

# --- 1. Configuration & Constants ---

# Security configuration
SECRET_KEY = "YOUR_SUPER_SECRET_KEY_GOES_HERE"  # Change this in a real application!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context (using bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme definition
# The tokenUrl specifies the endpoint where the client can get a token (login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- 2. Data Models (Pydantic) ---

class Token(BaseModel):
    """The shape of the response when a token is successfully issued."""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """The data we expect to find inside the JWT payload."""
    username: Union[str, None] = None

class User(BaseModel):
    """The public user profile model."""
    username: str
    full_name: Union[str, None] = None
    email: Union[str, None] = None

class UserInDB(User):
    """The user model including the hashed password (never exposed)."""
    hashed_password: str


# --- 3. Database & Utility Functions (In a real app, this would be DB calls) ---

# Fake Database for demonstration
# Note: The password 'securepassword123' is hashed using bcrypt
def get_password_hash(password):
    return pwd_context.hash(password)

# Hashed password for 'testuser' is the hash of 'securepassword123'
# Generated using: pwd_context.hash("securepassword123")
FAKE_HASHED_PASSWORD = get_password_hash("admin123")

fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": FAKE_HASHED_PASSWORD,
    }
}

def verify_password(plain_password, hashed_password):
    """Verifies a plain-text password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: dict, username: str) -> Union[UserInDB, None]:
    """Retrieves a user from the fake database."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db: dict, username: str, password: str) -> Union[UserInDB, bool]:
    """Authenticates a user by checking username and password."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# --- 4. JWT Token Generation and Decoding ---

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """Creates an encoded JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Add the expiration time to the payload
    to_encode.update({"exp": expire.timestamp()}) 
    
    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Dependency to decode and validate the JWT from the Authorization header.
    
    This function is run on every protected route.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the subject (username)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
    
    except JWTError:
        # Catch token errors (e.g., signature mismatch, expired token)
        raise credentials_exception
        
    # Look up the user in the database (Optional, but recommended for authorization checks)
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
        
    # Return the user object (excluding the password hash)
    return User(username=user.username, full_name=user.full_name, email=user.email)

# Dependency to check if the user is both authenticated and active (optional)
def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # In a real app, you might check if the user is disabled here
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# --- 5. FastAPI Application and Endpoints ---

app = FastAPI(
    title="FastAPI JWT Auth Demo",
    description="Demonstrates OAuth2 Password Flow with JWTs for secure access."
)

@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    # This dependency parses the username and password from form data
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint for user login. 
    It checks credentials and returns a JWT access token.
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Define the token expiration time
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create the token, using the username as the JWT subject ("sub")
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", tags=["Public"])
async def read_root():
    """A public, unprotected endpoint."""
    return {"message": "Welcome! Access /docs to try the authentication flow."}

@app.get("/users/me/", response_model=User, tags=["Users"])
async def read_users_me(
    # By using the dependency, this route is protected
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """A protected endpoint that returns the current authenticated user's details."""
    return current_user

@app.get("/protected-data/", tags=["Data"])
async def read_protected_data(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """A protected endpoint demonstrating access to sensitive information."""
    return {
        "data": f"Hello, {current_user.full_name}! You successfully accessed protected data.",
        "user_id": current_user.username
    }

# How to run the application:
# 1. Install dependencies: pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt]
# 2. Save the code as main.py
# 3. Run the server: uvicorn main:app --reload
# 4. Access http://127.0.0.1:8000/docs
