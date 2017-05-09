from pyfcm import FCMNotification
import  json
class Firebase:
   API_KEY="AAAAqbc0vrg:APA91bE3-V7VdPTF5SFhNcUaIB_hI0245BHBufJsLq_PeuUQ_k2LKS92tWcpf_TSiAUfTktI75tPWwuce5ck37xpUFy0HpWMJyLhZIIsslP4cmiZ57RV9VUO4sBsChbYjINXibXyia9D"
   TOPIC_NAME = "sceneData"
   push_service = FCMNotification(api_key=API_KEY)
   def push(self,id,type,result, firebase_id):
       data = {}
       data['image_id'] = id
       data['result'] = result
       data['tag'] =  type
       if firebase_id is None:
           result = self.push_service.notify_topic_subscribers(topic_name=self.TOPIC_NAME, message_body=json.dumps(data))
       else:
           result = self.push_service.notify_single_device(registration_id=firebase_id, message_body=json.dumps(data))
       return result

