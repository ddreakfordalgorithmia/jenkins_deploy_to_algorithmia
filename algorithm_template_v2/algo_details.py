import json

# Path within this repo where the algo.py, requirements.txt, and model file are located
ALGO_TEMPLATE_PATH = 'algorithm_template_v2'

# Models to be deserialized and used for inference
MODEL_FILES = [
    'data/model-a.joblib',
    'data/model-b.joblib'
]

# Images referenced by algorithm README
FEATURE_IMAGES = [
    'data/features-a.png',
    'data/features-b.png'
]

# Config algorithm details/settings as per https://docs.algorithmia.com/#create-an-algorithm
#
ALGORITHM_NAME = 'CreditCardApproval'
ALGORITHM_DETAILS = {
    'label': 'Credit Card Approval (autodeploy)',
    'tagline': 'Predict credit card approvals and risk scores using gradient boosting or random forrest classifier.'
}
ALGORITHM_SETTINGS = {
    'language': 'python3-1',
    'source_visibility': 'closed',
    'license': 'apl',
    'network_access': 'full',
    'pipeline_enabled': True,
    'environment': 'cpu'
}

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
    "insights_enabled" : True
}
