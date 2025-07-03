"""Module for GitHub API testing and automation."""



import jwt
import sys
import requests
import time
import subprocess

owner  = 'jc41809-sw'
repo = 'test'

def create_jwt_token():
  try:
    client_id = 'Iv23litO4fWD9ioj7Eav'

    with open("C:\\Users\\jc41809-sw\\Downloads\\key.pem", 'rb') as pem_file:
        signing_key = pem_file.read()






    payload = {
         # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (10 minutes maximum)
    'exp': int(time.time()) + 600,
    
    # GitHub App's client ID
    'iss': client_id
}
    
    encoded_jwt= jwt.encode(payload, signing_key,algorithm='RS256')
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
    # Create a JWT token
    token =  create_jwt_token()

    header = {
       "Accept" : 'application/vnd.github+json',
       'Authorization': f'Bearer {token}',
       'X-GitHub-Api-Version' : '2022-11-28'
    }


    
    output = requests.get(f"https://api.github.com/app/installations", headers=header)

 

    print("\n \n")
    tester = output.json()

    installationid = tester[0]['id']

    print(installationid)

    output2 = requests.post(f"https://api.github.com/app/installations/{installationid}/access_tokens",headers = header)
  

    tester = output2.json()
    print("\n \n")

    token = tester
    print (token['token'])
    return token['token']


    



def github_api_calls():
    local_file = 'test.zip'
    """Used to create and call the apis for github to return values"""
    test_token = github_app_authentication()

    header = {
       "Accept" : 'application/vnd.github+json',
       'Authorization': f'Bearer {test_token}',
       'X-GitHub-Api-Version' : '2022-11-28'
    }

    

    subprocess.run(['git', 'fetch'], check=True, capture_output=True, text=True)
    subprocess.run(['git', 'pull'], check=True, capture_output=True, text=True)

    
    #output = requests.get(f'https://api.github.com/repos/jc41809-sw/Work-scripts/zipball', headers=header)


    # if output.status_code == 200:
    #    with open(local_file, 'wb') as f:
    #       for chunk in output.iter_content(chunk_size=8192):
    #          f.write(chunk)
    
    # print  ( output.status_code)



    




def syncing_data():
    """Syncing all data from gitrhub to Azure Automation"""







if __name__ == "__main__":
    
    github_api_calls()






















    