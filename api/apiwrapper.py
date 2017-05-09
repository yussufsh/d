from flask import Flask, request, redirect
from flask_restful import Resource, Api, reqparse
import werkzeug
import aws
import google_vision
import cloudsight_api
from sentence import SentenceGenerator
app = Flask(__name__)
api = Api(app)
from facedetect import facedetect
from threading import Thread
import time
from facebook import facebook

import logging
from summary import Summary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

summary_object = Summary()

class FileUploader(Resource):

    def post(self):
        print str(request)
        start = time.time()

        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('image_id', required=True, type=str, help='Please provide image id with type as str')
        parser.add_argument('session_id', type=str, help='Please provide session id with type as str')
        parser.add_argument('file', required=True, type=werkzeug.datastructures.FileStorage, location='files', help='Please provide image file with type as multipart')
        parser.add_argument('metadata', location='form', help='Please provide metadata with key value pairs as json string')
        parser.add_argument('firebase_id',type=str, help='Please provide metadata with key value pairs as json string')
        args = parser.parse_args()
        f = args['file']
        image_id =args['image_id']
        metadata = args['metadata']
        session_id = args['session_id']
        firebase_id = args['firebase_id']
        logger.info("SESSION_ID is"+ str(session_id))
        logger.info("FIREBASE__ID is"+ str(firebase_id))
        print image_id, metadata

        path="/root/upload/{0}.jpg".format(image_id)
        f.save(path)
        print path

        data = []
        data_names = []

        aws_res = []
        try:
            aws_res = aws.call_aws(path)
        except Exception as e:
            try:
                print "AWS SERVICE FAILED-------------------"
                logger.error("AWS SERVICE FAILED; RETRYING")
                aws_res = aws.call_aws(path)
            except Exception as e:
                try:
                    print "AWS SERVICE FAILED!!!!!!!!!!!!!!!!!!!!"
                    aws_res = aws.call_aws(path)
                    logger.error("AWS SERVICE FAILED AGAIN; RETRYING")
                except Exception as e:
                    print "AWS SERVICE FAILED&&&&&&&&&&&&&&&&&&&&&"
                    logger.error("AWS SERVICE FAILED; Asking google")
                    aws_res = [{u'Confidence': 99.27572631835938, u'Name': u'Meeting'}]

        print aws_res
        for i in aws_res:
            if i['Confidence'] > 75 :
                data.append({i['Name'].lower() : i['Confidence']})
                data_names.append(i['Name'].lower())

        if len(data_names) == 0:
            data.append({aws_res[0]['Name'] : aws_res[0]['Confidence']})


        # google_res = google_vision.call_google(path)
        # print google_res
        # g_res = google_res[0]['labelAnnotations']
        # for i in g_res:
        #     if i['score'] > 0.85 and i['description'].lower() not in data_names  :
        #         data.append({i['description'].lower() : i['score']*100})

        logger.info("AWS GAVE US:" + str(data))

        gr_res = ""
        try:
            s = SentenceGenerator()
            gr_res = s.generate_sentence(data)
        except Exception as e:
            print "GRAMMAR SERVICE FAILED!!!!!!!!!!!!!!!!!!!!"
            gr_res = "I see a Meeting room"

        logger.info("NLTK MODEL:" + str(gr_res))



        t1=Thread(target=cloudsight_api.call_cloudsight,args=(image_id,session_id, path,summary_object,firebase_id))
        t1.start()
        t2=Thread(target=facedetect,args=(image_id,session_id,path,summary_object,firebase_id))
        t2.start()

        return {'image_id': image_id, 'result' : gr_res}

    def get(self):
        return {'hello': 'world'}


class SummaryRest(Resource):
    def get(self,session_id):
        return  summary_object.get_summary(session_id)

class SimpleGet(Resource):
    def get(self):
	location = "http://www.baidu.com/"
	return redirect(location, code=302)

api.add_resource(FileUploader, '/upload')
api.add_resource(SummaryRest, '/summary/<string:session_id>')
api.add_resource(SimpleGet, '/')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)

