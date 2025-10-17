from fastapi import FastAPI

app =FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#--- request model ---

class ItemBase(BaseModel):
    name: str
    price: float
    description: str
    is_offer: bool | None = None

class ItemCreate(ItemBase):
    price: float = 0.01

@app.post('/items/')
def create_item(item: ItemCreate):
    return {'message': "Item Created", 'item': item}


#-------------Response Model -------------
class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool

class UserInPublic(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        from_attributes = True

def get_user_from_db(user_id: int) -> UserInDB:
    return UserInDB(id = user_id, username='SuperUser', hashed_password='xyz', email='z@a', is_active=True)

@app.get('/users/{user_id}', response_model=UserInDB)
def read_user(user_id: int):
    db_user = get_user_from_db(user_id=user_id)
    return db_user

