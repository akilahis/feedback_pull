import requests
import os 
import json
from datetime import datetime

# Define your API endpoint and parameters
url = "https://us-central1-chumbaka-dev-tms.cloudfunctions.net/bdAPI"
params = {
    "type": "feedbacks",
    "from": "2024-01-01",
    "to": "2025-06-16",
    #"schedule_id" : "MALAYSIA_MON0000_867"
}

# Add your authorization token (replace TOKEN_HERE with your actual token)
headers = {
    "Authorization": "Bearer Mdj-e3_ue4n%n3Hdj_emfH-dbKrrJr33fe4-u3e_n3",
    "Content-Type": "application/json"
}
# Create a data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Generate a timestamped filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"data/feedback_data_{timestamp}.json"

try:
    # Make the API request
    print("Making API request...")
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("Request successful!")
        
        # Save the data to a file
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Data saved to {filename}")
        
        # Print summary information
        print(f'Length of data: {len(data)}')
        print("First item preview:", data[0])
        
        # Also save a most_recent.json for easy access
        with open('data/most_recent.json', 'w') as f:
            json.dump(data, f, indent=2)
        print("\nAlso saved as data/most_recent.json for quick access")
        
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")