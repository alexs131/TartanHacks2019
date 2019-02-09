# import flask dependencies
import sqlite3

import requests, json
from flask import Flask, make_response, jsonify, request, current_app, render_template, g
from card_dict import *



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

def more_information(ndc):
    fda_query = "https://api.fda.gov/drug/label.json?search=\"{ndc}\"&limit=1".format(ndc = ndc)

    fda_req = requests.request(fda_query)


# function for responses
def results():
    # build a request object
    req = request.get_json(force=True)
    print(req)

    intent = req.get('queryResult').get('intent').get('displayName')
    if (intent == 'MoreInfo'):
        print("yes")
        return {}

    color = ""
    writing = ""
    #color = req.get('queryResult').get('outputContexts')[0].get('parameters').get('color')
    shape = req.get('queryResult').get('outputContexts')[0].get('parameters').get('shape')
    #writing = req.get('queryResult').get('outputContexts')[0].get('parameters').get('writing')
    shape2 = req.get('queryResult').get('outputContexts')[0].get('parameters').get('shape2')
    sides = req.get('queryResult').get('outputContexts')[0].get('parameters').get('sides')

    session_info_pre = req.get('queryResult').get('outputContexts')[0].get('name')
    session_info_split = session_info_pre.split('/')
    session_info = "/".join(session_info_split[0:len(session_info_split)-1]) + "/"
    print(session_info)

    if shape2:
        shape = shape2
    if sides:
        if sides == '3':
            shape = 'triangle'
        elif sides == '4':
            shape = 'trapezoid'
        elif sides == '5':
            shape = 'pentagon'
        elif sides == '6':
            shape = 'hexagon'
        elif sides == '7':
            shape = 'heptagon'
        elif sides == '8':
            shape = 'octagon'

    for context in req.get('queryResult').get('outputContexts'):
        if context.get('parameters').get('color'):
            color = context.get('parameters').get('color')
            writing = context.get('parameters').get('writing')
            break


    params = "color={color}&shape={shape}&imprint={writing}".format(color=color,shape=shape,writing=writing)

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

    final_dict = generate_dict(items,session_info)
    print(final_dict)

    pill_names = []
    for i in range(4):
        if i < len(items):
            pill_names.append(items[i]['name'])
        else:
            break

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO patient_data (name, color, shape, writing, identified_pill) VALUES (?,?,?,?,?)",
                ("John Doe",color,shape,writing,str(pill_names)))
    db.commit()

    return final_dict

# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    print("Request!!")
    # return response
    return make_response(jsonify(results()))

# run the app
if __name__ == '__main__':
    app.run()
