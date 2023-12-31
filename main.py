from enum import Enum
from typing import Annotated
from fastapi import FastAPI, Header, Path, Query ,Request
from pydantic import BaseModel, Field, HttpUrl


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None

    model_config = {
        "json_schema_extra": {"examples": [{"username": "Foo", "full_name": "Bar"}]}
    }


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def items(
    request: Request,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    user_agent: Annotated[str | None, Header()] = None,
    needy: str | None = None,
):
    client_host = request.client

    return {"item_id": item_id, "needy": needy , "user_agent": user_agent ,"client_host": client_host}


@app.post("/items/")
async def create_item(item: Item, user: User):
    return item, user


@app.post("/offers/" ,response_model=Offer)
async def create_offer(offer: Offer):
    return offer


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
