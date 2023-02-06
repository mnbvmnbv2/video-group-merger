"""File for uploading of videos to youtube through API"""
# -*- coding: utf-8 -*-

import os
import json
import glob

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from paths import client_secret_key, main_folder


scopes = ["https://www.googleapis.com/auth/youtube.upload"]


def upload_from_json(path_to_channel: str) -> None:
    """Uploads videos to youtube based on what is in the json file

    Args:
        path_to_json (str): Path to json file which should be beside videos
    """
    # load in json as dictionary
    mergersdata = json.load(path_to_channel + "\\\\mergersdata.json")

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"

    # iterate over each video
    # iterate over group (videos)
    for idx, group in enumerate(mergersdata):
        # print name and which group out of total number of group is being processed
        print(f"{group['name']}, {idx + 1}/{len(mergersdata)}")

        # get merged status (not set in mergerdata)
        try:
            merged = group["merged"]
        except KeyError:
            merged = False

        try:
            uploaded = group["uploaded"]
        except KeyError:
            uploaded = False

        if not merged or uploaded:
            print("Is already uploaded or not merged")
            continue

        # set title, description etc.
        title = group["name"]
        description = "Chapters:\n"
        for idx, chapter in enumerate(group["chapters"]):
            description += f"{chapter}: {group['videos']}\n"
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
            f"{path_to_channel}\\\\{group['name']}", mimetype=None, resumable=True
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

        # set json group as finished uploading
        group["uploaded"] = True
        # update json-file
        with open(f"{path_to_channel}\\\\mergerdata.json", "w") as outfile:
            json.dump(mergersdata, outfile)


if __name__ == "__main__":
    # get channels
    channel_paths = glob.glob(main_folder + "Channels/*")

    for channel_path in channel_paths:
        # print current channel
        print(channel_path)
        # merge videos in channel
        upload_from_json(channel_path)
