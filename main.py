import os
import pandas as pd
from fastapi import FastAPI



BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DATA_DIR = os.path.join(BASE_DIR, 'data')

#dataset = os.path.join(DATA_DIR, 'plants-reduced.xlsx')


app = FastAPI()

class Plant(BaseModel):
    state: Optional[str] = None
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None 
    net_generation: Optional[float] = None


@app.get('/')
def read_root():
    return {"Hello": "World"}
