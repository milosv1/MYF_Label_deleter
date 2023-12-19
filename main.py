import requests, csv, os #py -m pip install requests

#location of main.py
folder_path = os.path.dirname(os.path.abspath(__file__))

#creds
client_id = ""
client_secret = ""

def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials", "scope": "fw-fl2-api-au"},
        auth=(client_id, client_secret),
    )
    if response.json()["access_token"]:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token.")
    
def make_api_request(api_url, access_token):
    # Make API request using the OAuth token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.delete(api_url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return(f"API request failed with status code {response.status_code}. Response: {response.text}")

def iterate_first_column(access_token):
    with open(folder_path + '\conids.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row[0])
            print(make_api_request(f"https://api.myfastway.com.au/api/consignments/{row[0]}/reason/3", access_token))
                

access_token = get_access_token("https://identity.fastway.org/connect/token", client_id, client_secret)
           
# Call the delete function iterating over the list in the csv
iterate_first_column(access_token)