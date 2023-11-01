from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# connection via redis-om
redis = get_redis_connection(
    host = "redis-10965.c3.eu-west-1-2.ec2.cloud.redislabs.com",
    port =  10965,
    password = "H9g5gUyG1Fn8uwXIQbSyOMxoS5bHPgEp",
    decode_responses = True
)

class MainProduct(BaseModel):
    name: str
    price: float
    quantity: int

class Product(HashModel):
     name: str
     price: float
     quantity: int

     class Meta:
        database = redis

'''''
@app.get("/")
def index ():
    return {"messgae": "Hello World"}
    '''

@app.get("/products")
def get_products():
    return [format_product(pk) for pk in Product.all()]

def format_product(pk: str): #pk means primary keys
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }

@app.post('/products')
async def create_product(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get_product(pk: str):
    return Product.get(pk)

@app.put('/products/{pk}')
def update_product(pk: str, amount: int):
    product = Product.get(pk)
    product.quantity = product.quantity - amount
    return product.quantity