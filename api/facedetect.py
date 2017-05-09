import requests
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from firebase import Firebase
from summary import Summary
from facebook import facebook
from threading import Thread
from fuzzywuzzy import fuzz

#url = "http://35.185.68.150:7644/face-id"
url = "http://104.196.153.37:7644/face-id"


def facedetect(image_id, session_id, image_path, summary_object , firebase_id):
    q=[]
    t1=Thread(target=facebook,args=(image_path,q))
    t1.start()
   
    files = {'file': open(image_path,'rb')}
    #r = requests.post(url, files=files)
    #json_data = json.loads(r.text)
    #print json_data

    t1.join()
        
    #faces = json_data['predictions'] 
    #people = list(faces.keys())
    people = []
    logger.info("OPENFACE SENT:::::"+ str(people))
    if len(q) != 0:
        facebook_faces=q
        logger.info("Facebook got::::"+ str(facebook_faces))
        for face in facebook_faces:
           match=False
           for person in people:
              if fuzz.ratio(face,person) > 60:
                  match = True
           if not match:
              people.append(face)
    logger.info("ALL detected faces:"+ str(people))
    summary_object.add_faces(session_id, people )
    if len(people) == 0:
        return
    message = "I see "
    for i,person in enumerate(people):
        if len(people) > 1 and i == len(people)-1:
            message += " and " + person.replace("_",' ') +"."
        elif len(people) == 1:
            message += person.replace('_',' ')
        else:
            message += person.replace('_',' ')+", " 
    print message
    try:
        firebase = Firebase()
        result = firebase.push(image_id,'faces',message, firebase_id)
        logger.info("pushed to firebase"+ str(result))
    except Exception as e:
        logger.error("error pushing")
        logger.error(e.message)
        pass

    

if __name__ == '__main__':
    facedetect("1","/home/pranav_tendolkar/one.jpg")
                                                                   

