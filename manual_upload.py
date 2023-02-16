"""File for creating easy copy paste for manual upload"""
import glob
import json

from paths import main_folder


def create_descriptions(folder: str, channel: str) -> None:
    """Create mergersdata json file in the channel folder

    Args:
        folder (str): Path to channel folder
        channel (str): Channel in channel folder
    """

    # read
    path = f"{folder}\\mergerdata.json"
    try:
        with open(path, "r") as f:
            js = json.loads(f.read())
            for group in js:
                desc_filename = f'{folder}\\{group["name"]}.txt'
                output = ""
                for idx, video_name in enumerate(group["videos"]):
                    output += f'{group["chapters"][idx]}: {video_name}\n'
                with open(desc_filename, "w") as out_file:
                    out_file.write(output)
    except FileNotFoundError:
        return


if __name__ == "__main__":
    # get a list of channels
    channels = glob.glob(main_folder + "Channels/*")
    print(channels)
    # iterate channels
    for channel in channels:
        # print current folder
        channel_name = channel.split("\\")[-1]
        print(channel_name)
        # create metadata for the folder
        create_descriptions(channel, channel_name)
