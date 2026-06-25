import redis
r= redis.Redis(host='localhost',port=6379,db=0)
try:
    if r.ping():
        print('Connected to Redis')
except redis.ConnectionError:
    print("Redis Connectionn failed")


r.set('framework','FastAPI')

value=r.get('framework')

print(f"Stored Value for framework: {value.decode()}")