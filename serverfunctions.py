import tkinter as tk
from tkinter import scrolledtext
#import bcrypt
import asyncio
from datetime import datetime
import serverglobals
from homomorphic_enctryption_S import decrypt, text_to_int



'''
# Create a Tkinter window for the server
server_window = tk.Tk()
server_window.title("Secure Voting Server")


# Create a scrolled text widget to display messages
text_area = scrolledtext.ScrolledText(server_window, width=50, height=20)
text_area.pack(padx=10, pady=10)
'''

def verify_token(self, token, client_address):
    """Verify if the provided token is valid for the client"""
    return (client_address in self.client_tokens and 
        self.client_tokens[client_address] == token)


def server_registeration(self, json_data, client_address):
    print("registering into db")
    from user_details import UserDetails
    userDetails = UserDetails()
    userDetails.add_user(json_data['data']['username'], json_data['data']['password'], 
                        json_data['data']['phoneNumber'], json_data['data']['firstName'])


def get_userid_from_token(token):
    from user_session_info import UserSessionInfo
    userSessionInfo = UserSessionInfo()
    session_data = userSessionInfo.user_session_run_query([
        ('SessionUniqId', '==', token)
        # ('SessionTerminated', '==', False)
    ])
    if session_data:
        return session_data[0]['UserId']
    
    else:
        return "no active"

def server_login(token, request_data, client_address):
    from user_details import UserDetails
    userDetails = UserDetails()
    decrypted_username = decrypt(request_data['data']['username'], serverglobals.public_key, serverglobals.private_key)
    decrypted_password = decrypt(request_data['data']['password'], serverglobals.public_key, serverglobals.private_key)
    print("login details from db:",decrypted_username,decrypted_password)
    userdata = userDetails.user_run_query([("UserName", "==", request_data['data']['username']),
                                ("Password", "==", request_data['data']['password'])])
    # userdata = userDetails.user_run_query([("UserId", "==", "fqWgjokotTLGQSwyUZvj")])
    # userdata = userDetails.user_run_query([("Username", "==", request_data['data']['username'])])

    print("data from db from Id fqWgjokotTLGQSwyUZvj")
    print(userdata)

    print(userdata[0]['Username'])
    # decrypted_username = decrypt(int(userdata[0]['Username']), serverglobals.public_key, serverglobals.private_key)
    print("decrypted username from db")
    print(decrypted_username, decrypted_password)
    
    # print(decrypted_username,decrypted_password)
    if len(userdata) != 1:
        print.error("Invalid credentials")

    from user_session_info import UserSessionInfo
    userSessionInfo = UserSessionInfo()
    # userSessionInfo.add_user_session(userId=userdata['UserId'],sessionUniqId=token)

def server_logout(token, request_data, client_address):
    from user_session_info import UserSessionInfo
    userSessionInfo = UserSessionInfo()
    session_data = userSessionInfo.get_user_session_by_sessionid(token)
    session_data['SessionEndDatetime'] = int(datetime.now().timestamp())
    session_data['SessionTerminated'] = True
    userSessionInfo.update_user_session(session_data)

    
def server_vote_category(self, token, request_data, client_address):
    """Handle vote category related actions"""
    print("Inside server_vote_category")
    try:
        if request_data['data']['request_type'] == 'fetch_categories':
            # Simulate async database operation
            #await asyncio.sleep(0.1)  
            print("request data sent")
            # Filter active categories
            from voting_categories import VotingCategory
            voting_category = VotingCategory()
            categories = voting_category.get_all_categories()
            print(categories)
            # for doc in categories:
            #     print(f'{doc.id} => {doc.to_dict()}')
            
            #     {
            #         'id': '1',
            #         'name': 'Technology',
            #         'description': 'Technology related topics'
            #     },
            #     {
            #         'id': '2',
            #         'name': 'Science',
            #         'description': 'Science related topics'
            #     },
            #     {
            #         'id': '3',
            #         'name': 'Arts',
            #         'description': 'Arts and culture'
            #     }
            
            return categories
              

        elif request_data['data']['request_type'] == 'submit_categories':
                        
            try:
                # Get selected categories from the client request
                categories = request_data['data'].get('selected_categories', [])
                print(categories)
                if not categories:
                    return {
                        'status': 'error',
                        'message': 'No categories provided'
                    }
                user_id = get_userid_from_token(token)
                # Save the selected categories for the client in a dictionary
             
                from user_preferences import UserPreferences
                userPreferences = UserPreferences()
                existingpref = userPreferences.get_user_pref_by_userid(user_id)
                if existingpref: 
                    existingpref[0]['VotCatId'] = categories
                    userPreferences.update_user_pref(existingpref[0])
                else:
                    userPreferences.add_user_pref(user_id, votcatId=categories)

                # Return a success response
                return {
                    'status': 'success',
                    'message': 'Categories submitted successfully',
                    'data': {'selected_categories': categories}
                }
                        
            
            except Exception as e:
                # Handle exceptions and return an error response
                return {
                    'status': 'error',
                    'message': f'Failed to submit categories: {str(e)}'
                }
    except Exception as e:
        print(f"Error in server_vote_category: {e}")
        return {'status': 'error', 'message': str(e)} 



