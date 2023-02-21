from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# To run the code type the below command in terminal
# uvicorn fastApiTask:app --reload 
# FastApiTask is the file name and app is the variable assigned to FastAPI()
  
class Item(BaseModel):
    category:str
    price:float
    brand:str | None = None

class Update_Item(BaseModel):
    category:str  | None = None   
    price:float  | None = None   
    brand:str | None = None   
    
app = FastAPI()
inventory = {
    0:{
        "category":"mobile",
        "price":25000,
        "brand":"Redmi"
    }
}

@app.get("/")
def homepage():
    return {"welcome":"FastAPI Task"}

@app.get("/items")
def get_all_items():
    return inventory

@app.get("/items/{item_id}")
def get_item(item_id:int):
    if item_id in inventory:
            return inventory[item_id]
    else:
        raise HTTPException(status_code = 404, detail = "Item ID not found")

@app.post("/add-item/{item_id}")
def add_item(item_id:int, item:Item):
    if item_id in inventory:
        raise HTTPException(status_code = 400, detail = "Item ID already exists")
    inventory[item_id] = item
    return inventory[item_id]

@app.put("/update_item/{item_id}")
def edit_item(item_id:int, item:Update_Item):
    if item_id not in inventory:
        raise HTTPException(status_code = 400, detail = "Item ID not found")
    if item.category != None:
        inventory[item_id].category = item.category
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    
    return inventory[item_id]

@app.delete("/delete_item")
def delete_item(item_id:int = Query(..., description = "ID is mandatory", gt = 0)):
    if item_id not in inventory:
        raise HTTPException(status_code = 404, detail = "Item ID not found")
    del inventory[item_id]
    return {item_id:"Delete success" }
