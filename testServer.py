import requests

# URL of the predict endpoint
url = 'http://192.168.1.166:5000/predict'

# Sample data (replace this with your actual sample image data)
sample_data = {'image': 'C:\\Users\\surfc\\IdeaProjects\\FishID\\fishTrain\\clownfish\\201468278.jpg'}

# Send a POST request to the predict endpoint with the sample data
response = requests.post(url, json=sample_data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the predictions from the JSON response
    predictions = response.json()['predictions']
    print('Predictions:', predictions)
else:
    print('Error:', response.text)
