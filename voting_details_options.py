from db_base import FirebaseDBBase
'''Format
{
    'VotDtlsId': '',
    'VotDtlsOptionId': '',
    'VotDtlsOptionName': '' 
}
'''
class VotingDetailsOptions(FirebaseDBBase):
    def __init__(self):
        super().__init__('VOTING_DETAILS_OPTIONS')

    def get_voting_details_options_by_votdtlsid(self, votDtlsId):
        return self.voting_details_options_run_query([("VotDtlsId", "==", votDtlsId)])

    def get_voting_details_options_by_optionid(self, VotDtlsOptionId):
        return self.get_document(VotDtlsOptionId)
    
    def get_all_voting_details_options(self):
        return self.get_all_values()
    
    def add_voting_details_options(self, votDtlsId, votDtlsOptionName):
        data = {
            'VotDtlsId': votDtlsId,
            'VotDtlsOptionName': votDtlsOptionName 
        }
        votDtlsOptionId = self.add_document(data)
        data['VotDtlsOptionId'] = votDtlsOptionId
        self.update_voting_details_options(votDtlsOptionId, data)
        print(f"Voting Detais Option saved for VotDtlsOptionId: {votDtlsOptionId}")
        return votDtlsOptionId

    def update_voting_details_options(self, data):
        self.update_document(data['VotDtlsOptionId'], data)

    def voting_details_options_run_query(self, conditions):
        return self.run_query(conditions)
    
    def voting_details_options_run_or_query(self, or_conditions):
        return self.run_or_query(or_conditions)    
