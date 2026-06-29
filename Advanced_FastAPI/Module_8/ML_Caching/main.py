from fastapi import FastAPI
from pydantic import BaseModel
import redis
import redis
import hashlib
import joblib

app=FastAPI()
redis_clent=redis.Redis(host='localhost', port='6379')

