import requests, csv #py -m pip install requests

#creds
client_id = ""
client_secret = ""

def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials", "scope": "fw-fl2-api-au"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]
    
# assign to a variable to pass to delete     
print(get_access_token("https://identity.fastway.org/connect/token", client_id, client_secret))



## Doesnt work yet
def iterate_first_column(csv_file_path):
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        
        # Iterate over each row and print the first column
        for row in csv_reader:
            if row:  # Check if the row is not empty
                first_column_value = row[0]
                print(first_column_value) #add delete action here
                
           
# Provide the path to your CSV file
csv_file_path = 'labels.csv'

# Call the function with the CSV file path
# iterate_first_column(csv_file_path)