async def handle_category_data(self, request_data, client_address):
    """
    Handle requests for detailed category data.
    Verifies user eligibility and returns category items for client display.
    """
    try:
        if request_data.get('request_type') == 'get_category_data':
            # Verify the user
            user_ref = self.db.collection('users').document(client_address)
            user_doc = user_ref.get()

            if not user_doc.exists:
                return {'status': 'error', 'error': 'User not found'}

            # Validate category name
            category_name = request_data.get('category')
            if not category_name:
                return {'status': 'error', 'error': 'Category not specified'}

            # Fetch user-selected categories
            user_data = user_doc.to_dict()
            user_categories = user_data.get('selected_categories', [])

            # Query the category by name
            categories_ref = self.db.collection('voting_categories')
            category_query = categories_ref.where('name', '==', category_name).limit(1).stream()
            category_doc = next(category_query, None)

            if not category_doc:
                return {'status': 'error', 'error': 'Category not found'}

            category_id = category_doc.id
            if category_id not in user_categories:
                return {'status': 'error', 'error': 'User not eligible for this category'}

            # Fetch active items in the category
            items_ref = self.db.collection('voting_categories').document(category_id).collection('items')
            items_query = items_ref.where('active', '==', True).stream()
            items_data = [
                {
                    'id': item.id,
                    'name': item_data.get('name', 'Unnamed Item'),
                    'description': item_data.get('description', ''),
                    'additional_info': item_data.get('additional_info', {})
                }
                for item in items_query
                for item_data in [item.to_dict()]
            ]

            # Check if voting is still open
            category_data = category_doc.to_dict()
            current_time = datetime.now()
            voting_end_time = category_data.get('voting_end_time')

            if voting_end_time and current_time > voting_end_time:
                return {'status': 'error', 'error': 'Voting period has ended for this category'}

            # Log access details
            self.db.collection('access_logs').add({
                'user_id': client_address,
                'category_id': category_id,
                'timestamp': current_time,
                'action': 'view_category_data'
            })

            return {
                'status': 'success',
                'data': items_data,
                'category_info': {
                    'name': category_data.get('name'),
                    'description': category_data.get('description'),
                    'voting_end_time': voting_end_time.isoformat() if voting_end_time else None
                }
            }

    except Exception as e:
        print(f"Error in handle_category_data: {str(e)}")  # Server-side logging
        return {'status': 'error', 'error': 'Failed to retrieve category data'}


def server_submit_vote_dropdown(self, token, request_data, client_address):
    """Handle vote submission actions"""
    print("server_submit_vote_dropdown")
    try:
        user_id = get_userid_from_token(token)
        if request_data['data']['request_type'] == 'create_dropdown':
            from user_preferences import UserPreferences
            userPreferences = UserPreferences()
            userpref = userPreferences.get_user_pref_by_userid(user_id)
            if len(userpref) != 1:
                print.error("User preference not found")
            selected_categories = userpref[0]['VotCatId']

            from voting_categories import VotingCategory
            voting_category = VotingCategory()
            categories = voting_category.get_all_categories()

            json_data = []
            for item in categories:
                if item['VotCatId'] in selected_categories:
                    print(f"Entry returned: {item}")
                    item['is_selected'] = True
                    json_data.append(item)
            print(json_data)
               
            return json_data
                
                          
    except Exception as e:
        return {'status': 'error', 'mes    sage': str(e)}


