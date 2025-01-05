from db_base import FirebaseDBBase

class CategoryOperations(FirebaseDBBase):
    def __init__(self):
        # Initialize the base class with the 'users' collection
        super().__init__('user_categories')

    def add_user_selection(self, userid, selected_categories):
        # Format for selected_categories column
        # selected_categories = {
        #     "category1": true,
        #     "category3": true
        # }
        data = {'userid': userid, 'selectedCategories': selected_categories}
        user_id = self.add_document(data)
        print(f"User added with ID: {user_id}")
        return user_id

    def get_user_selection(self, user_id):
        return self.get_document(user_id)

    def update_user_selection(self, user_id, data):
        self.update_document(user_id, data)

    # def delete_user(self, user_id):
    #     self.delete_document(user_id)
