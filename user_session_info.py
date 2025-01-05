from db_base import FirebaseDBBase
from datetime import datetime
'''
data = {
    'UserId': userId, 
    'SessionUniqId': sessionUniqId, 
    'SessionStartDateTime': time, 
    'SessionEndDatetime': time,
    'SessionTerminated':time,
    'AppVersion': appVersion,
    'DeviceUniqId': deviceUniqId,
    'DeviceLocation': deviceLocation

}'''
class UserSessionInfo(FirebaseDBBase):
    def __init__(self):
        # Initialize the base class with the 'users' collection
        super().__init__('USER_SESSION_INFO')

    def add_user_session(self, userId, sessionUniqId, sessionEndDatetime = None, isTerminated = False, 
                        appVersion= None, deviceUniqId = None, deviceLocation = None ):
        time = int(datetime.now().timestamp())
        data = {
            'UserId': userId, 
            'SessionUniqId': sessionUniqId, 
            'SessionStartDateTime': time, 
            'SessionEndDatetime': time,
            'SessionTerminated':isTerminated,
            'AppVersion': appVersion,
            'DeviceUniqId': deviceUniqId,
            'DeviceLocation': deviceLocation

        }
        id = self.add_document(data)
        data['id'] = id
        self.update_user_session(data)    
        print(f"User Session saved with id: {id}")
        return id

    def get_user_session_by_userid(self, user_id):
        return self.user_session_run_query([("UserId", "==", user_id)])

    def get_user_session_by_sessionid(self, sessionUniqId):
        return self.user_session_run_query([("SessionUniqId", "==", sessionUniqId)])
    
    def get_user_session_by_id(self, id):
        return self.get_document(id)

    def update_user_session(self, data):
        self.update_document(data['id'], data)

    def delete_user_session_by_userid(self, user_id):
        entry = self.user_pref_run_query([("UserId", "==", user_id)])
        self.delete_document(entry['id'])

    def user_session_run_query(self, conditions):
        return self.run_query(conditions)
    
    def user_session_run_or_query(self, or_conditions):
        return self.run_or_query(or_conditions)