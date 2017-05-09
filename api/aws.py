import boto3
import argparse
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = boto3.client('rekognition')

def call_aws(image_path):
    start=time.time()
    response = ""
    with open(image_path,'rb') as f:
        byte_data = f.read()
        #client = boto3.client('rekognition')
        response = client.detect_labels( Image={'Bytes': byte_data })
    end=time.time()
    #print "Time taken:"+str(end-start)
    # result=""
    # for item in response['Labels']:
    #     result+=item['Name'] +', '

    logger.info("Time taken by AWS: "+str(end-start))
    return response['Labels']

    


# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    print call_aws(args.image_file)
