# !/usr/bin/env python3
"""Module for GitHub API testing and automation."""
# Jaheim Cain

import jwt
import sys
import requests
import time
import subprocess
import base64
import os 
import sys
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
tmp_root = r"C:/AzureAutomation"
sys.path.append(os.path.join(tmp_root, "SubScripts"))
from SecretServerPackage import TeamPasswordManager

try:
  # Collecting credentials for tpm
  Auth_token = DefaultAzureCredential(exclude_managed_identity_credential=True, exclude_enviornmental_credential=True)
  testingSec = SecretClient( vault_url='https://gsu-iam-devkv.vault.azure.net/', credential=Auth_token)


  # Creating an instance fo tpm for keys and users
  secret_server = TeamPasswordManager()
  secret_server.connect(
            base_url="https://tpm.georgiasouthern.edu/index.php/",
            public_key=testingSec.get_secret("TPMPublic").value,
            private_key=testingSec.get_secret("TPMPrivate").value
            )


  # Collecting client ids and keys from tpm
  usercall = secret_server.get_username(3046)
  keycall = secret_server.get_encrypted_note(3046)
except Exception as e: 
  print (f'error connecting to azure due to {e}')

owner  = 'jc41809-sw'
repo = 'test'




def create_jwt_token():
  try:
    get_tpm_user = usercall
    tpm_bytes = base64.b64decode(keycall)
    # Payload Creation for the key
    payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 60,
    
    # GitHub App's client ID
    'iss': get_tpm_user
    }
    # Create token using credentials
    encoded_jwt= jwt.encode(payload,tpm_bytes,algorithm='RS256')
    print("JWT Token Created")

    return encoded_jwt

  except FileNotFoundError as e:
    print(f"Error finding path: {e}")
    sys.exit(1)
  except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(1)


def github_app_authentication():
  """Base app authentication for github app"""
  try:
    # Calling for jwt token
    token =  create_jwt_token()

    # Passing in jwt token to get oauth token
    header = {
       "Accept" : 'application/vnd.github+json',
       'Authorization': f'Bearer {token}',
       'X-GitHub-Api-Version' : '2022-11-28'
    }

    #request for the installl id
    install_id_request = requests.get(f"https://api.github.com/app/installations", headers=header).json()
    installationid = install_id_request[0]['id']

    # Request for the access token
    OAuth_token_request = requests.post(f"https://api.github.com/app/installations/{installationid}/access_tokens",headers = header).json()
    return OAuth_token_request['token']
  except requests.exceptions.HTTPError as e:
   print(f'Error Invalid Url : {e}')
  except requests.exceptions.ConnectTimeout as e:
    print(f'Error connection timeout: {e}')



if __name__ == "__main__":
  try:
    # github_api_calls()
    test_token = github_app_authentication()
    print(test_token)
    # Pull request for the listed repo
    subprocess.run(['C:\\AzureAutomation\\Dependencies\\Git\\Git\\git.exe', 'pull', f'https://{owner}:{test_token}@github.com/{owner}/{repo}.git'], text=True, shell=False)
  
  except FileNotFoundError as e :
    print ('Subprocess has an error getting the path to git. Please check path and try again.')
  except TypeError as e:
    print ('One of the datatypes inputted were incorrect please try again later.')















    