import time
import datetime
from msgraph.core import GraphClient
from azure.identity import ClientSecretCredential
import csv
import os
from elasticsearch import Elasticsearch, helpers

#Variables
client_id = ""
client_secret = ""
tenant_id = ""
graph_endpoint = 'https://graph.microsoft.com/beta/auditLogs/directoryAudits'
cloud_id = ''
username = ''
password = ''
es_index = 'entraaudit'

# Create a ServicePrincipalCredentials object
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

# Create the GraphClient
graph_client = GraphClient(credential=credentials)
# Create the Elasticsearch client
es_client = Elasticsearch(
    cloud_id=cloud_id,
    http_auth=(username, password),
)
#define column names
column_names = ['id','activityDateTime', 'category', 'correlationId', 'result', 'resultReason', 'activityDisplayName', 'loggedByService', 'initiatedBy','operationType', 'targetResources', 'additionalDetails']

while True:
    # Calculate the start and end times for the query
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=5)

    # Format the start and end times as ISO 8601 strings
    start_time_str = start_time.isoformat() + 'Z'
    end_time_str = end_time.isoformat() + 'Z'

    # Build the query string
    query_string = f"{graph_endpoint}?$filter=activityDateTime ge {start_time_str} and activityDateTime le {end_time_str}"

    # Make the request to the Microsoft Graph API
    response = graph_client.get(query_string)
    # Clear the contents of the CSV file every 5 minutes
    if datetime.datetime.utcnow().minute % 5 == 0:
        open('entraaudit.csv', 'w').close()
        print("Cleared contents of CSV file")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        response_json = response.json()
        # Check if the response contains the expected data
        if 'value' in response_json:
            #Write to file
            with open('entraaudit.csv', 'a' ,newline="", encoding="utf-8") as audit_logs:
                writer = csv.DictWriter(audit_logs, fieldnames=column_names)
                if os.stat('entraaudit.csv').st_size == 0:
                    writer.writeheader()
                for event in response_json['value']:
                    writer.writerow({
                        'id': event['id'],
                        'activityDateTime': event['activityDateTime'],
                        'category': event['category'],
                        'correlationId': event['correlationId'],
                        'result': event['result'],
                        'resultReason': event['resultReason'],
                        'activityDisplayName': event['activityDisplayName'],
                        'loggedByService': event['loggedByService'],
                        'initiatedBy': event['initiatedBy'],
                        'operationType': event['operationType'],
                        'targetResources': event['targetResources'],
                        'additionalDetails': event['additionalDetails'],
                        })
                print(f"Wrote {len(response_json['value'])} events to CSV file")

            # Read the CSV file and ship the data to Elastic
            with open('entraaudit.csv', 'r', encoding="utf-8") as f:
                reader = csv.DictReader(f)
                actions = [
                    {
                        '_index': es_index,
                        '_source': row,
                    }
                    for row in reader
                ]
                helpers.bulk(es_client, actions)
            print(f"Shipped {len(response_json['value'])} events to Elastic")

        else:
            print("Error: Response does not contain 'value' key")
            print(response.content)
    else:
        print("Error: Request failed with status code", response.status_code)
        print(response.content)

    # Wait for 5 minutes before running the loop again
    time.sleep(300)