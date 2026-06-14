import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

df=pd.read_csv('D:\Project\CampusX\Model_Serializable\Serving ML Model\housing.csv').iloc[:,:-1].dropna()
print("Read the dataset")

X=df.drop(columns='median_house_value')
y=df.median_house_value.copy()
print("Split the dataset")

model=LinearRegression().fit(X,y)
print('Trained the Model')

joblib.dump(model,'model.joblib')
print('Save the Model')

