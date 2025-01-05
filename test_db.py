from firebase_config import initialize_firebase
initialize_firebase()


def addUserDetails():
    from user_details import UserDetails
    user_details = UserDetails()
    user_details.add_user(username="user1", password="1234", email="user1@gmail.com", 
                        phoneNumber="45377338", firstName="userFirst")
    print(user_details.get_user_by_username("user1"))

    user_details.add_user(username="user2", password="68899", email="user2@yahoo.co.in", 
                        phoneNumber="587686986", firstName="userSecond")
    print(user_details.get_user_by_username("user2"))
    print(user_details.run_query([("FirstName", "!=", "userFirst")]))

    

# addUserDetails()

# def addVotingCategories():
#     from voting_categories import VotingCategory
#     votingCategory = VotingCategory()
#     id = votingCategory.add_category(votCatName="Science", votCatDesc="Science related topics")
#     print(votingCategory.get_category_by_id(id))

#     id = votingCategory.add_category(votCatName="Art", votCatDesc="Arts and culture")
#     print(votingCategory.get_category_by_id(id))

#     id = votingCategory.add_category(votCatName="Technology", votCatDesc="Technology related topics")
#     print(votingCategory.get_category_by_id(id))
    
#     print(votingCategory.get_all_categories())

# # addVotingCategories()

# def addVotingDetails():
#     from voting_details import VotingDetails
#     votingDetails = VotingDetails()
#     id = votingDetails.add_voting_details(votDtlsName=, votDtlsDesc=, votDtlsNumberOfOpt=)
#     print(votingDetails.get_voting_details(id))

#     print(votingDetails.get_all_voting_details())

# # addVotingDetails()

# def addVotingDetailsOptions():
#     from voting_details_options import VotingDetailsOptions
#     votingDetailsOptions = VotingDetailsOptions()
#     id = votingDetailsOptions.add_voting_details_options(votDtlsId=, votDtlsOptionName=)
#     print(votingDetailsOptions.get_voting_details_options_by_optionid(id))

#     print(votingDetailsOptions.get_all_voting_details_options())

# # addVotingDetailsOptions()


def addCatDetailsMapping():
    from voting_cat_details_mapping import VotingCatDetailsMapping
    votingCatDetailsMapping = VotingCatDetailsMapping()
    id = votingCatDetailsMapping.add_cat_dtls_mapping(votCatId='1', votDtlsId='1')
    print(votingCatDetailsMapping.get_voting_details_by_id(id))

    print(votingCatDetailsMapping.get_all_mappings())

addCatDetailsMapping()

# from user_preferences import UserPreferences
# userPreferences = UserPreferences()
# userpref = userPreferences.add_user_pref(user_id="abc", votcatId=["1","2"])
# userPreferences.get_user_pref_by_userid("abc")