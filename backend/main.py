import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

class Fruit(BaseModel):
    name: str

class Fruits(BaseModel):
    fruits: List[Fruit]

app = FastAPI(debug=True)

origins = [
    "http://localhost:5173",]
# if running on local machine use the port that front end is running on
# DEFINE THE BASE ORIGIN WHEN DEPLOYING
# "https://yourdomain.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"fruits": [
    Fruit(name="Apple"),

]}

@app.get("/fruits", response_model=Fruits)
def get_fruits():
    return Fruits(fruits=memory_db["fruits"])

@app.post("/fruits")
def add_fruit(fruit: Fruit):
    memory_db["fruits"].append(fruit)
    return fruit

# @app.delete("/fruits/{name}")
# def delete_fruit(name: str):
#     global memory_db
#     memory_db["fruits"] = [fruit for fruit in memory_db["fruits"] if fruit.name != name]
#     return {"message": "Fruit {} deleted successfully".format(name)}
    # return {"message": f"Fruit {name} deleted successfully"}

# @app.delete("/fruits/{name}")
# def delete_fruit(name: str):
#     global memory_db
#     # Remove the fruit by name
#     fruit_to_delete = next((fruit for fruit in memory_db["fruits"] if fruit.name == name), None)
#     if fruit_to_delete:
#         memory_db["fruits"] = [fruit for fruit in memory_db["fruits"] if fruit.name != name]
#         return {"message": "Fruit {} deleted successfully".format(name)}
#     else:
#         return {"message": "Fruit {} not found".format(name)}

@app.delete("/fruits/{fruit_name}")
def delete_fruit(fruit_name: str):
    fruit_to_remove = next((fruit for fruit in memory_db["fruits"] if fruit.name == fruit_name), None)
    if fruit_to_remove:
        memory_db["fruits"].remove(fruit_to_remove)
        return {"message": f"Deleted {fruit_name}"}
    else:
        return {"message": "Fruit not found"}, 404

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)