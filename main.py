import requests, csv, os, time #py -m pip install requests

#GLOBALS
#location of main.py
folder_path = os.path.dirname(os.path.abspath(__file__))
log__file_name = str(time.time()) + '_logs.txt' #log file naming
client_id = ""
client_secret = ""
myfastway_url = "uat.api.myfastway.com.au/"
identity_url = "https://uat.identity.fastway.org/connect/token"

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
    # if response.status_code == 200:
    #     return response
    # else:
    #     return(f"API request failed with status code {response.status_code}. Response: {response.text}")
    return response
    
#Write lines to a dynamic log file within the logs folder
def write_logs(action_reponse):
    with open(folder_path +  '/logs/' + log__file_name, 'a') as txt:
        txt.write(action_reponse)

def iterate_first_column(access_token):
    conids_list = []
    with open(folder_path + '\conids.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row:       
                conid = row[0]
                response = make_api_request(f"https://{myfastway_url}api/consignments/{conid}/reason/3", access_token)
                if response.status_code == 200:
                    print(f"Successfully deleted {conid}")
                    write_logs(f"Successfully deleted: {conid} with {response.status_code}\n")
                    conids_list.append(conid)
                else:
                    print(f"Delete request has failed with {response.status_code}. Response: {response.text}")  
                    write_logs(f"Failed to delete: {conid} with {response.status_code} {response.json()}\n")
            else:
                print("Cannot be empty!")

    return conids_list        

#This function adds any deleted conids to a new csv file which acts as a small database
def add_deleted_conids_to_csv(conids_list):
    with open(folder_path + '\deleted_conids.csv', 'w') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        for conid in conids_list:
            writeCSV.writerow([conid])


access_token = get_access_token(identity_url, client_id, client_secret)
           
# Call the delete function iterating over the list in the csv
conids_list = iterate_first_column(access_token)

#Call function to write deleted conids to new csv file
add_deleted_conids_to_csv(conids_list)


