from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


class ModelName(str,Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name : str
    description : str | None = None
    price :float
    tax : float | None = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/items/{item_id}')
async def items(item_id : int , needy: str| None = None):
    return {"item_id": item_id,"needy": needy}


@app.post("/items/")
async def create_item(item:Item):
    return item

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}






