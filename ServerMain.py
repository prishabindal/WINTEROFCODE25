import socket
import threading
import uuid
import tkinter as tk
from tkinter import scrolledtext
import json
import secrets
import ssl
import asyncio
from serverfunctions import server_vote_category, server_submit_vote_dropdown, server_registeration, server_login, server_logout
from datetime import datetime
import serverglobals
from firebase_config import initialize_firebase
from homomorphic_enctryption_S import encrypt, decrypt
import serverglobals

# Create a Tkinter window for the server
server_window = tk.Tk()
server_window.title("Secure Server")

# Create a scrolled text widget to display messages
text_area = scrolledtext.ScrolledText(server_window, width=50, height=20)
text_area.pack(padx=10, pady=10)

class SecureTokenServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.ssl_context = self.setup_ssl_context()
        self.server_socket = None  # Initialize to None
        # self.client_tokens = {}
        self.active_connections = {}  #

        #self.server_functions = ServerFunctions()  # Initialize ServerFunctions

    def setup_ssl_context(self):
        """
        Set up SSL context with certificate and key
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        return context

    def generate_unique_token(self):
        """
        Generate a secure, unique token for each client connection.
        """
        uuid_part = str(uuid.uuid4())
        random_part = secrets.token_hex(16)
        unique_token = f"{uuid_part}-{random_part}"
        return unique_token


    def handle_client(self, ssl_socket, client_address):
        """
        Handle individual client connections and token generation.
        """
        print("Inside handle_client")
        try:
            text_area.insert(tk.END, f"Secure connection established with {client_address}\n")
            text_area.yview(tk.END)
            self.active_connections[client_address] = ssl_socket #

            while True:
                try:
                    message = ssl_socket.recv(4096).decode('utf-8')
                
                    # print(message)
                    if not message:
                        print("failure")
                        break
                
                    json_data = json.loads(message)  # Parse JSON data
                    print(f"Received from client: {json_data}")
                 
                    print(json_data.get('action'))
                    print(json_data.get('data'))
                    
                    if json_data.get('action') == 'login':
                        print("entered if")
                       
                        if 'data' in json_data:
                            print(json_data['data'])
                            user= json_data['data'].get('username')
                            password= json_data['data'].get('password')

                            token = self.generate_unique_token()
                            server_login(token, json_data, client_address) 
                            #new token generated after login
                            
                            # self.client_tokens[client_address] = token
                            print(f"recieved user:{user} password:{password}")
                            response = {
                                'status': 'success',
                                'token': token,
                                'message': f'Message received and :{message}'
                               
                            }

                                    
                    elif json_data.get('action') == 'get_categories':
                        categories = []
                        if 'data' in json_data and json_data['data'].get('request_type') == 'fetch_categories':
                            categories = server_vote_category(self, token, json_data, client_address)
                        response = {
                            'status': 'success',
                            'categories': categories
                        }

                    elif json_data.get('action') == 'save_categories':
                        if 'data' in json_data and json_data['data'].get('request_type') == 'submit_categories':
                            selected_categories = server_vote_category(self, token, json_data, client_address)
                        
                   
                    

                    elif json_data.get('action') == 'get_selected_categories':
                        print("get_selected_cat")
                        selected_categories = []
    
                        if 'data' in json_data and json_data['data'].get('request_type') == 'create_dropdown':
                            try:
                                # Assuming you have a function to fetch selected categories
                                selected_categories = server_submit_vote_dropdown(self, token, json_data, client_address)
                                
                                response = {
                                    'status': 'success',
                                    'selected_categories': selected_categories
                                }
                            except Exception as e:
                                response = {
                                    'status': 'error',
                                    'message': f'Failed to fetch selected categories: {str(e)}'
                                }

                    elif json_data.get('action') == 'logout':
      
                        server_logout(token, json_data, client_address)
                        serverglobals.current_token=None
                        response = {
                            'status': 'success'
                        }

                    elif json_data.get('action') == 'register':
                        print("register elif")
                        server_registeration(self, json_data, client_address)
                        response = {
                                'status': 'success',
                                'token': "ABCD",
                        }
                    
                    elif json_data.get('action') == 'token':
                        token = self.generate_unique_token()
                        from user_session_info import UserSessionInfo
                        userSessionInfo = UserSessionInfo()
                        userSessionInfo.add_user_session(userId="FO2WL197An5ijRlZppZy",sessionUniqId=token)
                        # self.client_tokens[client_address] = token
                        response = {
                            'status': 'success',
                            'token': token,
                            'message': f'Message received and :{message}',
                            'public_key' : serverglobals.public_key,
                            'private_key': serverglobals.private_key
                        }
        
                    else:
                        # token = self.generate_unique_token()
                        # self.client_tokens[client_address] = token
                        response = {
                            'status': 'success',
                            'token': token,
                            'message': f'Message received and :{message}'
                        }
                
                    ssl_socket.send(json.dumps(response).encode('utf-8'))

                except json.JSONDecodeError:
                    response = {
                        'status': 'error',
                        'message': 'Invalid JSON format'
                    }
                    ssl_socket.send(json.dumps(response).encode('utf-8'))
                except Exception as e:
                    print(f"Error handling message: {e}")
                    break   
            #text_area.insert(tk.END, f"Token generated for {client_address}\n")
            #text_area.yview(tk.END)
               
        except Exception as e:
            text_area.insert(tk.END, f"Error with {client_address}: {str(e)}\n")
            text_area.yview(tk.END)   
      #  finally:
          #  ssl_socket.close()
          #  text_area.insert(tk.END, f"Connection closed with {client_address}\n")
           # text_area.yview(tk.END)

    async def handle_client_request(self, request, client_address):
        """Process client requests based on action type"""
        print("Inside handle_client_request")
        try:
            if request['action'] == 'get_categories':
                if request['data']['request_type'] == 'fetch_categories':
                    categories = await self.server_vote_category(request,client_address)
                    return {
                        'status': 'success',
                        'categories': categories
                    }
            elif request['action'] == 'request_token':
                token = self.generate_unique_token()
                self.client_tokens[client_address] = token
                return {
                    'status': 'success',
                    'token': token,
                    'message': 'Token generated successfully'
                }
            
            return {
                'status': 'error',
                'message': 'Invalid action'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def handle_login(self):
       '''
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
        
            if not username or not password:
                #messagebox.showerror("Error", "Please enter both username and password")
            return
            
            if ssl_socket:
            # Format the message with clear separation
            message = f"{username}:\n{password}\n"
            
            # Send credentials
            ssl_socket.send(message.encode('utf-8'))
            
            # Wait for server response
            try:
                response = ssl_socket.recv(1024).decode('utf-8')
                print(f"Server response: {response}")
                
                # Proceed with authentication
                self.authenticate_user()
            except Exception as e:
                print(f"Error receiving server response: {e}")
                messagebox.showerror("Error", "Failed to receive server response")
        else:
            messagebox.showerror("Connection Error", "No secure connection to server")
            
    except Exception as e:
        print(f"Error in handle_login: {e}")
        messagebox.showerror("Error", "Failed to process login request")
    '''
       
    def start_server(self):
        """
        Start the secure server and listen for client connections.
        """
        try:
            # Create and bind the socket only once
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Add this line to allow port reuse
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)

            text_area.insert(tk.END, f"Secure server started on {self.host}:{self.port}\n")
            text_area.insert(tk.END, "Waiting for secure connections...\n")
            text_area.yview(tk.END)

            while True:
                client_socket, client_address = self.server_socket.accept()
                ssl_socket = self.ssl_context.wrap_socket(
                    client_socket,
                    server_side=True
                )

                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(ssl_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except Exception as e:
            text_area.insert(tk.END, f"Server error: {str(e)}\n")
            text_area.yview(tk.END)

def main():
    server = SecureTokenServer()
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True
    server_thread.start()
    # Initializing DB
    initialize_firebase()
    
    def on_closing():
        try:
            if server.server_socket:
                server.server_socket.close()
        except:
            pass
        server_window.destroy()

    server_window.protocol("WM_DELETE_WINDOW", on_closing)
    server_window.mainloop()

if __name__ == '__main__':
    main()