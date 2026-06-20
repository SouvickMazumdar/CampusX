from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
app=FastAPI()


# this middle will add the response time in the response
class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time=time.time()
        response=await call_next(request)
        duration=time.time()-start_time
        print(f'Request: {request.url.path} processed in {duration:.5f} seconds' )
        return response


app.add_middleware(TimerMiddleware)
@app.get('/hello')
async def hello():
    for _ in range(10**7):
        pass
    return {'message':'Hello World!!'}