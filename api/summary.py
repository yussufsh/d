'''
This was a meetiung,
held at place and time
Looked like durga was present, bu i coulndt find xyz
there were x number of Photos clicked,
they contained,
    second level info
'''
import pickle
from threading import Thread

import fcntl

import errno

import time

import copy
import datetime
now = datetime.datetime.now()

meetingdetails = "You recorded this interaction on "

class WriteThread(Thread):
    def __init__(self, summaries):
        ''' Constructor. '''
        Thread.__init__(self)
        self.summaries = summaries

    def run(self):
        file = open("summaries.pkl", "wb")
        while True:
            try:
                fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                pickle.dump(self.summaries, file)
                fcntl.flock(file, fcntl.LOCK_UN)
                break
            except IOError as e:
                # raise on unrelated IOErrors
                if e.errno != errno.EAGAIN:
                    raise
                else:
                    time.sleep(0.3)
        file.close()


class Summary:
    summaries={}

    def __init__(self):
        try:
            self.summaries = pickle.load(open("summary.pkl", "rb"))
        except:
            pass


    def dump_data(self):
        writeThreadObj = WriteThread(summaries=copy.deepcopy(self.summaries))
        writeThreadObj.start()

    def add_faces(self, session_id, data ):
        try:
            self.summaries[session_id]['faces'] += data;
        except KeyError:
            self.add_meeting_details(session_id,meetingdetails + str(now.strftime("%x") + ". ") )
            self.summaries[session_id]['faces'] = data;
        self.dump_data()

    def add_second_level(self, session_id, data):
        try:
            self.summaries[session_id]['secondlevel'].append(data)
        except KeyError:
            self.add_meeting_details(session_id,meetingdetails +  str(now.strftime("%x") + ". "))
            self.summaries[session_id]['secondlevel']=[]
            self.summaries[session_id]['secondlevel'].append(data)
        self.dump_data()

    def add_meeting_details(self, session_id, data):
	try:
	    self.summaries[session_id]['meetingdetails']=data;
        except KeyError:
            self.summaries[session_id]={}
            self.summaries[session_id]['meetingdetails']=data;
        self.dump_data()
        pass

    def get_summary(self,session_id):
        summary = self.summaries[session_id]['meetingdetails']
        try:
            if len(self.summaries[session_id]['faces'] ) >0:
                summary+= "Looks like"
		setoffaces = set(self.summaries[session_id]['faces'])
                for face in setoffaces:
                    summary+=', ' + face.replace('_', ' ')
                if(self.summaries[session_id]['faces'] == 1):
		    summary+=" was present."
	        else:
		    summary+=" were present."
        except:
            pass

        try:
            summary+= "You clicked %s pictures, with the contents including," % (len(self.summaries[session_id]['secondlevel']))
            for detail in self.summaries[session_id]['secondlevel']:
                summary += detail + ", "
	    summary=summary[:-2]
        except:
            pass
        return summary
