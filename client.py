import tkinter as tk
from tkinter import ttk
import threading
import ssl
import json
from datetime import datetime
from tkinter import messagebox
import Globals  # Import the globals module

# from homomorphic_enctryption_S import generate_paillier_keys, encrypt
#ssl_socket = None

# global content_frame
# content_frame = tk.Frame(bg="white")
# content_frame.grid(row=1, column=1, sticky="nsew")

class VotingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Voting System")
        self.auth_token = None  # Store authentication token
        self.selected_categories = []
        self.current_frame = None
        
    def create_main_frame(self):
        """Create and return main container frame"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = ttk.Frame(self.root, padding="10")
        self.current_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        return self.current_frame
    
    

    def vote_category_view(self):
        """Display available voting categories"""
        print("inside vote_category_view")
        
        #clear_content_frame()

        #frame = self.create_main_frame()
        
        # Get categories from server
        response = self.send_json_request("get_categories", {'request_type': 'fetch_categories'})
      
        if not response:
            messagebox.showerror("Error", "Failed to retrieve categories")
            return
        
        categories = response.get('categories', [])
        
       #
        # Create category selection area with a scroll frame
        # category_frame = ttk.Frame(frame)
        # category_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        # # Create checkboxes for categories
        print("before import")
        from Client_connection import  show_vote_category_content
        print("after import")
        self.category_vars = show_vote_category_content(categories)
        # for category in response['categories']:
        #     var = tk.BooleanVar(value=category.get('is_selected', False))
        #     self.category_vars[category['id']] = var

        #     category_label = ttk.Label(
        #         category_frame,
        #         text=category['description'],
        #         wraplength=400,
        #         font=("Helvetica", 10)
        #     )
        #     ttk.Checkbutton(
        #         frame,
        #         text=category['name'],
        #         variable=var
        #     ).pack(anchor=tk.W, pady=2)
        #     category_label.pack(anchor=tk.W, padx=20, pady=(0, 10))
        
        # ttk.Button(
        #     frame,
        #     text="Submit",
        #     command=self.vote_category_submit
        # ).pack(pady=10)

    
        
    def vote_category_submit(self):
        print("inside vote category submit")
        """Save selected categories to database"""
        selected = [
            cat_id for cat_id, var in self.category_vars.items()
            if var.get()
        ]
        
        response = self.send_json_request("save_categories", {
            "request_type": 'submit_categories',
            "selected_categories": selected
        })
        
        if response and response.get('status') == 'success':
            messagebox.showinfo("Success", "Categories saved successfully")
            from Client_connection import clear_content_frame
            clear_content_frame()
            # self.submit_vote_category()
        else:
            messagebox.showerror("Error", "Failed to save categories")
    
    def get_selected_categories(self):
        print("Inside get_selected_categories")
        from Client_connection import clear_content_frame
        clear_content_frame()
        """Display dropdown button for selected voting categories."""
        #frame = self.create_main_frame()

        # Get user's selected categories
        response = self.send_json_request("get_selected_categories", {
            "request_type": 'create_dropdown'
        })
        
        selected_categories = response.get('selected_categories', [])
        print(selected_categories)

        if not response or response.get('status') != 'success':
            messagebox.showerror("Error", "Failed to retrieve selected categories")
            return
        
        # Initialize the selected_category attribute
        self.selected_category = tk.StringVar(value="Select Category")
        # Create a label for the dropdown button
        ttk.Label(Globals.content_frame, text="Select Category:").pack(anchor=tk.W, pady=5)
        print(selected_categories)
        # Create a menu for the dropdown button
        dropdown_menu = tk.Menu(Globals.content_frame, tearoff=0)
        for cat in selected_categories:
            dropdown_menu.add_command(
                label=cat['VotCatName'],
                command=lambda category=cat['VotCatName']: self.select_category(category)
            )

        # Create the dropdown button
        dropdown_button = ttk.Button(
            Globals.content_frame,
            textvariable=self.selected_category,
            command=lambda: dropdown_menu.post(
                dropdown_button.winfo_rootx(),
                dropdown_button.winfo_rooty() + dropdown_button.winfo_height()
            )
        )
        dropdown_button.pack(pady=10)

    def select_category(self, category):
        """Handle category selection from the dropdown."""
        self.selected_category.set(category)
        
        print(f"Selected category: {category}")
        response = self.send_json_request("get_voting_details", {
            "request_type": 'get_voting_details',
            "category": category
        })

        self.selected_detail = tk.StringVar()

        category_details = response.get('category_details', [])
        if len(category_details) == 0:
            messagebox.showwarning("Warning", "No voting detail available for this category ")

        # details_vars = {}
        # for details in category_details:
        #     var = tk.BooleanVar(value=category.get('is_selected', False))
        #     details_vars[category['VotCatId']] = var

        # Create label for the section
        ttk.Label(Globals.content_frame, text=f"Details for {category}:").pack(anchor='w')
        
        # Create radio buttons for each option in the response
        
        for details in category_details:
            ttk.Radiobutton(
                Globals.content_frame,
                text=details['VotDtlsName'],
                value=details['VotDtlsId'],
                variable=self.selected_detail,
                command=self.handle_detail_selection
            ).pack(anchor='w', pady=2)
        ttk.Button(
            Globals.content_frame,
            text="Submit",
            command=lambda: self.submit_vote_ok()     
        ).pack(pady=10)                                         
        
        
    def handle_detail_selection(self):
        """Handle when a radio button option is selected."""
        selected_value = self.selected_detail.get()
        print(f"Selected detail: {selected_value}")
            

      
    def submit_vote_ok(self):
        """Display voting options for selected category"""
        if not self.selected_detail.get():
            messagebox.showwarning("Warning", "Please select a voting detail")
            return
          
       
        # Get voting options for selected category
        response = self.send_json_request("get_voting_options", {
                        "voting_detail": self.selected_detail.get()
        })
        
        if not response or response.get('status') != 'success':
            messagebox.showerror("Error", "Failed to retrieve voting options")
            return
        voting_options = response.get('voting_options',[])
        # Create radio buttons for options
        self.selected_option = tk.StringVar()
        for option in voting_options:
            ttk.Radiobutton(
                Globals.content_frame,
                text=option['VotDtlsOptionName'],
                value=option['VotDtlsOptionId'],
                variable=self.selected_option
            ).pack(anchor=tk.W, pady=2)
        
        ttk.Button(
            Globals.content_frame,
            text="Submit Vote",
            command=self.submit_vote_submit
        ).pack(pady=10)
    
    def submit_vote_submit(self):
        """Submit final vote"""
        if not self.selected_option.get():
            messagebox.showwarning("Warning", "Please select an option")
            return
        
        response = self.send_json_request("submit_vote", {
                    "selected_option": self.selected_option.get()
        })
        
        if response and response.get('status') == 'success':
            messagebox.showinfo("Success", "Vote submitted successfully")
            from Client_connection import clear_content_frame
            clear_content_frame()
        else:
            messagebox.showerror("Error", "Failed to submit vote")
    
    
    def send_json_request(self,action, data):

        print(f"Action: {action}")
        print(f"Checking Globals.ssl_socket: {Globals.ssl_socket}")
        print(f"Type of Globals.ssl_socket: {type(Globals.ssl_socket)}")
        print(f"Globals.ssl_socket._closed: {getattr(Globals.ssl_socket, '_closed', 'Attribute not found')}")

        try:
            if Globals.ssl_socket:
                print("Socket is open and connected.")

                # encrypted_data = {k: str(Globals.paillier_public_key.encrypt(v)) for k, v in data.items()}
                # print(f"Encrypted Data: {encrypted_data}")

                request = {
                    "action": action,
                    "token": Globals.current_token,
                    "client_address": Globals.ssl_socket.getsockname()[0],
                    "timestamp": datetime.now().isoformat(),
                    "data": data
                }
                print("Preparing to send data...")
                # Globals.ssl_socket.send(json.dumps(request).encode('utf-8'))
                Globals.ssl_socket.send(json.dumps(request).encode())
                print("Data sent successfully.")

                print("Waiting for response...")
                response = Globals.ssl_socket.recv(4096).decode()
                print(f"Raw response: {response}")



                return json.loads(response) if response else None
               
            else:
                print("Socket is None or invalid.")
                messagebox.showerror("Connection Error", "No secure connection to server")
                return None
        except Exception as e:
            print(f"Exception occurred: {e}")
            messagebox.showerror("Error", f"Failed to send request: {e}")
            return None

        '''

        message=f"Called from : {action}"
        
        """Generic function to send JSON requests to server"""
        
        if Globals.ssl_socket:
            print("Socket is open and connected.")
        else:
            print("Socket is either None or closed.")

        if Globals.ssl_socket:
            
            #print(f"Globals.ssl_socket: {Globals.ssl_socket}")

            #messagebox.showerror("Inside Socketr", "Sending data to server2")
            request = {
                "action": action,
                "token":Globals.current_token,
                "client_address": Globals.ssl_socket.getsockname()[0],
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            Globals.ssl_socket.send(json.dumps(request).encode('utf-8'))

            response = Globals.ssl_socket.recv(1024).decode()
            print(response)
            return json.loads(response) if response else None
            
        else:
            messagebox.showerror("Connection Error", "No secure connection to server")
            return None

        #except Exception as e:
         #   messagebox.showerror("Error", f"Failed to send request: {e}")
          #  return None

        '''

'''       
def client_vote_category_view(main_frame): #vote category

    response = send_json_request("vote_category", {
        "request_type": "fetch_categories"
    })
    if not response and 'categories' in response:
        messagebox.showerror("Error", "Failed to fetch categories")
        return
    
  
    # Create main window
    vote_window = tk.Toplevel()
    vote_window.title("Vote Categories")
    vote_window.geometry("400x500")
    

    # Create scrollable frame
    container = tk.Frame(vote_window)
    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Create checkboxes for categories
    checkboxes = {}
    for category in response['categories']:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(scrollable_frame, text=category['name'], variable=var)
        cb.pack(anchor="w", padx=10, pady=5)
        checkboxes[category['id']] = var
    
    container.pack(fill="both", expand=True, padx=10, pady=10)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def client_vote_category_submit():
        selected = [cat_id for cat_id, var in checkboxes.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one category")
            return
            
        submit_response = send_json_request("vote_category", {
            "request_type": "submit_categories",
            "selected_categories": selected
        })
        
        if submit_response and submit_response.get('status') == 'success':
            vote_window.destroy()
            messagebox.showinfo("Success", submit_response.get('message', "Categories submitted successfully"))


        else:
            messagebox.showerror("Error", "Failed to submit categories")
    
    # Submit button
    submit_button = tk.Button(vote_window, text="Submit", command=client_vote_category_submit)
    submit_button.pack(pady=10)
    # Here you would typically update the UI with the categories
    # display voting categories with checkboxes and create a submit button to call the fn client_vote_category_submit()

  
def client_vote_category_submit():
        """Handle submission of selected categories"""
 
    selected_categories = []
    for category, var in category_vars.items():
        if var.get():
            selected_categories.append(category)
        
        # Here you can call your API or handle the selected categories
    print(f"Selected categories: {selected_categories}")
    window.destroy()
    
    if response and 'categories' in response:
        # Create main window
        window = tk.Tk()
        window.title("Vote Categories")
        window.geometry("400x500")
        
        # Create frame for categories
        frame = ttk.Frame(window, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create label
        ttk.Label(frame, text="Select Categories:").grid(row=0, column=0, pady=10)
        
        # Create checkboxes for each category
        category_vars = {}
        for i, category in enumerate(response['categories']):
            var = tk.BooleanVar()
            category_vars[category] = var
            ttk.Checkbutton(
                frame, 
                text=category,
                variable=var
            ).grid(row=i+1, column=0, sticky=tk.W, pady=2)
        
        # Create submit button
        ttk.Button(
            frame,
            text="Submit",
            command=client_vote_category_submit
        ).grid(row=len(response['categories'])+1, column=0, pady=20)
 '''       

    


'''

def client_submit_vote_category(main_frame):
    response = send_json_request("submit_vote", {"request_type": "create_dropdown"})
    
    if not response:
        messagebox.showerror("Error", "Failed to fetch categories")
        return
        
    # Clear main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
        
    # Create label and dropdown
    tk.Label(main_frame, text="Select Voting Category").pack(pady=10)
    
    category_var = tk.StringVar()
    dropdown = ttk.Combobox(main_frame, textvariable=category_var)
    dropdown['values'] = [cat['name'] for cat in response.get('categories', [])]
    dropdown['state'] = 'readonly'
    dropdown.pack(pady=5)
    
    def on_select(event):
        selected = category_var.get()
        if selected:
            client_vote_category_submit(main_frame, selected)
    
    dropdown.bind('<<ComboboxSelected>>', on_select)
'''
'''   
def client_submit_vote_dropdown(ssl_socket, root):
    def on_fetch():
        try:
            # Disable button and fetch data
            fetch_button.state(['disabled'])
            response = send_json_request("fetch_data", {})
            #request = json.dumps({"select vote category": "fetch_categories"})
            if response and response.get('data'):
                dropdown['values'] = response['data']
                if response['data']:
                    dropdown.set(response['data'][0])
            #ssl_socket.send(request.encode())
            #response = ssl_socket.recv(4096).decode()
            #data = json.loads(response)
            
            # Update dropdown with received data
            #dropdown['values'] = data
            #if data:
            #    dropdown.set(data[0])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            fetch_button.state(['!disabled'])

    # Create GUI elements
    dropdown = ttk.Combobox(root, state="readonly")
    dropdown.pack(pady=10)
    
    fetch_button = ttk.Button(root, text="Fetch Data", command=on_fetch)
    fetch_button.pack(pady=5)
    
    return dropdown, fetch_button

    response = send_json_request("select vote category", {"request_type": "fetch_categories"})

    if response and 'categories' in response:
        pass 
    
    #show the eligible vote categories for the selected user in a dropdown with click option on any one of them + a submit button to call 
    # the fn client_submit_vote_ok() 
'''

'''
def client_submit_vote_dtls(category):

    """
    Send request to verify token, get category data and display it with single selection option.
    Returns the selected item.
    """
    try:
        # Get data from server
        response = send_json_request("get_category_data", {
            "category": category,
            "verify_token": True
        })
        
        if not response or 'error' in response:
            messagebox.showerror("Error", response.get('error', "Failed to retrieve data"))
            return None
            
        # Setup display window
        display_window = tk.Toplevel()
        display_window.title(f"{category} Selection")
        display_window.geometry("400x300")
        
        selected_item = tk.StringVar()
        listbox = tk.Listbox(display_window, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add data to listbox
        for item in response.get('data', []):
            listbox.insert(tk.END, item['name'])
            
        def on_select():
            if listbox.curselection():
                selected_item.set(listbox.get(listbox.curselection()))
                display_window.destroy()
                
        tk.Button(display_window, text="Select", command=on_select).pack(pady=10)
        display_window.wait_window()
        return selected_item.get()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process category data: {e}")
        return None
'''   
'''
def client_submit_vote_ok(display_frame):
    try:
        # Verify token
        verify_response = send_json_request("verify_token", {"verify": True})
        if not verify_response or verify_response.get('status') != 'success':
            messagebox.showerror("Error", "Token verification failed")
            return
            
        # Get selection
        selected_option = client_submit_vote_dtls("your_category")
        if not selected_option:
            return
            
        # Send selection to server
        submission_response = send_json_request("submit_selection", {
            "selected": selected_option
        })
        
        if not submission_response:
            messagebox.showerror("Error", "Failed to submit selection")
            return
            
        # Clear frame
        for widget in display_frame.winfo_children():
            widget.destroy()
            
        # Create listbox for response data
        listbox = tk.Listbox(display_frame, selectmode=tk.SINGLE)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Populate response data
        for item in submission_response.get('data', []):
            listbox.insert(tk.END, item['name'])
         
        def client_submit_vote_submit():
            if listbox.curselection():
                selected = listbox.get(listbox.curselection())
                # Handle final selection here
                print(f"Final selection: {selected}")
              
        submit_btn = tk.Button(display_frame, text="Submit", command=client_submit_vote_submit)
        submit_btn.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Operation failed: {e}")
'''
'''
def client_submit_vote_submit(display_frame, selected_option):
    try:
        verify_response = send_json_request("verify_token", {"verify": True})
        if not verify_response or verify_response.get('status') != 'success':
            messagebox.showerror("Error", "Token verification failed")
            return
            
        final_response = send_json_request("final_submit", {
            "final_selection": selected_option
        })
        
        if not final_response:
            messagebox.showerror("Error", "Failed to submit final selection")
            return
            
        for widget in display_frame.winfo_children():
            widget.destroy()
            
        message_label = tk.Label(display_frame, text=final_response.get('message', "Submission completed"))
        message_label.pack(pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Final submission failed: {e}")
'''


def client_profile_view(main_frame):
    """Handle Profile button click"""
    response = send_json_request("profile", {
        "request_type": "fetch_profile"
    })
    if not response:
        messagebox.showerror("Error", "Failed to fetch profile")
        return
        
    # Clear main frame
    for widget in main_frame.winfo_children():
        widget.destroy()
        
    # Create profile display
    #profile_frame = tk.Frame(main_frame)
    #rofile_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Display profile data
    for field, value in response.get('profile_data', {}).items():
        #label = tk.Label(main_frame), text=f"{field}: {value}"
        label.pack(anchor="w", pady=5)
    
    button_frame = tk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Edit Profile", command=client_profile_edit).pack(side="left", padx=5)
        # Here you would typically update the UI with the profile data
       # pass

def client_profile_edit(main_frame):
        
    # Clear profile display
        for widget in main_frame.winfo_children():
            widget.destroy()
            
        # Create edit fields
        edit_frame = tk.Frame(main_frame)
        edit_frame.pack(pady=20, padx=20)
        
        entries = {}
        for field, value in response.get('profile_data', {}).items():
            tk.Label(edit_frame, text=field).pack(anchor="w")
            entry = tk.Entry(edit_frame)
            entry.insert(0, value)
            entry.pack(anchor="w", pady=5)
            entries[field] = entry

        tk.Button(edit_frame, text="Submit", command=client_profile_submit).pack(pady=10)

def client_profile_submit(main_frame):
    updated_data = {field: entry.get() for field, entry in entries.items()}
    submit_response = send_json_request("profile", {
        "request_type": "update_profile",
        "profile_data": updated_data
    })
            
    if submit_response and submit_response.get('status') == 'success':
        messagebox.showinfo("Success", "Profile updated successfully")
        client_profile_view(main_frame)
    else:
        messagebox.showerror("Error", "Failed to update profile")

    

def client_reset_password(main_frame): #reset password

    """Handle Reset Password button click"""
    response = send_json_request("reset_password", {
        "request_type": "password_reset_initiation"
    })
    if not response:
        messagebox.showerror("Error", "Failed to fetch profile")
        return
    
    # Clear main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Create edit fields
    edit_frame = tk.Frame(main_frame)
    edit_frame.pack(pady=20, padx=20)

    # Create the "Current Password" field
    tk.Label(edit_frame, text="Current Password").pack(anchor="w")
    current_password_entry = tk.Entry(edit_frame, show="*")  # 'show' masks the input
    current_password_entry.pack(anchor="w", pady=5)

    # Create the "New Password" field
    tk.Label(edit_frame, text="New Password").pack(anchor="w")
    new_password_entry = tk.Entry(edit_frame, show="*")  # 'show' masks the input
    new_password_entry.pack(anchor="w", pady=5)


    tk.Button(edit_frame, text="Submit", command=client_reset_password_ok).pack(pady=10)

def client_reset_password_ok():
    try:
        # Step 1: Validate input fields
        current_password = current_password_entry.get()
        new_password = new_password_entry.get()

        if not current_password or not new_password:
            messagebox.showerror("Input Error", "Both fields are required!")
            return

        # Step 2: Prepare the data and send the reset request
        password_data = {
            "current_password": current_password,
            "new_password": new_password
        }
        password_response = send_json_request("reset_password", password_data)

        # Step 3: Handle the server response
        if password_response and password_response.get("status") == "success":
            messagebox.showinfo("Success", "Password reset successfully!")

            # Clear the edit_frame
            for widget in edit_frame.winfo_children():
                widget.destroy()
        else:
            error_message = password_response.get("error", "Password reset failed")
            messagebox.showerror("Reset Failed", f"Error: {error_message}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
  
def logout_message(): #logout

    """Handle Log Out button click"""
    # #global current_token
    # response = Globals.client.send_json_request("logout", {
    #     "logout_request": "user_initiated"
    # })

    # if response and response.get("status") == "success":
    #     # Show confirmation dialog
    confirm = messagebox.askyesno("Logout Confirmation", "Are you sure you want to log out?")

    if confirm:  # If the user clicks "Yes"
            messagebox.showinfo("Logged Out", "You have been successfully logged out!")
            # Additional cleanup actions (if needed)
            response = Globals.client.send_json_request("logout", {
                "logout_request": "user_initiated"
            })

            if response and response.get("status") == "success":
                Globals.current_token = None  # Clear the token or handle session reset
                from Client_connection import clear_content_frame, show_login_content
                clear_content_frame()
                show_login_content()

    else:  # If the user clicks "No"
        messagebox.showinfo("Cancelled", "Logout cancelled.")

    # else:
    #         error_message = response.get("error", "Unable to verify token for logout.")
    #         messagebox.showerror("Logout Failed", f"Error: {error_message}")
    
 
def client_home_button(): #home

    """Handle Home button click"""
    response = send_json_request("home", {
        "page_access": "home_page"
    })
    if response and response.get("status") == "success":
        messagebox.showinfo("Home", "Welcome to the Home Page")
        #instead load the home page
    else:
       messagebox.showinfo("error", "could not go to home") 

def client_about(): #about
    
    """Handle About button click"""
    response = send_json_request("about", {
        "page_access": "about_page"
    })
    if response:
        messagebox.showinfo("About", "Secure Voting System v1.0")
        #print the about page

def client_user_voting(main_frame): #history

    """Handle History button click"""
    response = send_json_request("history", {
        "request_type": "fetch_voting_history"
    })
    if response and 'history' in response:
                
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Display data
        for field, value in response.get('user_voting_history', {}).items():
            #label = tk.Label(main_frame), text=f"{field}: {value}"
            label.pack(anchor="w", pady=5)

    else:
        messagebox.showerror("Error", "Failed to fetch profile")