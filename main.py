import requests, csv, os #py -m pip install requests


#location of main.py
folder_path = os.path.dirname(os.path.abspath(__file__))


#Enter your Myfastway Credentials (UAT)
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
    # if response.status_code == 200:
    #     return response
    # else:
    #     return(f"API request failed with status code {response.status_code}. Response: {response.text}")
    return response

def iterate_first_column(access_token):
    conids_list = []
    with open(folder_path + '\conids.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            # if row is not empty...
            #TODO - try and get content of each cell, then save them onto the list and into other csv file.
            if row:       
                conid = row[0]
                conids_list.append(conid)
                response = make_api_request(f"https://uat.api.myfastway.com.au/api/consignments/{conid}/reason/3", access_token)
                if response.status_code == 200:
                    print(f"Successfully deleted {conid}")
                else:
                    print(f"Delete request has failed with {response.status_code}. Response: {response.text}")         
            else:
                print("Cannot be empty!")

    return conids_list        


#This function adds any deleted conids to a new csv file which acts as a small database
def add_deleted_conids_to_csv(conids_list):
    with open(folder_path + '\deleted_conids.csv', 'w') as csvfile:
        writeCSV = csv.writer(csvfile, delimiter=',')
        for conid in conids_list:
            writeCSV.writerow([conid])


def write_logs(conid, access_token):
    with open(folder_path + '\logs.txt', 'a') as txt:
        response = make_api_request(f"https://uat.api.myfastway.com.au/api/consignments/{conid}/reason/3", access_token)
       
        print(f"Response for {conid}: {response.status_code} - {response.text}")
       
        try:
            response_json = response.json()
        except ValueError:
            response_json = None

        if response.status_code == 200:
            txt.write(f"Successfully deleted: {conid} with {response.status_code}\n")
            if response_json:
                txt.write(f"Response: {response_json}\n")
        else:
            txt.write(f"Failed to delete: {conid} with {response.status_code}\n")
            if response_json:
                txt.write(f"Error Response: {response_json}\n")

        txt.write('\n')


access_token = get_access_token("https://uat.identity.fastway.org/connect/token", client_id, client_secret)
           
# Call the delete function iterating over the list in the csv
#iterate_first_column(access_token)

conids_list = iterate_first_column(access_token)

#Call function to write deleted conids to new csv file
add_deleted_conids_to_csv(conids_list)

#For each conid in the list, write a log to the logs.txt file
for conid in conids_list:
    write_logs(conid, access_token)
