from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. The Pydantic Model (Schema)
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Initialize the app
app = FastAPI()

# 2. The In-Memory 'Database'
# Key: int (Item ID), Value: Item object (Pydantic)
items_db: dict[int, Item] = {}
next_id = 1 # Simple counter for new IDs

# C - CREATE
@app.post("/items/")
def create_item(item: Item):
    global next_id # Need to modify the global variable

    # 'Saving' the item to our in-memory DB
    items_db[next_id] = item

    # Optional: return the item along with its new ID
    new_item_id = next_id
    next_id += 1 # Increment ID for the next item

    return {"id": new_item_id, **item.model_dump()} 
    # model_dump() converts the Pydantic model to a dict

# R - READ ALL
@app.get("/items/")
def read_items() -> List[Item]:
    # Return all the values (the Item objects) from our dict
    return list(items_db.values())


# R - READ ONE (Path Parameter Example)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        # Best Practice: Return a 404 Not Found error
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")

    return items_db[item_id]

# U - UPDATE
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    # Overwrite the existing item with the new data
    items_db[item_id] = item
    return {"id": item_id, "message": "Item updated successfully", **item.model_dump()}


# D - DELETE
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id] # Python's way to delete a dictionary key

    # Best Practice: Return a 204 No Content status, but for simplicity, 
    # we'll return a 200 with a message.
    return {"message": f"Item with ID {item_id} deleted"}