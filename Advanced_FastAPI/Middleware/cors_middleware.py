from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origin=[
        'https://my-frontend.com','http://localhost:3000'
    ],
    allow_methods=['GET','POST','PUT','DELETE'],
    allow_headers=['*']
)

# it channels or filter which addresses should be allowed or not\

