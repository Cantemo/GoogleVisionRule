#!/opt/cantemo/python/bin/python
"""
A Rules Engine 3 script to integrate Google Vision image analysis (https://cloud.google.com/vision/) with
Cantemo Portal.

.. Copyright 2016 Cantemo AB. All Rights Reserved
"""
# Add Portal classes to path and setup Django environment.
import sys
import os

sys.path.append("/opt/cantemo/portal")
os.environ['DJANGO_SETTINGS_MODULE'] = 'portal.settings'

# Settings must be imported to setup logging correctly
from portal import settings
import logging
import requests
import base64
import json
# Logging through standard Portal logging, i.e. to /var/log/cantemo/portal/portal.log
log = logging.getLogger('portal.plugins.rulesengine3.shellscripts.google_vision')

# Fill in your own Google Vision API key below, also called "Browser key". For more information, see
# https://cloud.google.com/vision/docs/auth-template/cloud-api-auth
VISION_API_KEY = ''

# Tags from Label Detection are stored into this metadata field
TAGS_FIELD = 'portal_mf572883'

# Texts from Text Detection are stored into this metadata field
OCR_FIELD = 'portal_mf915296'

# The full JSON from Google Vision is stored into this field
FULL_OUTPUT_FIELD = 'portal_mf700776'

VISION_URL = 'https://vision.googleapis.com/v1/images:annotate?key=%s' % VISION_API_KEY
# The request sent to Google Vision, listing the requested features. For full list of available features, see:
# https://cloud.google.com/vision/docs/requests-and-responses#types_of_vision_api_requests
VISION_JSON = """{
  "requests":[
    {
      "image":{
        "content":"IMAGE_CONTENTS_BASE64"
      },
      "features":[
        {
          "type":"LABEL_DETECTION",
          "maxResults":10
        },
        {
          "type":"TEXT_DETECTION",
          "maxResults":10
        }
      ]
    }
  ]
}
"""

item_id = os.environ.get('portal_itemId')
if item_id:
    from portal.vidispine.iitem import ItemHelper

    ith = ItemHelper()
    item = ith.getItem(item_id)
    log.info('Item title: %s / type: %s / metadata: %s', item.getTitle(), item.getMediaType(),
             item.getMetadataFieldGroupName())
    # If item is an image, with the GoogleVision metadata schema, perform the analysis
    if item.getMediaType() == 'image' and item.getMetadataFieldGroupName() == 'GoogleVision':
        log.info('Getting original image data')
        vsfile = item.getOriginalTag().getVideoComponents()[0].getFiles()[0]
        r = requests.get(vsfile.json_object['uri'][0])
        image_data = r.content

        # Replace placeholder in the request JSON with Base64 encoded image data
        json_data = VISION_JSON.replace('IMAGE_CONTENTS_BASE64', base64.encodestring(image_data))

        # Make request to Google Vision API
        gr = requests.post(VISION_URL, json_data)
        gr.raise_for_status()
        log.info('Google vision output: %s', gr.json())

        # Parse response
        tags = []
        ocr_text = ""
        for x in gr.json().get('responses', []):
            for y in x.get(u'labelAnnotations', []):
                tags.append(y['description'])
            for y in x.get(u'textAnnotations', []):
                ocr_text += y['description']
                ocr_text += '\n\n'

        # Store values to item metadata
        ith.setItemMetadataFieldValue(item_id, TAGS_FIELD, tags)
        ith.setItemMetadataFieldValue(item_id, OCR_FIELD, ocr_text)
        ith.setItemMetadataFieldValue(item_id, FULL_OUTPUT_FIELD, json.dumps(gr.json(), indent=2))
    else:
        log.info('Not valid type or schema, skipping analysis')
else:
    log.info('portal_itemId not set')

log.info('Done: %s' % item_id)
