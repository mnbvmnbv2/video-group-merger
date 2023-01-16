# -*- coding: utf-8 -*-

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from paths import client_secret_key

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"

    # about
    title = "test-vid-1"
    description = "This is a test upload\n Test: 10:00"
    tags = ["Education"]

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret_key, scopes
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    media = MediaFileUpload(
        "./Channels/ADA/session1.mp4", mimetype=None, resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        autoLevels=True,
        notifySubscribers=False,
        stabilize=True,
        body={
            "snippet": {"title": title, "description": description, "tags": tags},
            "status": {"madeForKids": False, "privacyStatus": "private"},
        },
        media_body=media,
    )
    # response = request.execute()

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
        print("Upload Complete!")

    print(response)


if __name__ == "__main__":
    main()
