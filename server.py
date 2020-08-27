from flask import Flask, jsonify, request

app = Flask(__name__)

#  Bind method to predict endpoint of server
@app.route('/predict', methods=['POST'])

def predict():
    # Extract fields from request that was sent by client
    basket = request.json['basket']
    zipCode = request.json['zipCode']
    totalAmount = request.json['totalAmount']
    p = probability(basket, zipCode, totalAmount)
    #  Return return probability to client (as json)
    return jsonify({'probability': p}), 201

def probability(basket, zipCode, totalAmount):
    print("Processing request: {},{},{}".format(basket, zipCode, totalAmount))
    return 0.0

if __name__ == "__main__":
	app.run(debug=True)
