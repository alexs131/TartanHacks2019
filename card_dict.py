import copy

card = {
  "fulfillmentText": "",
  "payload": {
    "google": {
      "expectUserResponse": False,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": ""
            }
          },
          {
            "basicCard": {
              "title": "Your Pill",
              "subtitle": "",
              "image": {
                "url": "https://example.com/image.png",
                "accessibilityText": ""
              },
              "buttons": [
                {
                  "title": "More Information",
                  "openUrlAction": {
                    "url": "https://assistant.google.com/"
                  }
                }
              ],
              "imageDisplayOptions": "CROPPED"
            }
          }
        ]
      },
    }
  },
  "fulfillmentMessages": [
  ],
}

carousel = {
  "fulfillmentText": "",
  "payload": {
    "google": {
      "expectUserResponse": False,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "",
              "displayText": ""
            }
          },
          {
            "carouselBrowse": {
              "items": [

              ]
            }
          }
        ]
      },
    }
},  "fulfillmentMessages": [
  ],


}

carousel_item = {
  "title": "Pill 1",
  "openUrlAction": {
    "url": "google.com"
  },
  "image": {
    "url": "IMG_URL.com",
    "accessibilityText": "Image alternate text"
  }
}

def generate_dict(pills, session_info):
  new_resp = copy.deepcopy(carousel)

  new_resp['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Here's what I found: "
  new_resp['payload']['google']['richResponse']['items'][0]['simpleResponse']['displayText'] = "Here's what I found: "
  new_resp['fulfillmentText'] = "Here's what I found: "

  items = new_resp['payload']['google']['richResponse']['items'][1]['carouselBrowse']['items']
  #pill_ndcs = []
  for i in range(4):
    if i < len(pills):
      new_item = copy.deepcopy(carousel_item)
      new_item['title'] = pills[i]['name']
      new_item['openUrlAction']['url'] = 'http://www.google.com/search?q={name}'.format(name=pills[i]['name'])
      new_item['image']['url'] = pills[i]['imageUrl']
      new_item['image']['accessibilityText'] = pills[i]['name']
      #pill_ndcs.append(pills[i]['relabelersNdc9'][0]['ndc9'][0])
      items.append(new_item)

      #new_resp['fulfillmentText'] += (', ' + pills[i]['name'])
      new_resp['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] += (', ' + pills[i]['name'])

    else:
      break



  new_resp['payload']['google']['richResponse']['items'][0]['simpleResponse']['textToSpeech'] += ", Would you like to know more?"
  #new_resp['outputContexts'][0]['parameters']['ndcs'] = str(pill_ndcs)
  #new_resp['followupEventInput']['parameters']['ndcs'] = str(pill_ndcs)
  #new_resp['outputContexts'][0]['name'] = (session_info + "MoreInfo")
  return new_resp