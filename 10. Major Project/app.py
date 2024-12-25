import os
import pandas as pd 
import numpy as np 
import flask
import pickle
import sklearn
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def index():
 return render_template('index.html')

                              
def ValuePredictor(to_predict_list):
 print("Input to model:", to_predict_list)  # Debugging line
 to_predict = np.array(to_predict_list).reshape(1,-1)
 loaded_model = pickle.load(open("model.pkl","rb"))
 result = loaded_model.predict(to_predict)
 return result

@app.route('/predict',methods = ['POST'])
def result():
 if request.method == 'POST':
    to_predict_list = request.form.to_dict()
    to_predict_list=list(to_predict_list.values())
    result = ValuePredictor(to_predict_list)
    prediction = int(result)
    
    if prediction == 1:
        predicted_result = 'Viable. Can be approved'
    else:
        predicted_result = 'Not Viable. Advisable to be Rejected'

    return render_template('predict.html',prediction=predicted_result)
                        
if __name__ == "__main__":
    app.run(debug=True)