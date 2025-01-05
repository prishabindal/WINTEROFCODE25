from firebase_admin import firestore
import warnings


# Base class for Firestore operations
class FirebaseDBBase:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.db = firestore.client()

    def add_document(self, data):
        print(data)
        print(f'Add to {self.collection_name}')
        """
        Add a document to the Firestore collection with an auto-generated document ID.
        """
        _,doc_ref = self.db.collection(self.collection_name).add(data)
        print(f'Document added with ID {doc_ref.id} to {self.collection_name}')
        return doc_ref.id  # Return the auto-generated ID

    def get_document(self, doc_id):
        print(f'Get from {self.collection_name} by id')
        """
        Get a document from the Firestore collection.
        """
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            print(f'Document data: {doc.to_dict()}')
            return doc.to_dict()
        else:
            print(f'No document found with ID {doc_id}')
            return None

    def update_document(self, doc_id, data):
        print(f'Update document in {self.collection_name} by {doc_id}')
        """
        Update an existing document in the Firestore collection.
        """
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        doc_ref.update(data)
        print(f'Document {doc_id} updated in {self.collection_name}')

    def delete_document(self, doc_id):
        print(f'Delete document in {self.collection_name} by {doc_id}')
        """
        Delete a document from the Firestore collection.
        """
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        doc_ref.delete()
        print(f'Document {doc_id} deleted from {self.collection_name}')

    def get_all_values(self):
        print(f"Get all values from {self.collection_name}")
        ref = self.db.collection(self.collection_name)
        data = ref.stream()
        json_data=[]
        for doc in data:
            print(f'{doc.id} => {doc.to_dict()}')
            json_data.append(doc.to_dict()) 
        print(json_data)
        return json_data

    # def run_query(self, conditions):
    #     print(f"Run query on {self.collection_name}: {conditions}")
    #     """
    #     Run a Firestore query with multiple conditions.

    #     :param conditions: List of conditions. Each condition is a tuple:
    #     (field_name, operator, value)
    #     Example: [("age", ">", 20), ("status", "==", "active")]
    #     :return: List of documents that match the query.
    #     """
    #     print(f"Running complex query on {self.collection_name}")
        
    #     # Start building the query
    #     ref = self.db.collection(self.collection_name)

    #     ref.where(filter=firestore.FieldFilter("Username", "==", "user1"))
    #     ref.where(filter=firestore.FieldFilter("Password", "==", "1234"))
        

        
    #     # query = ref.where(filter=firestore.FieldFilter("Username", "==", "user1"))
    #     # Apply each condition
    #     # for field_name, operator, value in conditions:
    #     #     # query = query.where(field_name, operator, value)
    #     #     query = query.where(filter=firestore.FieldFilter(field_name, operator, value))
            
    #         # print(query)

    #     print(ref)
    #     # Execute the query and fetch results
    #     results = ref.stream()
    #     print(results)
    #     json_data = []
    #     for doc in results:
    #         print(f'{doc.id} => {doc.to_dict()}')
    #         json_data.append(doc.to_dict())
        
    #     return json_data

    def run_query(self, conditions):
        print(f"Run query on {self.collection_name}: {conditions}")
        
        
        dbref = self.db.collection(self.collection_name)

        calls = "dbref"
        for field_name, operator, value in conditions:
            calls = calls + f".where(\"{field_name}\", \"{operator}\", \"{value}\")"

        query = eval(calls)
        
        # Execute the query and fetch results
        results = query.stream()
        json_data = []
        for doc in results:
            print(f'{doc.id} => {doc.to_dict()}')
            json_data.append(doc.to_dict())
        print(f"json_data: {json_data}")
        return json_data
    
    def run_or_query(self, or_conditions):
        print(f"Run OR query on {self.collection_name}: {or_conditions}")
        """
        Run an OR query by combining results from multiple queries.

        :param or_conditions: List of condition tuples for OR logic.
        Example: [("status", "==", "active"), ("age", ">", 30)]
        :return: List of unique documents that match any condition.
        """
        print(f"Running OR query on {self.collection_name}")
        result_set = set()
        
        for field_name, operator, value in or_conditions:
            query = self.db.collection(self.collection_name).where(field_name, operator, value)
            results = query.stream()
            for doc in results:
                result_set.add(doc.id)  # Use document IDs to ensure uniqueness
        
        # Fetch and return full document details for the unique IDs
        json_data = []
        for doc_id in result_set:
            doc = self.get_document(doc_id)
            if doc:
                json_data.append(doc)
        
        return json_data