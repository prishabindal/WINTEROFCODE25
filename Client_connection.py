import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import ssl
import re
import json
from client import VotingSystem, logout_message
import Globals  # Import the globals module
from homomorphic_enctryption_S import encrypt, decrypt
import base64



# Global variable for SSL socket
#global ssl_socket 
#ssl_socket= None




# Function to connect to the server
def connect_to_server():
    #global ssl_socket
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Globals.ssl_socket = context.wrap_socket(
            client_socket,
            server_hostname='localhost'
        )
        Globals.ssl_socket.connect(('localhost', 12345))
        
        print("Connected securely to the server...")
        if Globals.ssl_socket:
            data= {}
            response = Globals.client.send_json_request("token", data)
                  
            if not response:
                messagebox.showerror("Error", "Failed to retrieve token")
                return
            
            Globals.current_token = response.get('token', [])
            Globals.public_key = response.get('public_key', [])
            Globals.private_key = response.get('private_key', [])
        
        else:
            messagebox.showerror("Connection Error", "No secure connection to server")


    except Exception as e:
        print(f"Error connecting to server: {e}")
        messagebox.showerror("Connection Error", "Failed to establish secure connection to server.")

#def on_button_click(button_name):
    #messagebox.showinfo("Button Clicked", f"You clicked on {button_name}")

def on_button_click(button_name):
    
    try:    
        if Globals.ssl_socket:
                       
            message=f"{button_name} button clicked"
            Globals.ssl_socket.send(json.dumps(message).encode('utf-8'))

            respose = Globals.ssl_socket.recv(4096).decode()
            
            if respose:
                json_data = json.loads(respose)  # Parse JSON data
                print(f"Received from client: {json_data}")

        else:
            messagebox.showerror("Connection Error", "No secure connection to server")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")


'''
    userid = "JohnDoe@firebase"
    try:
        fetch_profile_data(content_frame, userid)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch profile data: {e}")
'''


# New function to handle login
def handle_login(username_entry, password_entry):
    user = username_entry.get()
    password = password_entry.get()
    encrypted_user = encrypt(user, Globals.public_key)
    encrypted_password = encrypt(password, Globals.public_key)
    try:
        if Globals.ssl_socket:
            print("entered ssl socket")
            # Send the credentials to server
            #credentials = f"{username}:\n{password}\n"
            data= {"username": encrypted_user, "password":encrypted_password}
            print(data)
            response = Globals.client.send_json_request("login", data)
            
            #Globals.ssl_socket.send(json.dumps(message).encode('utf-8'))
            #message =  json.dumps(credentials).encode('utf-8')
            #print(message)
            #Globals.ssl_socket.send(message)
                              
            if not response:
                messagebox.showerror("Error", "Login Failed, please enter correct username and password")
                return
            
            Globals.current_token = response.get('token', [])
           
            if response and response.get('status') == 'success':
                messagebox.showinfo("Success", "logged in successfully")
                clear_content_frame()
            else:   
                messagebox.showerror("Error", "Failed to login")
            # Get server response
            #response = Globals.ssl_socket.recv(1024).decode()
            #print(f"Server received credentials for user: {username}", response)
            
            # Call the original authenticate_user function
           # authenticate_user()
        else:
            messagebox.showerror("Connection Error", "No secure connection to server")
    except Exception as e:
        print(f"Error sending credentials to server: {e}")
        messagebox.showerror("Error", "Failed to send credentials to server")

