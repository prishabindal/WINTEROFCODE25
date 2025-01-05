from db_base import FirebaseDBBase
'''Format
{
    'VotCatId': '',
    'VotCatName': '',
    'VotCatDesc': ''
}
'''
class VotingCategory(FirebaseDBBase):
    def __init__(self):
        super().__init__('VOTING_CATEGORY')

    def get_category_by_id(self, votCatId):
        print("Get category by votCatId")
        return self.get_document(votCatId)

    def get_all_categories(self):
        print("Get all categories")
        return self.get_all_values()

    def add_category(self, votCatName, votCatDesc):
        print("Add category")
        data = {
            'VotCatName': votCatName,
            'VotCatDesc': votCatDesc
        }
        votCatId = self.add_document(data)
        data['VotCatId'] = votCatId
        self.update_category(votCatId, data)
        print(f"Category saved for VotCatId: {votCatId}")
        return votCatId

    def update_category(self, votCatId, data):
        print("Update category")
        self.update_document(votCatId, data)

    def category_run_query(self, conditions):
        print("Run query in category")
        return self.run_query(conditions)
    
    def category_run_or_query(self, or_conditions):
        print("Run OR query in category")
        return self.run_or_query(or_conditions)
