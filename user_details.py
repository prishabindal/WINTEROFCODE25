from datetime import datetime
from db_base import FirebaseDBBase

class UserDetails(FirebaseDBBase):
    def __init__(self):
        # Initialize the base class with the 'users' collection
        super().__init__('USER_DETAILS')

    def add_user(self, username, password, phoneNumber, firstName, middleName = None, lastName = None, 
                alternatePhoneNumber = None, encryptionToken = None, deviceUniqId = None):
        time = int(datetime.now().timestamp())
        data = {
            'Username': username, 
            'Password': password, 
            'FirstName':firstName,
            'MiddleName': middleName,
            'LastName': lastName,
            'PhoneNumber': phoneNumber,
            'AlternatePhoneNumber': alternatePhoneNumber,
            'CreationTime':time,
            'Modifiedtime':time,
            'EncryptionToken':encryptionToken,
            'DeviceUniqId':deviceUniqId
        }
        user_id = self.add_document(data)
        data['UserId'] = user_id
        self.update_user(user_id, data)
        print(f"User added with ID: {user_id}")
        return user_id

    def get_user(self, user_id):
        return self.get_document(user_id)
    
    def get_user_by_username(self, username):
        return self.user_run_query([("Username", "==", username)])

    def update_user(self, user_id, data):
        data['Modifiedtime'] = int(datetime.now().timestamp())
        self.update_document(user_id, data)

    def delete_user(self, user_id):
        self.delete_document(user_id)

    def user_run_query(self, conditions):
        return self.run_query(conditions)
    
    def user_run_or_query(self, or_conditions):
        return self.run_or_query(or_conditions)
    
    def get_all_users(self):
        print("Get all users")
        return self.get_all_values()
