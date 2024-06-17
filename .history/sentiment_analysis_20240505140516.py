import tweepy


# Define Twitter API credentials 
consumer_key = 'gC44j8IPEE9ipjhgl7CNbhhQd'
consumer_secret = 'Qld9VTiICB7ROAGWtq0FIxA63bPDxKBVSo5o4SCJmevaEoA3CT'


# Create an authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# Initiate the OAuth 1.a authorization process
auth_url = auth.get_authorization_url()

print(f"Open this URL in your browser to authorize the app: {auth_url}")

# Get verification PIN code after authorization
verifier = input("Enter the PIN code from the authorization page: ")

# Verify credentials and obtain access tokens
try:
  auth.get_access_token(verifier)
except tweepy.TweepyError as e:
  print("Error obtaining access tokens:", e)
  exit()

# Print the generated OAuth tokens (store them securely)
print("-" * 50)
print("Your OAuth 1.a Tokens:")
print(f"Access Token: {auth.access_token}")
print(f"Access Token Secret: {auth.access_token_secret}")
print("-" * 50)
