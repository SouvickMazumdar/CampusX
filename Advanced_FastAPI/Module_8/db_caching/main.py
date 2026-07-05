import sqlite3
import redis
import json
import hashlib
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()
redis_client=redis.Redis(host='localhost',port=6379, db=0)

# establish db connection
def get_db_connection():
    conn=sqlite3.connect('db.sqlite3')
    conn.row_factory=sqlite3.Row  #make row behave like a dictionary
    return conn

# set up the database
def init_db():
    conn=get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
                   id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   age INTEGER
                   )
    """)
    cursor.execute("INSERT INTO users (id, name, age) VALUES (1, 'Michael',45) ON CONFLICT(id) DO NOTHING")
    cursor.execute("INSERT INTO users (id, name, age) VALUES (2, 'Tim',35) ON CONFLICT(id) DO NOTHING")
    cursor.execute("INSERT INTO users (id, name, age) VALUES (3, 'Jim',25) ON CONFLICT(id) DO NOTHING")
    cursor.execute("INSERT INTO users (id, name, age) VALUES (4, 'Rim',15) ON CONFLICT(id) DO NOTHING")
    conn.commit()
    conn.close()

init_db()
class UserQuery(BaseModel):
    user_id: int

def make_cache_key(user_id: int):
    raw=f"user:{user_id}"
    return hashlib.sha256(raw.encode()).hexdigest()

@app.post('/get-user')
def get_user(query: UserQuery):
    cache_key=make_cache_key(query.user_id)
    cached_result=redis_client.get(cache_key)
    if cached_result:
        print("Serving prediction from Cache")
        return json.loads(cached_result)
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute("Select * FROM users WHERE id = ?", (query.user_id,))
    row=cursor.fetchone()
    conn.close()
    if row is None:
        return {'message': 'User not found.'}
    result ={'id': row['id'], 'name':row['name'], 'age':row['age']}
    redis_client.setex(cache_key, 3600, json.dumps(result))
    print('Fetched from database and cached')
    return result


