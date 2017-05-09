from facepy import GraphAPI
import requests
import json
import argparse
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




access_token="EAACEdEose0cBADXBbaz7XFZAZBNn4sRZBFzkauZCZB3EoOjQytgZAkwLQ6J0PzINbN464xp4NoNQkd8SFGlJwFfrq54bDFLni14GF8QAImcmZBnzWIxdyuVGp9WV9ubBJmZBH1pZCl6BvzRfz1fJR5yucET584RlGg0HrXOSQBNWuSC22AosnXZCq4ABzyVxrKLl4ZD"
access_token="EAACEdEose0cBAP9WDcJSAZBpO3lZAX7wq6kRPJWnZB5ZCqL6n8d9qES28ny6OkwhxuCy3js6gDPQ3DTjZCysFpJE6nUOLZBjkZBY5NhEvlZAsJZA7FEkDJafCkFj5Uuy7lVYnOO7PJzbxlaKyZBeAx5dQTtEEYoMhhM3nmWnPvGSLalouYknjTtg62thjB9WxnSBwZD"
access_token="EAACEdEose0cBADEpH4FxJiApZA1DZCUZC8ZCmZBuOLqkHwiZAZBxcjZBhov443oxcJd2JODWnfRw9XTtvUl5iQFiyPcGue3uo5DzXXItNMgX24ykbyap4C8WiAeVPckNJOfDptUDXUmf3r89ZBQM1t3GbV5bKLrAOZBo6cAIuCLilEiZAeNfTUGuB5VjhDZBS6dzD2AZD"
access_token="EAACEdEose0cBAAuGFcW6lByQdNMr1uMa3p9hpmZAKbKSsZCRCGqa0pWdkxPoDez8x2oCL9pdZAtF4ZAh8p7axsePSjLHfjpZAKFYTnnwTGB9R0n2unZAjsShkGFvuGa7NyXBOZC0csqUb2hg71jHqkJsk44x5mWTwPZAOkzvH4heC4IHAqabMytMzED2oUEFhGwZD"
access_token="EAACEdEose0cBACc0Fae58lQBGbIBZCvvXIZACGd6lmMH0EXUmKyVYNDJGgghLSZBNjR01BDCMrv9PJdZAxymI47vz4f2ZCJNEwZBZBCWZC3HpdKnxlWMyLkgLfhqo4rBYgNqYFggyOZAVkOeYk4co5SYwqjtwyxpS7PZCKbZA1OVQP5AA8JWc0FqRTRes8yoYH5xyMZD"
cookie='''datr=G_KxWLwPZCJtJtj3aPPqDhxN; sb=MfKxWC_VwcYgvbkmjn1xG7qq; pl=n; lu=gg_-3rPmftLQjz-umPqs00GQ; act=1488062502226%2F4; c_user=100014993925849; xs=47%3AAKj-x3tM5RRzOQ%3A2%3A1488056881%3A20908; fr=0uj2dajnP2E6Mw4WZ.AWWfqHmry1PDbXu897TFpSZqDwg.BYsfIb.K5.AAA.0.0.BYsg5d.AWWU5AgM; csm=2; p=-2; presence=EDvF3EtimeF1488064387EuserFA21B14993925849A2EstateFDutF1488064387233CEchFDp_5f1B14993925849F2CC'''

fb_dtsg= "AQGhW8WG2FmQ:AQF_MGGpevEk"


access_token='''EAACEdEose0cBANGJuNNjRUf6yumvkQ3oHUwBfbK6ACky4pwgdTiAYTin6A52isRurQtVXB9UKozaowVOsVQYtZBZAHTrV2CwDTin3kPFd1du4JqPcLPJcaZAIuMS3UpZCCTSfc2rRL0ApIZCBZB685GEnhf2AzZBfOcX49ZBNTc2ZA5xFM9FEuZCzA'''

fb_dtsg="AQGkoQA0YpwT:AQHsrIfsVbnf"

