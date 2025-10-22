from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

#data model
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None

#app initi
app = FastAPI()

#in-memory db
items_db: dict[int, Item] = {}
next_id = 1

@app.post('/items/')
def create_item(item: Item):
    global next_id

    items_db[next_id] = item
    new_item_id = next_id
    next_id += 1

    return {'id': new_item_id, **item.model_dump()}

@app.get('/items/')
def read_items() -> List[Item]:
    return list(items_db.values())


@app.get('/items/{item_id}')
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f'Item with id {item_id} not found')
    
    return items_db[item_id]

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f'Item with id {item_id} not found')
    
    items_db[item_id] = item
    return {'id': item_id, "message": 'item object is updated', **item.model_dump()}

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f'Item with id {item_id} not found')

    del items_db[item_id]
    return {'id': item_id, 'message': f'Item with id {item_id} is removed'}