import argparse
import cloudsight
import time
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from firebase import Firebase
from threading import Thread

#api_key = 'Gw8g6_vn-hfPhixcBEXuhg'
#secret = 'zmRP7MT7UrOcOWBJcN9r4A'
api_key = 'VJMwBOL9tAXEIqqWHe70pg'
secret = 'LxoMz2G6ZSdbv28U_JTs0w'
def call_cloudsight(image_id,session_id, photo_file,summary_object, firebase_id ,q=[]):

    response = []
    call_cs(photo_file, response)
    if not response:
        call_cs(photo_file, response)

    try:
       firebase = Firebase()
       result = firebase.push(image_id,'secondlevel',response[0], firebase_id)
       logger.info("pushed to firebase"+ str(result))
       summary_object.add_second_level(session_id, response[0])
    except Exception as e:
       logger.error("error pushing")
       logger.error(e.message)
       pass


def call_cs(photo_file, res=[]):
    print "inside call"
    try:
        # auth = cloudsight.SimpleAuth('miOkt71mVHbtGk8PPrenPA')
        auth = cloudsight.OAuth(api_key, secret)
        api = cloudsight.API(auth)
        start = time.time()
        with open('%s' % photo_file, 'rb') as f:
            response = api.image_request(f, '%s' % photo_file, {'image_request[locale]': 'en-US', })
        status = api.image_response(response['token'])
        if status['status'] != cloudsight.STATUS_NOT_COMPLETED:
            pass
        status = api.wait(response['token'], timeout=30)
        end = time.time()
        print "Cloudsight took %s :" % (end - start)
        response = json.loads(json.dumps(status))
        logger.info("CLOUDSIGHT SAYS : " + response['name'])
        logger.info("Time taken by Cloudsight: " + str(end - start))
        logger.info("CS: " + response['name'])
        res.append(response['name'])
    except Exception as e:
        # --TODO--
        print "CLOUDSIGHT FAILED!!!!!!!"
        logger.info("CLOUDSIGHT FAILED!!!!!!!")
        logger.error(e.message)

# [START run_application]
if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('image_file', help='The image you\'d like to label.')
    # args = parser.parse_args()
    print call_cloudsight('12.jpg','/root/upload/12.jpg')