cookie='''datr=uhlpV54kIQPg4VwPnB-khOcq; sb=vhlpV3Rme1qGb_-t5UM5hP95; lu=gQ-9dYfeLakA2Nu5zKv8_UoA; c_user=1675931368; xs=63%3AF4aDKI6pDGfseg%3A2%3A1477051735%3A20908; fr=0CUVEwf3dTz0j8j8e.AWX4WC4VU1k0-hwnmkdBxakalsY.BXaRm6.n2.AAA.0.0.BY9Ii8.AWU8_PoW; presence=EDvF3EtimeF1492420847EuserFA21675931368A2EstateFDutF1492420834546CEchFDp_5f1675931368F0CC; act=1492420867406%2F4'''
access_token='''EAACEdEose0cBACCRlugpxDJEFZAaZAK9vOQAkqVplu9P6hwGLblkrPjGkIWKZA5UmDH92bN7QQy4AUFbxrZCafJdyZBOBWNpLlWd8mVnWYTOxokObhvo0dovbEWxtnrIEJNRLLFFz6QLRi9sa73XetD9hH5gKd6OOmjxHcRMBbQgZBP3TgHVEn'''
access_token='''EAACEdEose0cBAFvhaHrjS6g1h07J4BZB9dWNp9DO5taE0R47H5MVtwaUacONHc6TgQkhOnBhMYCWSOZBgHr80ZATyT3kLCmUmJH0y64orFZAhkjG7PPTdwaiZAKYPVy7pUs1jC6eXKQcdl6XOHDA9LuNhEnI5cgTeCouQOOqwk7Qm6iG0b5hg'''
def recognize(path,access_token,cookies,fb_dtsg):
	""" 
	Face recognition using Facebook's recognize method
		Args:
			path : file path of the photo to be processed
			access_token : Facebook user access token
			cookies : Facebook cookies
			fb_dtsg : special Facebook token required for face recognition
		Returns:
			arr : array of recognitions with the name of recognized people and the certainity of each recognition
	"""

	URL = "https://www.facebook.com/photos/tagging/recognition/?dpr=1"
	
	graph = GraphAPI(access_token)
	
	#Uploading the picture to Facebook	
	post_id = graph.post( path = 'me/photos', source = open(path, 'rb'))['id']
	headers = {
			'x_fb_background_state': '1',
			'origin': 'https://www.facebook.com',
			'accept-encoding': 'gzip, deflate, lzma',
			'accept-language': 'en-US,en;q=0.8',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2723.2 Safari/537.36',			'content-type': 'application/x-www-form-urlencoded',
			'accept': '*/*',
			'referer': 'https://www.facebook.com/',
			'cookie': cookies,
			'dnt': '1',

	}
	
	arr = []
	payload = ""
	
	#Since the POST sometimes returns a blank array, retrying until a payload is obtained
	while not payload:
		data = 'recognition_project=composer_facerec&photos[0]='+post_id+'&target&is_page=false&include_unrecognized_faceboxes=false&include_face_crop_src=true&include_recognized_user_profile_picture=true&include_low_confidence_recognitions=true&__a=1&fb_dtsg='+fb_dtsg
		req = requests.post(URL,data = data,headers=headers)
		payload =  json.loads(req.text.replace('for (;;);',''))['payload']
		if payload:
			break
	print  payload
	for recog in payload[0]['faceboxes']:
		name = recog['recognitions']
		if name:
			arr.append({'name':name[0]['user']['name'] , 'certainity' : name[0]['certainty']})
	
	#Deleting the uploaded picture
	graph.delete(path = post_id)

	return arr






def facebook(image_file,q):
    try:
        people = recognize(image_file,access_token,cookie,fb_dtsg)
        output ="It looks like  "
        logger.info( people)
        for person in people:
   	    if person['certainity'] > 0.3:
                string_rep=str(person['name'])
                q += [string_rep]
	        output+= person['name'] + ", "
        output = output[:-1]
        logger.info("FACEBOOK!!!!!!!!!!!!!!!!!! "+output)
        if len(people) > 0:
            #q.append(people)
            logger.info("Facebook says:::::::::::::::::::::"+ output)
	    return output
        else:
	    return ""
    except Exception as e:
        logger.error(e.message)
        pass




# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    path = args.image_file
    #print(recognize(path,access_token,cookie,fb_dtsg))
    facebook(args.image_file)

