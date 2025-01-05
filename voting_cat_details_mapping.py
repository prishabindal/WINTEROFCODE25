from db_base import FirebaseDBBase
'''Format
{
    'VotCatId': '',
    'VotDtlsId': ''
}
'''
class VotingCatDetailsMapping(FirebaseDBBase):
    def __init__(self):
        super().__init__('VOTING_CAT_DETAILS_MAPPING')

    def get_voting_details_by_catid(self, votCatId):
        return self.cat_dtls_mapping_run_query([("VotCatId", "==", votCatId)])

    def get_voting_details_by_dtlsid(self, votDtlsId):
        return self.cat_dtls_mapping_run_query([("VotDtlsId", "==", votDtlsId)])
    
    def get_voting_details_by_id(self, id):
        return self.get_document(id)

    def get_all_mappings(self):
        return self.get_all_values()
           
    def add_cat_dtls_mapping(self, votCatId, votDtlsId):
        data = {
            'VotCatId': votCatId,
            'VotDtlsId': votDtlsId
        }
        id = self.add_document(data)
        data['id'] = id
        self.update_cat_dtls_mapping(data)
        print(f"Voting Category Details Mapping saved with id: {id}")
        return id

    def update_cat_dtls_mapping(self, data):
        self.update_document(data['id'], data)

    def cat_dtls_mapping_run_query(self, conditions):
        return self.run_query(conditions)
    
    def cat_dtls_mapping_run_or_query(self, or_conditions):
        return self.run_or_query(or_conditions)

    
    
