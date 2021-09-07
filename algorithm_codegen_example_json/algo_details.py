import json

# Path within this repo where the algo.py, requirements.txt, and model file are located
ALGO_TEMPLATE_PATH = 'algorithm_codegen_example_json'
ALGO_DATA_PATH = f"{ALGO_TEMPLATE_PATH}/data"

# Files to be uploaded to a hosted data collection
# Such as:
# - Models to be deserialized and used for inference
# - Libraries to be loaded at runtime (scoring code jar in this example)
MODEL_FILES = [
    # '612ed4900f36aeb71aea695c-612e415c8f79f0a48ad152b7-pe.jar'
    "model-a.joblib",
    "model-b.joblib"
]

# Images referenced by algorithm README
FEATURE_IMAGES = [
    'features-a.png',
    'features-b.png'
]

# Config algorithm details/settings as per https://docs.algorithmia.com/#create-an-algorithm
#
ALGORITHM_NAME = 'LoanDefaultPrediction'
ALGORITHM_DETAILS = {
    'label': 'Loan Default Prediction (autodeployed)',
    'tagline': 'Predict loan default using the top-rated classification model from the DataRobot Leaderboard.'
}

# This algorithm uses the "Python 3.7 + H2O" environment
ALGORITHM_SETTINGS = {
    'language': 'python3',
    'algorithm_environment': '0175c4fb-aa63-46ba-9a53-9571c7df5e73',
    'source_visibility': 'closed',
    'license': 'apl',
    'network_access': 'full',
    'pipeline_enabled': True,
    'environment': 'cpu'
}

# SAMPLE_INPUT = [
#     { "loan_amt": 4000,
#       "funded_amt": 4000,
#       "term": " 60 months",
#       "int_rate": 0.07,
#       "installment": 79.76,
#       "grade": "A",
#       "sub_grade": "A4",
#       "emp_title": "Time Warner Cable",
#       "emp_length": "10+ years",
#       "home_ownership": "MORTGAGE",
#       "annual_inc": 50000.0,
#       "verification_status": "not verified",
#       "pymnt_plan": "n","url": "https:\\/\\/www.lendingclub.com\\/browse\\/loanDetail.action?loan_id=728956",
#       "desc": None,
#       "purpose": "medical",
#       "title": "Medical",
#       "zip_code": "766xx",
#       "addr_state": "TX",
#       "dti": 10.87,
#       "delinq_2yrs": 0.0,
#       "earliest_cr_line": "12\\/1\\/92",
#       "inq_last_6mths": 0.0,
#       "mths_since_last_delinq": None,
#       "mths_since_last_record": None,
#       "open_acc": 15.0,
#       "pub_rec": 0.0,
#       "revol_bal": 12087,
#       "revol_util": 12.1,
#       "total_acc": 44.0,
#       "initial_list_status": "f",
#       "mths_since_last_major_derog": None,
#       "policy_code": 1
#     }
# ]
SAMPLE_INPUT = {
    "high_balance": 0, 
    "owns_home": 1, 
    "child_one": 0, 
    "child_two_plus": 0, 
    "has_work_phone": 0, 
    "age_high": 0, 
    "age_highest": 1, 
    "age_low": 0, 
    "age_lowest": 0, 
    "employment_duration_high": 0, 
    "employment_duration_highest": 0, 
    "employment_duration_low": 0, 
    "employment_duration_medium": 0, 
    "occupation_hightech": 0, 
    "occupation_office": 1, 
    "family_size_one": 1,
    "family_size_three_plus": 0,
    "housing_coop_apartment": 0,
    "housing_municipal_apartment": 0,
    "housing_office_apartment": 0,
    "housing_rented_apartment": 0,
    "housing_with_parents": 0,
    "education_higher_education": 0,
    "education_incomplete_higher": 0,
    "education_lower_secondary": 0,
    "marital_civil_marriage": 0,
    "marital_separated": 0,
    "marital_single_not_married": 1,
    "marital_widow": 0
}

# Config publish settings as per https://docs.algorithmia.com/#publish-an-algorithm
#
ALGORITHM_VERSION_INFO = {
    "release_notes": "Automatically created, deployed and published from Jenkins.",
    "sample_input": json.dumps(SAMPLE_INPUT),
    "version_type": "minor",
    "insights_enabled" : False
}
