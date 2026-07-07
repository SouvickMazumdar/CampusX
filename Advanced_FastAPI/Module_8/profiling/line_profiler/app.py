import time
from fastapi import FastAPI

app=FastAPI()

def computation(n: int):
    res=sum((i*2) for i in range(n))
    time.sleep(2)
    return res

@profile
def process_data(x: int):
    return computation(x)

@app.get('/profiling')
def profiling(a: int):
    return {'result': process_data(a)}

