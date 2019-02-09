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
            "carouselBrowse": {
              "items": [
                {
                  "title": "Pill 1",
                  "openUrlAction": {
                    "url": "google.com"
                  },
                  "description": "Description of item 1",
                  "footer": "Item 1 footer",
                  "image": {
                    "url": "IMG_URL.com",
                    "accessibilityText": "Image alternate text"
                  }
                },
                {
                  "title": "Pill 2",
                  "openUrlAction": {
                    "url": "google.com"
                  },
                  "description": "Google Assistant on Android and iOS",
                  "footer": "More information about the Google Assistant",
                  "image": {
                    "url": "IMG_URL_Assistant.com",
                    "accessibilityText": "Image alternate text"
                  }
                },
                {
                  "title": "Pill 3",
                  "openUrlAction": {
                    "url": "google.com"
                  },
                  "description": "Google Assistant on Android and iOS",
                  "footer": "More information about the Google Assistant",
                  "image": {
                    "url": "IMG_URL_Assistant.com",
                    "accessibilityText": "Image alternate text"
                  }
                },
              ]
            }
          }
        ]
      },
    }
}

}
