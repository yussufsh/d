
import httplib, urllib, base64
import argparse
import base64
import json
import os
from threading import Thread
import time
import Queue
import cloudsight_api
#from facebook import facebook
from clarifai.rest import ClarifaiApp
from threading import Thread
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_google(photo_file,q=[]):
    """Run a label request on a single image"""

    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)
    # [END authenticate]

    # [START construct_request]
    start = time.time()
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [
                {
                    'type': 'LABEL_DETECTION',
                    'maxResults': 100
                },
                ]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        #print "GOOGLE ANALYSED"
	    #result = json.dumps(response,indent=4)
    end = time.time()
    logger.info("Time taken by Google: " + str(end - start))
    return response['responses']
        
def main(photo_file):
    try:
        q=[]
        cloudsight_q=[]
        with open(photo_file, 'rb') as image:
            image_content = image.read()
        #t1=Thread(target=call_vision,args=(image_content,q))
        #t2=Thread(target=call_emotion,args=(image_content,q,photo_file))
        #t3=Thread(target=call_cloudsight,args=(photo_file,cloudsight_q))
        #t4=Thread(target=call_clarifai,args=(photo_file,q))
        t5=Thread(target=call_google,args=(photo_file,q))
        #t6=Thread(target=call_vision_analyse,args=(image_content,q))
        #t1.start()
        #t2.start()
        #t3.start()
        #t4.start()
        t5.start()
        #t6.start()
        #t1.join()
        #t2.join()
        #t4.join()
        t5.join()
        #t6.join()
        #q.reverse()


        output=''
        for item in q:
            output=output+item 

        return output
        #t3.join()
        #print cloudsight_q
        #os.system("python ~/python-docs-samples/vision/api/label/label.py ~/microsoft-vision/%s" % photo_file)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return "Error"

        #print("[Errno {0}] {1}".format(e.errno, e.strerror))
        #print e

# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    print main(args.image_file)


