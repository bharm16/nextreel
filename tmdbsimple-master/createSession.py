import requests

api_key = "89b32847c0525854de030aea3a8c5d9d"
request_token = "8c55549c56ad998c8d8e4937124605008f914bd2"  # Replace with the request token obtained in Step 2

# Create a session by making a POST request to the session endpoint
session_url = f"https://api.themoviedb.org/3/authentication/session/new?api_key={api_key}"
data = {
    "request_token": request_token
}

response = requests.post(session_url, json=data)
data = response.json()

if response.status_code == 200 and data.get("success"):
    session_id = data["session_id"]
    print(f"Session ID: {session_id}")
else:
    print("Failed to create a session.")

#9dda1966677ccd739156442ffba09047db32a541