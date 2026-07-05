import httpx
import redis
import hashlib
import json
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
redis_client=redis.Redis(host='localhost', port=6379, db=0)

class PostRequest(BaseModel):
    post_id: int


def make_cache_key(post_id):
    raw=f"external_api:post_{post_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

@app.post('/get-post')
async def get_post(data: PostRequest):
    cache_key=make_cache_key(data.post_id)
    cached_data=redis_client.get(cache_key)
    if cached_data:
        print("Response getting from Cache...")
        return json.loads(cached_data)
    print('Calling external API...')
    # Below method is used to call an external api and store its response in json format inside redis
    async with httpx.AsyncClient() as client:
        response=await client.get(f"https://jsonplaceholder.typicode.com/posts/{data.post_id}")
        if response.status_code!=200:
            return {'error':'Post not found !!!'}
        post_data=response.json()
        redis_client.setex(cache_key, 600, json.dumps(post_data))
        print('Fetched and stored in Cache !!!')
        return post_data

"""
Difference bewtween json.dumps() and json.loads()

json.dumps() takes a Python dictionary and turns it into a text string.
json.loads() takes a text string and turns it into a Python dictionary.
"""
