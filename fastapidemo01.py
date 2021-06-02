from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

# https://www.youtube.com/watch?v=-ykeT6kk4bk

app = FastAPI()
# Endpoint = '/item' etc
# GET, POST, PUT, DELETE

class Item(BaseModel):
	name: str
	price: float
	brand: Optional[str] = None

class UpdateItem(BaseModel):
	name: Optional[str] = None
	price: Optional[float] = None
	brand: Optional[str] = None

# inventory = {
# 	1: {
# 		"name": "Milk",
# 		"price": 3.99,
# 		"brand": "Regular"
# 	}
# }

inventory = {}

@app.get("/")
def home():
	return {"Data": "Test"}


@app.get("/about")
def about():
	return {"Data": "About"}

# Path 
@app.get("/get-item/{item_id}")
#def get_item(item_id: int):
def get_item(item_id: int = Path(None, description="The ID of the Item"),GT=0,LT=10):  #descripitions are added to api docs.
	return inventory[item_id]

# query parameter
@app.get("/get-by-name")  
#def get_by_name(name: str):
def get_by_name(item_id: int, name: str = None): # default to None, and optional.  /get-by-name?name=Milk&item_id=1
	for item_id in inventory:
		# if inventory[item_id]["name"] == name:
		if inventory[item_id].name == name:
			return inventory[item_id]
	raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Item name not found")

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):  #Item from request body, not from query parameter
	if item_id in inventory:
		raise HTTPException(status_code = 400, detail="Item id already exists")

	inventory[item_id] = item
	#inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
	return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):  #Item from request body, not from query parameter
	if item_id not in inventory:
		raise HTTPException(status_code = 404, detail="Item id does not exist")

	if item.name != None:
		inventory[item_id].name = item.name
	if item.price != None:
		inventory[item_id].price = item.price
	if item.brand != None:
		inventory[item_id].brand = item.brand

	return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id: int):  
	if item_id not in inventory:
		raise HTTPException(status_code = 404, detail="Item id does not exist")

	del inventory[item_id]
	return {"Success":"Item deleted"}
