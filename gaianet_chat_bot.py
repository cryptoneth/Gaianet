import requests
import time
from web3 import Web3
from eth_account import Account

def get_input(prompt):
    return input(prompt)

# Get URL from user
url = get_input("Please enter the URL: ")

# Get Gaianet API endpoint from user
api_endpoint = get_input("Please enter the Gaianet API endpoint: ")

# Get rest time between messages
rest_time = int(get_input("Please enter the rest time between messages in seconds: "))

# Get private key for wallet
private_key = get_input("Please enter your private key (be cautious!): ")

# Create an account from the private key
acct = Account.from_key(private_key)

# Get the public address from the account
address = acct.address

print(f"Wallet Address: {address}")

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
        full_url = f"{url}{api_endpoint}"
        
        # Sign the message with the wallet for authentication (if GaiaNet requires this)
        signature = acct.sign_message(message.encode('utf-8')).signature.hex()
        
        # Send message to Gaianet server
        payload = {
            'message': message,
            'address': address,
            'signature': signature  # Assuming GaiaNet uses this for authentication
        }
        
        try:
            response = requests.post(full_url, json=payload)
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
