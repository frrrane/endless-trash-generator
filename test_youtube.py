import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

def test_connection():
    client_secrets_file = "client_secrets.json"
    # We use a 'readonly' scope just to verify the connection
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    print("🌐 Opening your browser for authentication...")
    # This will open a Chrome tab on your Chromebook
    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    # Fetch basic channel info to prove it works
    request = youtube.channels().list(part="snippet", mine=True)
    response = request.execute()

    print("\n✅ SUCCESS!")
    print(f"Connected to Channel: {response['items'][0]['snippet']['title']}")

if __name__ == "__main__":
    test_connection()