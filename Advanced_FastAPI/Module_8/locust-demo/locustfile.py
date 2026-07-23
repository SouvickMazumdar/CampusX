import json
from locust import HttpUser, task, between

# below class will be a simulation, just like a real user
# it will be used to create simulation using HttpUser
class APIUser(HttpUser):
    wait_time=between(1,2)
    @task
    def call_predict(self):
        payload={
            'feature1':1.0,
            'feature2':2.0
        }
        headers={'Content-Type': 'application/json'}
        self.client.post('/predict',data=json.dumps(payload))
    
    @task(1)
    def call_root(self):
        self.client.get('/')