def handle_register():
    clear_content_frame()
    # Create a frame for the registration form
    register_frame = tk.Frame(Globals.content_frame)
    register_frame.pack(padx=20, pady=20)

    # Create and pack form fields
    fields = {
        'Username': tk.StringVar(),
        'Password': tk.StringVar(),
        # 'Email': tk.StringVar(),
        'Phone': tk.StringVar(),
        'First Name': tk.StringVar()

    }

    # Create labels and entry fields
    for i, (label_text, var) in enumerate(fields.items()):
        # Label
        tk.Label(register_frame, text=label_text).grid(row=i, column=0, padx=5, pady=5, sticky='e')
        
        # Entry field
        entry = tk.Entry(register_frame, textvariable=var)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='w')
        
        # Make password field secure
        if label_text == 'Password':
            entry.config(show='*')
    def submit_registration():
        # Collect form data

        data = {
            'firstName': fields['First Name'].get(),
            'username': encrypt(fields['Username'].get(),Globals.public_key),
            'password': encrypt(fields['Password'].get(),Globals.public_key),
            # 'email':encrypt(fields['Email'].get(),Globals.public_key),
            'phoneNumber': encrypt(fields['Phone'].get(), Globals.public_key)
        }
        # data = {
        #     'firstName': "'"+encrypt(fields['First Name'].get(), Globals.public_key)+"'",
        #     'username': "'"+encrypt(fields['Username'].get(),Globals.public_key)+"'",
        #     'password': "'"+encrypt(fields['Password'].get(),Globals.public_key)+"'",
        #     'email': "'"+encrypt(fields['Email'].get(),Globals.public_key)+"'",
        #     'phoneNumber': "'"+encrypt(fields['Phone'].get(), Globals.public_key)+"'"
        # }

       
        # Basic validation
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Email validation
        # if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        #     messagebox.showerror("Error", "Invalid email format!")
        #     return

        # # Phone validation
        # if not data['phoneNumber'].replace('-', '').replace('+', '').isdigit():
        #     messagebox.showerror("Error", "Invalid phone number!")
        #     return

        # Send registration data to server
        response = Globals.client.send_json_request('register', data)

        if response and response.get('status') == 'success':
            messagebox.showinfo("Success", "Registration successful!")
            # Clear the form
            # for var in fields.values():
            #     var.set('')
            clear_content_frame()
            show_login_content()
        else:
            messagebox.showerror("Error", f"Registration failed: {response.get('message', 'Unknown error')}")

    # Submit button
    submit_btn = tk.Button(
        register_frame,
        text="Submit Registration",
        command=submit_registration
    )
    submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)


def create_home_page():
    print("creating home page")
    
    root.title("Home Page")
    root.geometry("600x700")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)

    left_nav_frame = tk.Frame(root, bg="#E0E0E0", width=120)
    left_nav_frame.grid(row=0, rowspan=2, column=0, sticky="nsew")
    left_nav_frame.grid_propagate(False)
    
    
    
    left_buttons = [
        {"name": "Home", "command": lambda: on_button_click("Home")},
        {"name": "Reset Password", "command": lambda: on_button_click("Reset Password")},
        {"name": "Vote Category", "command": lambda: Globals.client.vote_category_view()},
        {"name": "Submit Vote", "command": lambda: Globals.client.get_selected_categories()},
        {"name": "History", "command": lambda: on_button_click("History")},
    ]

    for idx, btn in enumerate(left_buttons):
        btn_widget = tk.Button(
            left_nav_frame,
            text=btn["name"],
            command=btn["command"],
            bg="#FFFFFF",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            width=12
        )
        btn_widget.grid(row=idx, column=0, sticky="ew", padx=5, pady=15)

    right_nav_frame = tk.Frame(root, bg="white", width=100)
    right_nav_frame.grid(row=0, rowspan=2, column=2, sticky="nsew")
    right_nav_frame.grid_propagate(False)

    right_buttons = [
        {"name": "Profile", "command": lambda: on_button_click("Profile")},
        {"name": "Log Out", "command": lambda: logout_message()},
        {"name": "About", "command": lambda: on_button_click("About")},
    ]

    for idx, btn in enumerate(right_buttons):
        btn_widget = tk.Button(
            right_nav_frame,
            text=btn["name"],
            command=btn["command"],
            bg="#E0E0E0",
            font=("Helvetica", 10),
            relief=tk.FLAT,
            width=10
        )
        btn_widget.grid(row=idx, column=0, sticky="ew", padx=5, pady=15)
    
    #content_frame
    Globals.content_frame = tk.Frame(root, bg="white")
    Globals.content_frame.grid(row=1, column=1, sticky="nsew")

    show_login_content()
    # content_label = tk.Label(
    #     content_frame,
    #     text="Secure Voting!",
    #     font=("Helvetica", 14),
    #     bg="white",
    # )
    # content_label.pack(pady=20)

    # username_label = tk.Label(content_frame, text="Username:")
    # username_label.pack(anchor='w')
    # username_entry = tk.Entry(content_frame, width=30)
    # username_entry.pack(pady=(0, 10))

    # password_label = tk.Label(content_frame, text="Password:")
    # password_label.pack(anchor='w')
    # password_entry = tk.Entry(content_frame, show="*", width=30)
    # password_entry.pack(pady=(0, 10))

    # # Modified login button command to use the new handle_login function
    # login_button = tk.Button(
    #     content_frame, 
    #     text="Login", 
    #     command=lambda: handle_login(username_entry, password_entry)
    # )
    # login_button.pack(pady=5)

    # register_button = tk.Button(content_frame, text="Register", command=lambda: handle_login(username_entry, password_entry)
    # )
    # register_button.pack(pady=5)

    root.mainloop()




