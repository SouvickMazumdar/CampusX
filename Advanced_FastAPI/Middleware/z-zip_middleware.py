from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
app=FastAPI()
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)
# it minimizes the output zip it which saves the latency


