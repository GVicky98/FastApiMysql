import pymysql
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

# To run the code type the below command in terminal
# uvicorn fastApiMysql:app --reload
# FastApiMysql is the file name and app is the variable assigned to FastAPI()

app = FastAPI()

db = pymysql.connect(host = "localhost", user = "root", password = "vicky")
cursor = db.cursor()
cursor.execute("create database if not exists riverstone")
cursor.execute("use riverstone")
cmd1 = "create table if not exists inventory(item_id int primary key,item_category varchar(30),item_price bigint,item_brand varchar(30));"
cursor.execute(cmd1)
# cursor.execute("insert into inventory values (1,'Mobile',25000,'Nokia')")
db.commit()
# db.close()

class Item(BaseModel):
    category:str
    price:float
    brand:str | None = None

class Update_Item(BaseModel):
    category:str  | None = None   
    price:float  | None = None   
    brand:str | None = None   
    
class Inventory_Mysql:

    def __init__(self):     
        self.db = pymysql.connect(host = "localhost", user = "root", password = "vicky", db = "riverstone")
        self.cursor = self.db.cursor()
    
    def get_all_mysql(self):
        self.inv = self.cursor.execute("select * from inventory")
        self.inv = self.cursor.fetchall()
        self.db.commit()
        # self.db.close()
        inventory = {}
        for x in self.inv:
            # print(x[0],x[1],x[2],x[3])
            inventory[x[0]] = {"Category":x[1],
                               "Price":x[2],
                               "Brand":x[3]
                               }
        return inventory

    def add_item_sql(self, item_id, item:dict):
        # item = dict(item1)
        category = item.get("category")
        price = item.get("price")
        brand = item.get("brand")       
        cmd1 = f"""insert into inventory values(%s,%s,%s,%s)"""
        cmd2 = (item_id, category, price, brand)
        self.cursor.execute(cmd1, cmd2)
        data = self.cursor.execute(f"select * from inventory where item_id = {item_id}") 
        data = self.cursor.fetchall()
        self.db.commit()
        inventory = {}
        for x in data:
            inventory[item_id] = {"Category":x[1],
                               "Price":x[2],
                               "Brand":x[3]
                               }
        # self.db.close()
        return inventory
        
    def edit_item_sql(self, item_id, item:dict):
        if item['category'] != "string":
            cmd1 = f"update inventory set item_category = '%s' where item_id = {item_id}" % (item["category"])
            self.cursor.execute(cmd1)
            self.db.commit()
        
        if item["price"] != 0:
            cmd2 = f"update inventory set item_price = '%d' where item_id = {item_id}" % (item["price"])
            self.cursor.execute(cmd2)
            self.db.commit()
            
        if item["brand"] != "string":
            cmd2 = f"update inventory set item_brand = '%s' where item_id = {item_id}" % (item["brand"])
            self.cursor.execute(cmd2)
            self.db.commit()
            
        data = self.cursor.execute(f"select * from inventory where item_id = {item_id}") 
        data = self.cursor.fetchall()
        self.db.commit()
        inventory = {}
        for x in data:
            inventory[item_id] = {"Category":x[1],
                               "Price":x[2],
                               "Brand":x[3]
                               }
        # self.db.close()
        return inventory
    
    def delete_item_sql(self, item_id):
        cmd1 = f"delete from inventory where item_id = {item_id}"
        self.cursor.execute(cmd1)
        self.db.commit()

@app.get("/")
def homepage():
    return {"welcome":"FastAPI Task"}

@app.get("/items")
def get_all_items():
    items = Inventory_Mysql()
    return items.get_all_mysql()

@app.get("/items/{item_id}")
def get_item(item_id:int):
    items = Inventory_Mysql()
    inventory = items.get_all_mysql()
    if item_id in inventory:
            return inventory[item_id]
    else:
        raise HTTPException(status_code = 404, detail = "Item ID not found")

@app.post("/add-item/{item_id}")
def add_item(item_id:int, item:Item):
    items = Inventory_Mysql()
    inventory = items.get_all_mysql()
    if item_id in inventory:
        raise HTTPException(status_code = 400, detail = "Item ID already exists")
    # inventory[item_id] = item
    # print(type(item.dict()))
    ans = items.add_item_sql(item_id, item.dict())
    return ans

@app.put("/update_item/{item_id}")
def edit_item(item_id:int, item:Update_Item):
    items = Inventory_Mysql()
    inventory = items.get_all_mysql()
    if item_id not in inventory:
        raise HTTPException(status_code = 400, detail = "Item ID not found")

    ans = items.edit_item_sql(item_id, item.dict())
    return ans
    
@app.delete("/delete_item")
def delete_item(item_id:int = Query(..., description = "ID is mandatory", gt = 0)):
    items = Inventory_Mysql()
    inventory = items.get_all_mysql()
    if item_id not in inventory:
        raise HTTPException(status_code = 404, detail = "Item ID not found")
    items.delete_item_sql(item_id)
    return {item_id:"Delete success"}
