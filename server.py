import pickle 

import pandas as pd
from flask import Flask, jsonify, request


app = Flask(__name__)

# load model

loaded_model = pickle.load(open('finalized_model.sav', 'rb'))


#  Bind method to predict endpoint of server
@app.route('/predict', methods=['POST'])
def predict():
    # Extract fields from request that was sent by client
    basket = request.json['basket']
    zipCode = request.json['zipCode']
    totalAmount = request.json['totalAmount']
    print("Processing request: {},{},{}".format(basket, zipCode, totalAmount))
    
    # trasforming the data
    df_data = trasformdata(basket, zipCode, totalAmount)
    
    # predicting
    
        
    p = probability(df_data)
    #  Return return probability to client (as json)
    return jsonify({'probability': p}), 201

def probability(df):
    prediction_result = loaded_model.predict_proba(df)
    print(prediction_result)
    return prediction_result[0][1]
    

def trasformdata(basket, zipCode, totalAmount):
    print('Trasforming data')
    d = {'totalAmount': totalAmount, 'basket': [basket], 'zipCode': zipCode}
    df = pd.DataFrame(data=d)
    
    df['c_0'] = df.basket.map(lambda x: x.count(0))
    df['c_1'] = df.basket.map(lambda x: x.count(1))
    df['c_2'] = df.basket.map(lambda x: x.count(2))
    df['c_3'] = df.basket.map(lambda x: x.count(3))
    df['c_4'] = df.basket.map(lambda x: x.count(4))
    df['c_5'] = df.basket.map(lambda x: x.count(5))
    
    df['zipCode'] = pd.Categorical(df['zipCode'], categories=list(range(1000,20000)))
    dummies = pd.get_dummies(df.zipCode)
    
    df = pd.concat([df, dummies], axis=1)
    
    df.drop(["basket", "zipCode"], axis=1, inplace=True)
    print('Data trasformtion completed')
    return df 

if __name__ == "__main__":
	app.run(debug=True)