def show_login_content():
    #clear_content_frame()
    # global content_frame
    print("show_login_content")
    content_label = tk.Label(
        Globals.content_frame,
        text="Secure Voting!",
        font=("Helvetica", 14),
        bg="white",
    )
    content_label.pack(pady=20)
    
    username_label = tk.Label(Globals.content_frame, text="Username:")
    username_label.pack(anchor='w')
    username_entry = tk.Entry(Globals.content_frame, width=30)
    username_entry.pack(pady=(0, 10))
    
    password_label = tk.Label(Globals.content_frame, text="Password:")
    password_label.pack(anchor='w')
    password_entry = tk.Entry(Globals.content_frame, show="*", width=30)
    password_entry.pack(pady=(0, 10))
    
    login_button = tk.Button(
        Globals.content_frame,
        text="Login",
        command=lambda: handle_login(username_entry, password_entry)
    )
    login_button.pack(pady=5)
    
    register_button = tk.Button(
        Globals.content_frame,
        text="Register",
        command=lambda: handle_register()
    )
    register_button.pack(pady=5)

def clear_content_frame():
    print("clearing content frame")
    # Destroy all widgets in content_frame
    #global content_frame
    for widget in Globals.content_frame.winfo_children():
        widget.destroy()

def show_vote_category_content(categories):
    print("show_vote_category_content")
    #global content_frame
    clear_content_frame()
    
    
    # Add your new content here
    title_label = tk.Label(
        Globals.content_frame,
        text="Vote Categories",
        font=("Helvetica", 14),
        bg="white"
    )
    title_label.pack(pady=20)

    if not categories:
        ttk.Label(
            Globals.content_frame,
            text="No categories available",
            font=("Helvetica", 12)
        ).pack(pady=20)
        return
    
    category_vars = {}
    for category in categories:
        var = tk.BooleanVar(value=category.get('is_selected', False))
        category_vars[category['VotCatId']] = var

        category_label = ttk.Label(
            Globals.content_frame,
            text=category['VotCatDesc'],
            wraplength=400,
            font=("Helvetica", 10)
        )
        ttk.Checkbutton(
            Globals.content_frame,
            text=category['VotCatName'],
            variable=var
        ).pack(anchor=tk.W, pady=2)
        category_label.pack(anchor=tk.W, padx=20, pady=(0, 10))
    
    ttk.Button(
        Globals.content_frame,
        text="Submit",
        command=lambda: Globals.client.vote_category_submit()     
    ).pack(pady=10)                                         
    return category_vars
 
def main():
    global root
    
    root = tk.Tk()
    Globals.client = VotingSystem(root)
    # Connect to the server in the background
    connect_to_server()

    # Create the home page
    create_home_page()

if __name__ == '__main__':
    main()