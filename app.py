# import flask dependencies
import sqlite3

import requests, json
from flask import Flask, make_response, jsonify, request, current_app, render_template, g
from card_dict import card



# initialize the flask app
app = Flask(__name__)

RXIMAGE_API = "http://rximage.nlm.nih.gov/api/{apiName}/{apiVersion}/{resourcePath}?{parameters}"

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# default route
@app.route('/')
def index():
    cur = get_db().cursor()
    cur.execute("select * from patient_data")
    rows = cur.fetchall();
    print(rows)
    return render_template('index.html',rows = rows)

# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    print(req)

    color = req.get('queryResult').get('outputContexts')[0].get('parameters').get('color')
    shape = req.get('queryResult').get('outputContexts')[0].get('parameters').get('shape')

    if shape == '3':
        shape = 'triangle'
    elif shape == '4':
        shape = 'trapezoid'
    elif shape == '5':
        shape = 'pentagon'
    elif shape == '6':
        shape = 'hexagon'
    elif shape == '7':
        shape = 'heptagon'
    elif shape == '8':
        shape = 'octagon'

    writing = req.get('queryResult').get('outputContexts')[0].get('parameters').get('writing')

    params = "color={color}&shape={shape}&writing={writing}".format(color=color,shape=shape,writing=writing)

    rx_api_str = RXIMAGE_API.format(apiName="rximage",apiVersion="1",resourcePath="rxnav",parameters=params)

    rx_req = requests.request('GET',rx_api_str)

    rx_dict = json.loads(rx_req.text)
    print(rx_dict)
    reply_status = rx_dict['replyStatus']
    if reply_status['success'] != True:
        return {'fulfillmentText': "Sorry, I couldn't find a pill that matched your description."}

    if 'nlmRxImages' not in rx_dict:
        return {'fulfillmentText': "Sorry, I couldn't find a pill that matched your description."}

    items = rx_dict['nlmRxImages']
    if len(items) == 0:
        return {'fulfillmentText': "Sorry, I couldn't find a pill that matched your description."}

    pill = items[0]
    new_card = card.copy()
    new_card["fulfillmentText"] = pill['name']

    new_card['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = pill['name']

    card_content = new_card['payload']['google']['richResponse']['items'][1]['basicCard']

    card_content['subtitle'] = pill['name']
    card_content['image']['url'] = pill['imageUrl']
    card_content['image']["accessibilityText"] = pill['name']
    card_content['buttons'][0]['openUrlAction']['url'] = 'http://www.google.com/search?q={name}'.format(name=pill['name'])

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO patient_data (name, color, shape, writing, identified_pill) VALUES (?,?,?,?,?)",
                ("testuser",color,shape,writing,pill['name']))
    db.commit()

    # return a fulfillment response
    print(new_card)
    return new_card

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
    app.run()