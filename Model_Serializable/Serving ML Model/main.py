from fastapi import FastAPI
from schemas import InputSchema, OutputSchema
from predict import make_prediction, batch_prediction
from typing import List

app=FastAPI()

@app.get('/')
def index():
    return {'message': 'Welcome to the ML Model Predicitno API'}

@app.post('/prediction', response_model=OutputSchema)
def predict(user_input: InputSchema):
    prediction=make_prediction(user_input.model_dump()) #Converting json to dictionary
    return OutputSchema(predicted_price=prediction)


@app.post('/batch_prediction', response_model=List[OutputSchema])
def batch_prediction_endpoint(user_input: List[InputSchema]):
    input_array=[]
    for each in user_input:
        input_array.append(each.model_dump())
    # print(type(input_array[0]))
    predictions=batch_prediction(input_array) # Converting json to dictionary
    # print(type(prediction))
    # print(prediction)
    # prediction=prediction.tolist()
    # print(type(prediction))
    return [OutputSchema(predicted_price= prediction) for prediction in predictions]
    # return prediction


