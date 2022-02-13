import os
import glob
import re
from time import time
from datetime import datetime
from mutagen.mp3 import MP3
from playsound import playsound


# Get project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory of audio filenames
path_files = os.path.join(ROOT_DIR, "audiofiles")

# Get audio filenames and paths

# Experiment B
exp_B_filename_paths = glob.glob("audiofiles/MD*mp3")
exp_B_filenames = [f for f in os.listdir(path_files) if f.endswith(".mp3") and f.startswith("MD")]


input_list = exp_B_filename_paths
track_names = exp_B_filenames

# Timer starts
start_time = datetime.now()
start_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
value = ""

print(f"\nType number and press ENTER to play statement:\n"
      f"1: {track_names[0]}\n"
      f"2: {track_names[1]}\n"
      f"3: {track_names[2]}\n"
      f"4: {track_names[3]}\n"
      f"5: {track_names[4]}\n"
      f"6: {track_names[5]}\n"
      f"7: {track_names[6]}\n"
      f"8: {track_names[7]}\n"
      "Type Q and press ENTER to stop program.\n")

while value.lower() != "q":
    # Input for the ENTER key press
    value = input()

    if(value == str(1)):
        alexa_statement = input_list[0]
        audio = MP3(alexa_statement)
        audio_duration = audio.info.length

        print("*" * 20)
        start_time = datetime.now()
        start_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
        print(f"Started playing at: {start_time_str}")
        print(
            "\nPlaying: {}".format(re.sub("^audiofiles\/", "", alexa_statement)))
        print(f"Duration of statement: {audio_duration:.2f} secs.\n")

        playsound(alexa_statement)

        finish_time = datetime.now()
        finish_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
        print(f"Finished statement at: {finish_time_str}")
        print("*" * 20)

        print(f"\nType number and press ENTER to play statement:\n"
              f"1: {track_names[0]}\n"
              f"2: {track_names[1]}\n"
              f"3: {track_names[2]}\n"
              f"4: {track_names[3]}\n"
              f"5: {track_names[4]}\n"
              f"6: {track_names[5]}\n"
              f"7: {track_names[6]}\n"
              f"8: {track_names[7]}\n"
              "Type Q and press ENTER to stop program.\n")

    if (value == str(2)):
        alexa_statement = input_list[1]
        audio = MP3(alexa_statement)
        audio_duration = audio.info.length

        print("*" * 20)
        start_time = datetime.now()
        start_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
        print(f"Started playing at: {start_time_str}")
        print(
            "\nPlaying: {}".format(re.sub("^audiofiles\/", "", alexa_statement)))
        print(f"Duration of statement: {audio_duration:.2f} secs.\n")

        playsound(alexa_statement)

        finish_time = datetime.now()
        finish_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
        print(f"Finished statement at: {finish_time_str}")
        print("*" * 20)

        print(f"\nType number and press ENTER to play statement:\n"
              f"1: {track_names[0]}\n"
              f"2: {track_names[1]}\n"
              f"3: {track_names[2]}\n"
              f"4: {track_names[3]}\n"
              f"5: {track_names[4]}\n"
              f"6: {track_names[5]}\n"
              f"7: {track_names[6]}\n"
              f"8: {track_names[7]}\n"
              "Type Q and press ENTER to stop program.\n")

exit_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
print(f"Alexa controller was terminated by user at {exit_time_str}")