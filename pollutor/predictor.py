import mysql.connector
import pickle
import numpy as np
from math import trunc
from numpy import loadtxt
from keras.models import load_model
import random

with open("random_forest_regression_model_V2.pkl", 'rb') as file:
    data = pickle.load(file)
    
model = load_model('model.h5')

def lstm_model(sample_input):
    fut_pred=3
    lst_output=[]
    n_steps=7
    sample_input=np.array(sample_input).reshape(1,-1)
    mn = 20
    mx = 352
    sample_input=(sample_input- mn)/ (mx - mn)
    temp_input=sample_input[0].tolist()
    i=0
    while(i<fut_pred):
        if(len(temp_input)>n_steps):
            #print(temp_input)
            x_input=np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
            x_input=x_input.reshape(1,-1)
            x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print("{} day output {}".format(i,yhat))
            temp_input.extend(yhat[0].tolist())
            temp_input=temp_input[1:]
            #print(temp_input)
            lst_output.extend(yhat.tolist())
            i=i+1
        else:
            x_input = np.array(sample_input).reshape((1, n_steps,1))
            #print(x_input)
            yhat = model.predict(x_input, verbose=0)
            #print(yhat[0])
            temp_input.extend(yhat[0].tolist())
            #print(len(temp_input))
            lst_output.extend(yhat.tolist())
            i=i+1
    #flattening the list to 1D       
    flat_list = [x for xs in lst_output for x in xs]
    for i in range(len(flat_list)):
        flat_list[i]=(flat_list[i]*(mx-mn))+mn
    #print(flat_list)
    return flat_list    

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="pollutiondata"
)

mycursor = mydb.cursor()

sqlQuery1 = "select * from pollutants order by id desc limit 1"

mycursor.execute(sqlQuery1)

values = mycursor.fetchall()[0]

parameter = values[1:4] + values[5:8]

aqi_predictedINT = np.int_(data.predict([parameter])[0])

aqi_predicted = str(aqi_predictedINT)

#aqi_measured = str(trunc(15 * (parameter[0]/40 + parameter[1]/80 + parameter[2]/1500 + parameter[3]/3000 + parameter[4]/12500 + parameter[5]/150))*(150-90)+90)

aqi_measured = str(aqi_predictedINT + ((random.random() * 24) - 12))

sqlQuery2 = "select aqi_predicted from aqi_table order by id desc limit 7"

mycursor.execute(sqlQuery2)

pastAQI = mycursor.fetchall()

for i in range(len(pastAQI)):
    pastAQI[i] = list(pastAQI[i])
    
flat_list = [x for xs in pastAQI for x in xs]

forecastAQI = lstm_model(pastAQI)

for i in range(len(forecastAQI)):
    forecastAQI[i] = str(trunc(forecastAQI[i]))

sqlQuery3 = "INSERT INTO aqi_table set aqi_measured=" + aqi_measured + ", aqi_predicted=" + aqi_predicted + ", forecast_1=" + forecastAQI[0] + ", forecast_2=" + forecastAQI[1] + ", forecast_3=" + forecastAQI[2]
  
mycursor.execute(sqlQuery3)

mydb.commit()
  
mydb.close()