async def handle_category_data(self, request_data, client_address):
    """
    Handle category data retrieval requests with token verification.
    Returns detailed category data for display in client listbox.
    """
    try:
        # Verify the token first
        if request_data.get('verify_token'):
            user_ref = self.db.collection('users').document(client_address)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                return {
                    'status': 'error',
                    'error': 'User not found'
                }
            
            # Get the requested category
            category_name = request_data.get('category')
            if not category_name:
                return {
                    'status': 'error',
                    'error': 'Category not specified'
                }
            
            # Check if user is eligible for this category
            user_data = user_doc.to_dict()
            user_categories = user_data.get('selected_categories', [])
            
            # Find the category ID from name
            categories_ref = self.db.collection('voting_categories')
            category_query = categories_ref.where('name', '==', category_name).limit(1).stream()
            category_doc = next(category_query, None)
            
            if not category_doc:
                return {
                    'status': 'error',
                    'error': 'Category not found'
                }
            
            category_id = category_doc.id
            if category_id not in user_categories:
                return {
                    'status': 'error',
                    'error': 'User not eligible for this category'
                }
            
            # Get the category items/candidates
            items_ref = self.db.collection('voting_categories').document(category_id).collection('items')
            items_query = items_ref.where('active', '==', True).stream()
            
            # Format the data for client display
            items_data = []
            for item in items_query:
                item_data = item.to_dict()
                items_data.append({
                    'id': item.id,
                    'name': item_data.get('name', ''),
                    'description': item_data.get('description', ''),
                    'additional_info': item_data.get('additional_info', {})
                })
            
            # Check if voting is still open for this category
            category_data = category_doc.to_dict()
            current_time = datetime.now()
            voting_end_time = category_data.get('voting_end_time')
            
            if voting_end_time and current_time > voting_end_time:
                return {
                    'status': 'error',
                    'error': 'Voting period has ended for this category'
                }
            
            # Log the data access
            self.db.collection('access_logs').add({
                'user_id': client_address,
                'category_id': category_id,
                'timestamp': current_time,
                'action': 'view_category_data'
            })
            
            return {
                'status': 'success',
                'data': items_data,
                'category_info': {
                    'name': category_data.get('name'),
                    'description': category_data.get('description'),
                    'voting_end_time': voting_end_time.isoformat() if voting_end_time else None
                }
            }
            
    except Exception as e:
        print(f"Error in handle_category_data: {str(e)}")  # Server-side logging
        return {
            'status': 'error',
            'error': 'Failed to retrieve category data'
        }

async def server_handle_profile(self, request_data, client_address):
    """Handle profile related actions"""
    try:
        user_ref = self.db.collection('users').document(client_address)
          
        if request_data['request_type'] == 'fetch_profile':
            user_doc = user_ref.get()
            if user_doc.exists:
                profile_data = user_doc.to_dict()
                # Remove sensitive information
                profile_data.pop('password_hash', None)
                return {
                    'status': 'success',
                    'profile_data': profile_data
                }
                    
        elif request_data['request_type'] == 'update_profile':
            updated_data = request_data.get('profile_data', {})
            # Don't allow updating sensitive fields
            updated_data.pop('password_hash', None)
               
            user_ref.update(updated_data)
            return {
                'status': 'success',
                'message': 'Profile updated successfully'
            }
                
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    

async def handle_reset_password(self, request_data, client_address):
    """Handle password reset actions"""
    try:
        user_ref = self.db.collection('users').document(client_address)
        user_doc = user_ref.get()
          
        if not user_doc.exists:
            return {'status': 'error', 'message': 'User not found'}
               
        user_data = user_doc.to_dict()
        current_hash = user_data.get('password_hash')
        '''    
        # Verify current password
        if not bcrypt.checkpw(
            request_data['current_password'].encode(),
            current_hash.encode()
        ):
            return {'status': 'error', 'message': 'Current password is incorrect'}
                
        # Hash new password
        new_hash = bcrypt.hashpw(
            request_data['new_password'].encode(),
            bcrypt.gensalt()
        )
           
        # Update password in database
        user_ref.update({
           'password_hash': new_hash.decode(),
            'password_updated_at': datetime.now()
        })
        '''    
        return {
            'status': 'success',
            'message': 'Password updated successfully'
        }
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    

async def handle_logout(self, request_data, client_address):
        """Handle logout actions"""
        try:
            user_ref = self.db.collection('users').document(client_address)
            
            # Update last logout timestamp
            user_ref.update({
                'last_logout': datetime.now(),
                'is_active': False
            })
            
            return {
                'status': 'success',
                'message': 'Logged out successfully'
            }
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


async def handle_voting_history(self, request_data, client_address):
    """Handle voting history retrieval"""
    try:
        votes_ref = self.db.collection('votes')
        user_votes = votes_ref.where('user_id', '==', client_address).stream()
            
        history = []
        for vote in user_votes:
            vote_data = vote.to_dict()
            category_ref = self.db.collection('voting_categories').document(vote_data['category_id'])
            category_doc = category_ref.get()
                
            if category_doc.exists:
                category_name = category_doc.to_dict().get('name')
                history.append({
                    'category': category_name,
                    'vote_timestamp': vote_data['timestamp'].isoformat(),
                    'selection': vote_data['selection']
                })
            
        return {
            'status': 'success',
            'user_voting_history': history
        }
            
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def handle_request(self, request, client_address):
    """Main request handler that routes to specific handlers"""
    try:
        action = request.get('action')
        data = request.get('data', {})
            
        handlers = {
            'vote_category': self.handle_vote_category,
            'submit_vote': self.handle_submit_vote,
            'profile': self.handle_profile,
            'reset_password': self.handle_reset_password,
            'logout': self.handle_logout,
            'history': self.handle_voting_history
        }
            
        if action in handlers:
            return handlers[action](data, client_address)
        else:
            return {
                'status': 'error',
                'message': f'Unknown action: {action}'
            }
                
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Request handling error: {str(e)}'
        }


