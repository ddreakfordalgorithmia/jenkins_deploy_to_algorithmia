#from algorithm_credit_approval.algo_details import ALGORITHM_DETAILS, ALGORITHM_NAME, ALGORITHM_SETTINGS, ALGORITHM_VERSION_INFO, ALGO_DATA_PATH, ALGO_TEMPLATE_PATH, FEATURE_IMAGES, MODEL_FILES
from algorithm_codegen_example_json.algo_details import ALGORITHM_DETAILS, ALGORITHM_NAME, ALGORITHM_SETTINGS, ALGORITHM_VERSION_INFO, ALGO_DATA_PATH, ALGO_TEMPLATE_PATH, FEATURE_IMAGES, MODEL_FILES
import Algorithmia
from datetime import datetime
from git import Repo
from os import environ
from shutil import copyfile
from six.moves.urllib.parse import quote_plus
from tempfile import mkdtemp
from time import sleep

### --------- REQUIRED ENVIRONMENT VARIABLES ----------
#
# ALGORITHMIA_API_KEY - must have permission to manage algorithms
#
# ALGORITHMIA_DOMAIN - your Algorithmia Enterprise domain
#    E.g.: YOUR_COMPANY.productionize.ai
# 
# ALGORITHMIA_USERNAME - self explanatory
#
api_key = environ.get('ALGORITHMIA_API_KEY')
algo_domain = environ.get('ALGORITHMIA_DOMAIN')
algo_endpoint = f"https://{algo_domain}"
username = environ.get('ALGORITHMIA_USERNAME')
if not api_key:
    raise SystemExit('Please set the environment variable ALGORITHMIA_API_KEY (key must have permission to manage algorithms)')
if not algo_domain:
    raise SystemExit('Please set the environment variable ALGORITHMIA_DOMAIN (e.g. algorithmia.com')
if not username:
    raise SystemExit('Please set the environment variable ALGORITHMIA_USERNAME')


### --------- Algorithm Details ---------
#
if not ALGO_TEMPLATE_PATH:
    raise SystemExit('ALGO_TEMPLATE_PATH has not been set (see ./algo_details.py)')

# The algorithm will be created under https://ALGORITHMIA_ENDPOINT/ALGORITHMIA_USERNAME/ALGO_NAME
ALGO_NAME = ALGORITHM_NAME
if not ALGO_NAME:
    raise SystemExit('ALGORITHM_NAME has not been set (see ./algo_details.py)')

# The data collection will be created at https://ALGORITHMIA_ENDPOINT/data/ALGORITHMIA_USERNAME/COLLECTION_NAME
# Here, we used the algoritm name as the collection name, but it could be any legal name.
COLLECTION_NAME = f"{ALGO_NAME}"

# Config algorithm details/settings as per https://docs.algorithmia.com/#create-an-algorithm
if not ALGORITHM_DETAILS:
    raise SystemExit('ALGORITHM_DETAILS has not been set (see ./algo_details.py)')
if not ALGORITHM_SETTINGS:
    raise SystemExit('ALGORITHM_SETTINGS has not been set (see ./algo_details.py)')
if not ALGORITHM_VERSION_INFO:
    raise SystemExit('ALGORITHM_VERSION_INFO has not been set (see ./algo_details.py)')

# Simplistic template usage example.
# If you need to update the contents of algo.py during deployment, do so here
def UPDATE_ALGORITHM_TEMPLATE(file_contents):
    return file_contents.replace('#algo_username#', username)

# Set up Algorithmia client and path names
algo_full_name = username+'/'+ALGO_NAME
data_path = 'data://'+username+'/'+COLLECTION_NAME
client = Algorithmia.client(api_key, algo_endpoint)
algo = client.algo(algo_full_name)
algo.set_options(timeout=300) # optional

# Create Hosted Data collection
print('CREATING '+data_path)
print(f"ON Algorithmia cluster: {algo_endpoint}")
if not client.dir(data_path).exists():
    client.dir(data_path).create()

