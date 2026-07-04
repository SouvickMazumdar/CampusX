from fastapi import FastAPI
from pydantic import BaseModel
import redis
import redis
import hashlib
import joblib
import json
import logging

app=FastAPI()
redis_clent=redis.Redis(host='localhost', port='6379')
logging.info("Redis connection is done")

model=joblib.load('iris_model.joblib')
logging.info("Model is loaded")

class Iris(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthhCm: float

    def to_list(self):
        return [
            self.SepalLengthCm,
            self.SepalWidthCm,
            self.PetalLengthCm,
            self.PetalWidthhCm
        ]
    def cache_key(self):
        raw=json.dumps(self.model_dump(), sort_keys=True)
        return f"Predict : {hashlib.sha256(raw.encode()).hexdigest()}"
    

@app.post('/predict')
async def predict(data: Iris):
    key=data.cache_key()
    cached_result=redis_clent.get(key)
    if cached_result:
        print("Serving prediction from Cache")
        return json.loads(cached_result)
    prediction=model.predict([data.to_list()])[0]
    result={'prediction ': int(prediction)}
    redis_clent.set(key,json.dumps(result), ex=3600)
    return result 
        

