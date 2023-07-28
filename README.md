# Microsoft Graph to Elasticsearch Audit Log Sync

This is a Python script that interacts with the Microsoft Graph API to retrieve Office 365 audit logs and stores the logs in a CSV file, which is then shipped to an Elasticsearch instance.

The script runs in an infinite loop, making a request to the API every 5 minutes, and retrieving logs from the last 5 minutes.

## Dependencies
This script depends on:
- `msgraph.core` for interacting with Microsoft Graph API
- `azure.identity` for Azure authentication
- `elasticsearch` and `elasticsearch.helpers` for interacting with Elasticsearch
- `csv` and `os` for file handling
- `time` and `datetime` for scheduling requests and formatting timestamps

## How to Use
1. **Configure your credentials:** Replace the placeholders for `client_id`, `client_secret`, `tenant_id`, `cloud_id`, `username`, and `password` with your actual credentials.

2. **Run the script:** The script runs in an infinite loop, making a request to the Microsoft Graph API every 5 minutes, and retrieving logs from the last 5 minutes.

## Known Limitations
1. The CSV file `entraaudit.csv` is cleared every 5 minutes. This means any logs older than 5 minutes and not shipped to Elasticsearch will be lost. Ensure Elasticsearch is up and running to avoid data loss.
2. Error handling is minimal. Ensure correct configuration of your credentials and connectivity to Microsoft Graph and Elasticsearch.

## Future Features
1. **Fix CSV Handling and Make It More Modern:** Enhance the way CSV files are handled to make it more efficient and modern.
2. **Better Error Handling:** Improve error handling to make the script more robust and reliable.
3. **Docker Container:** Package the script into a Docker container for easier distribution, deployment, and execution.
4. **Better Credential Handling:** Enhance the way credentials are managed and stored, possibly integrating with Azure Key Vault or other secure credential storage solutions.

## License
This project is licensed under the terms of the [MIT license](LICENSE).

## Contact
For questions or feedback, please reach out to [username@example.com](mailto:username@example.com).

