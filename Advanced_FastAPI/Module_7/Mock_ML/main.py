from fastapi import FastAPI
from pydantic import BaseModel
from model import model
import numpy as np



app=FastAPI()

class IrisFlower(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

@app.post('/predict')
def predict(data: IrisFlower):
    features=np.array([
        data.SepalLengthCm,
        data.SepalWidthCm,
        data.PetalLengthCm,
        data.PetalWidthCm
    ])
    # this reshape function will convert the 1D array into 2D array (1,-1) means 1 row and based upon the element it will decide the column, in this case it will 4(columns)
    # prediction=model.predict(features.reshape(1,-1))
    # below we are passing feature inside square bracket because model is expecting 2d array
    prediction=model.predict([features])
    print(prediction)
    res=int(prediction[0])

    return {'prediction': res}
