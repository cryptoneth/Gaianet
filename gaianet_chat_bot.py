import requests
import time

def get_input(prompt):
    return input(prompt)

# Get URL from user
url = get_input("Please enter the URL: ")

# Get Gaianet API endpoint from user
api_endpoint = get_input("Please enter the Gaianet API endpoint: ")

# Get rest time between messages
rest_time = int(get_input("Please enter the rest time between messages in seconds: "))

# Get messages from user
messages = []
while True:
    message = get_input("Enter a message (or press enter to finish): ")
    if message == "":
        break
    messages.append(message)

print(f"Starting chat with {len(messages)} messages, waiting {rest_time} seconds between each message.")

while True:
    for message in messages:
        # Construct the full URL for the API request
        full_url = f"{url}{api_endpoint}"
        
        # Send message to Gaianet server
        payload = {'message': message}
        try:
            response = requests.post(full_url, data=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            print(f"Message sent: {message}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error sending message '{message}': {e}")

        # Wait for specified rest time
        time.sleep(rest_time)

    # Option to continue or stop the script after all messages are sent
    if get_input("Press enter to send messages again, or 'q' to quit: ").lower() == 'q':
        break

print("Script terminated.")
