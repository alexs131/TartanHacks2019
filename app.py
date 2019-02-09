# import flask dependencies
import requests, json
from flask import Flask, make_response, jsonify, request

# initialize the flask app
app = Flask(__name__)

RXIMAGE_API = "http://rximage.nlm.nih.gov/api/{apiName}/{apiVersion}/{resourcePath}?{parameters}"

# default route
@app.route('/')
def index():
    return 'Hello World!'

# function for responses
def results():
    print("called")

    # build a request object
    req = request.get_json(force=True)

    intent = req.get('queryResult').get('intent').get('displayName')

    color = req.get('queryResult').get('parameters').get('color')
    shape = req.get('queryResult').get('parameters').get('shape')
    writing = req.get('queryResult').get('parameters').get('writing')

    params = "color={color}&shape={shape}&writing={writing}".format(color=color,shape=shape,writing=writing)

    rx_api_str = RXIMAGE_API.format(apiName="rximage",apiVersion="1",resourcePath="rxnav",parameters=params)

    rx_req = requests.request('GET',rx_api_str)
    rx_dict = json.loads(rx_req.text)
    items = rx_dict['nlmRxImages']


    # return a fulfillment response
    return {'fulfillmentText': color}

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
   app.run()