# Upload the model file(s)
print('UPLOADING model file(s) to '+data_path)
for modelFile in MODEL_FILES:
    print(f"UPLOADING {data_path}/{modelFile}")
    client.file(f"{data_path}/{modelFile}").putFile(f"{ALGO_DATA_PATH}/{modelFile}")

# Upload other supporting files (e.g. for documentation)
print('UPLOADING supporting file(s) to '+data_path)
for auxFile in FEATURE_IMAGES:
    print(f"UPLOADING {data_path}/{auxFile}")
    client.file(f"{data_path}/{auxFile}").putFile(f"{ALGO_DATA_PATH}/{auxFile}")

# Create the Algorithm on AE
try:
    print(f"CREATING algorithm: {algo_full_name}")
    print(f"ON Algorithmia cluster: {algo_endpoint}")
    print(algo.create(details=ALGORITHM_DETAILS, settings=ALGORITHM_SETTINGS))
except Exception as x:
    print(str(x))
    if 'already exists' in str(x):
        try:
            print(f"UPDATING algorithm: {algo_full_name}")
            # print(algo.update(details=ALGORITHM_DETAILS, settings=ALGORITHM_SETTINGS))
        except Exception as x:
            raise SystemExit('ERROR: could not UPDATE {}: \n{}'.format(algo_full_name, x))
    else:
        raise SystemExit('ERROR: could not CREATE {}: \n{}'.format(algo_full_name, x))

# git clone the created algorithm's repo into a temp directory
tmpdir = mkdtemp()
encoded_api_key = quote_plus(api_key)
algo_repo = f"https://{username}:{encoded_api_key}@git.{algo_domain}/git/{algo_full_name}.git"
print(f"CLONING serving repo: {algo_repo}")
print(f"To local: {tmpdir}")
cloned_repo = Repo.clone_from(algo_repo, tmpdir)

# Add algo.py into repo
print('ADDING algorithm files...')
algorithm_file_name='{}.py'.format(algo_full_name.split('/')[1])
# Add requirements.txt into repo
copyfile(ALGO_TEMPLATE_PATH+'/requirements.txt', tmpdir+'/requirements.txt')
print(f"Copied requirements.txt to {tmpdir}/requirements.txt")
# Add README.md into repo
copyfile(ALGO_TEMPLATE_PATH+'/README.md', tmpdir+'/README.md')
print(f"Copied README.md to {tmpdir}/README.md")

# Update the algorithm (replacing template values)
algo_template = f"{ALGO_TEMPLATE_PATH}/algo.py"
algo_to_push = f"{tmpdir}/src/{algorithm_file_name}"
with open(algo_template, 'r+') as file_in:
    with open(algo_to_push, 'w+') as file_out:
        file_out.write(UPDATE_ALGORITHM_TEMPLATE(file_in.read()))
print(f"Wrote algorithm file '{algo_to_push}' from template '{algo_template}'")

cloned_repo.git.add(all=True)
cloned_repo.index.commit('Add algorithm files')

# push changes (implicitly causes Algorithm to recompile on server)
print('PUSHING local files to serving repo')
origin = cloned_repo.remote(name='origin')
origin.push()

# wait for compile to complete, then publish the Algorithm
print('Waiting for algorithm to compile...')
sleep(15)
print('PUBLISHING '+algo_full_name)
try:
    results = algo.publish(
        settings = {
            "algorithm_callability": "private"
        },
        version_info=ALGORITHM_VERSION_INFO,
        details = ALGORITHM_DETAILS
    )
except:
    # print('RETRYING: if this occurs repeatedly, increase the sleep() time before the PUBLISH step to allow for compilation time')
    try:
        sleep(60)
        results = algo.publish(
            settings = {
                "algorithm_callability": "private"
            },
            version_info = ALGORITHM_VERSION_INFO,
            details = ALGORITHM_DETAILS        
        )
    except Exception as x:
        raise SystemExit('ERROR: unable to publish Algorithm: code will not compile, or compile takes too long\n{}'.format(x))

print(results)
print(f"DEPLOYED version {results.version_info.semantic_version} to {algo_endpoint}/algorithms/{algo_full_name}")
