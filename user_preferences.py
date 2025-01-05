from db_base import FirebaseDBBase
from datetime import datetime
'''
{
    'UserId': '', 
    'VotCatId': '', 
    'IsActive': '', 
    'CreationTime':'',
    'Modifiedtime':'',
}'''
class UserPreferences(FirebaseDBBase):
    def __init__(self):
        # Initialize the base class with the 'users' collection
        super().__init__('USER_PREFERENCES')

    def add_user_pref(self, user_id, votcatId, isActive = True):
        time = int(datetime.now().timestamp())
        data = {
            'UserId': user_id, 
            'VotCatId': votcatId, 
            'IsActive': isActive, 
            'CreationTime': time,
            'Modifiedtime':time,
        }
        id = self.add_document(data)
        data['id'] = id
        self.update_user_pref(data)    
        print(f"Preference saved with id: {id}")
        return id

    def get_user_pref_by_userid(self, user_id):
        return self.user_pref_run_query([("UserId", "==", user_id)])

    def get_user_pref_by_id(self, id):
        return self.get_document(id)

    def update_user_pref(self, data):
        data['Modifiedtime'] = int(datetime.now().timestamp())
        self.update_document(data['id'], data)

    def delete_user_pref_by_userid(self, user_id):
        entry = self.user_pref_run_query([("UserId", "==", user_id)])
        self.delete_document(entry['id'])

    def user_pref_run_query(self, conditions):
        return self.run_query(conditions)
    
    def user_pref_run_or_query(self, or_conditions):
        return self.run_or_query(or_conditions)