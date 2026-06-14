import joblib
import numpy as np
from typing import List

saved_model=joblib.load('model.joblib')
print("Loaded the Model")

def make_prediction(data: dict) -> float:
    features=np.array([
        [
            data['longitude'],
            data['latitude'],
            data['housing_median_age'],
            data['total_rooms'],
            data['total_bedrooms'],
            data['population'],
            data['households'],
            data['median_income']
        ]
    ])
    return saved_model.predict(features)[0]



def batch_prediction(data: List[dict]) -> np.array:
    # dict is converted into numpy array because ml model expect either numpy array or pandas dataframe
    features=[]
    for each in data:
        one=[
            each['latitude'],
            each['longitude'],
            each['housing_median_age'],
            each['total_rooms'],
            each['total_bedrooms'],
            each['population'],
            each['households'],
            each['median_income']
        ]
        features.append(one)

    ans=np.array(features)
    print(type(ans[0]))
    return saved_model.predict(ans)

