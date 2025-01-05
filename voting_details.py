from db_base import FirebaseDBBase
'''Format
{
    'VotDtlsId': '',
    'VotDtlsName': '',
    'VotDtlsDesc': '',
    'VotDtlsNumberOfOpt': 
}
'''
class VotingDetails(FirebaseDBBase):
    def __init__(self):
        super().__init__('VOTING_DETAILS')

    def get_voting_details(self, votDtlsId):
        return self.get_document(votDtlsId)

    def get_all_voting_details(self):
        return self.get_all_values()
    
    def add_voting_details(self, votDtlsName, votDtlsDesc = None, votDtlsNumberOfOpt = 0):
        data = {
            'VotDtlsName': votDtlsName,
            'VotDtlsDesc': votDtlsDesc,
            'VotDtlsNumberOfOpt': votDtlsNumberOfOpt
        }
        votDtlsId = self.add_document(data)
        data['VotDtlsId'] = votDtlsId
        self.update_voting_details(votDtlsId, data)
        print(f"Voting Details saved for VotDtlsId: {votDtlsId}")
        return votDtlsId

    def update_voting_details(self, data):
        self.update_document( data['VotDtlsId'], data)

    def voting_details_run_query(self, conditions):
        return self.run_query(conditions)
    
    def voting_details_run_or_query(self, or_conditions):
        return self.run_or_query(or_conditions)
   
