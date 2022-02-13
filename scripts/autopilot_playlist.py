import os
import glob
import re
import time
from datetime import datetime
from mutagen.mp3 import MP3
from playsound import playsound

# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory of audio filenames
path_files = os.path.join(ROOT_DIR, "audiofiles")

# Get audio filenames and paths

# Experiment A
exp_A_filename_paths = glob.glob("audiofiles/DS*mp3", root_dir=ROOT_DIR)
exp_A_filenames = [f for f in os.listdir(path_files) if f.endswith(".mp3") and f.startswith("DS")]
# Experiment B
exp_B_filename_paths = glob.glob("audiofiles/MD*mp3", root_dir=ROOT_DIR)
exp_B_filenames = [f for f in os.listdir(path_files) if f.endswith(".mp3") and f.startswith("MD")]


# Create audio playliosts counterbalancing for Type of Information Provided

# all_mantain_items = [re.search(r".*maintaining.mp3", i).group(0) for i in exp_A_filename_paths if re.search(r".*maintaining.mp3", i)]
# all_reducing_items = [re.search(r".*reducing.mp3", i).group(0) for i in exp_A_filename_paths if re.search(r".*reducing.mp3", i)]
#
# print(all_mantain_items)
# print(all_reducing_items)
#
# print("maintaining item list")
# for count, item in enumerate(all_mantain_items):
#     print(f"{count} : {item}")
#
# print("reducing item list")
# for count, item in enumerate(all_reducing_items):
#     print(f"{count} : {item}")

# R M M R M R R M
seq_1 = ["audiofiles/DS1_reducing.mp3", "audiofiles/DS2_maintaining.mp3", "audiofiles/DS3_maintaining.mp3", "audiofiles/DS4_reducing.mp3",
         "audiofiles/DS5_maintaining.mp3", "audiofiles/DS6_reducing.mp3", "audiofiles/DS7_reducing.mp3", "audiofiles/DS8_maintaining.mp3"]

# M R R M R M M R
seq_2 = ["audiofiles/DS1_maintaining.mp3", "audiofiles/DS2_reducing.mp3", "audiofiles/DS3_reducing.mp3", "audiofiles/DS4_maintaining.mp3",
         "audiofiles/DS5_reducing.mp3", "audiofiles/DS6_maintaining.mp3", "audiofiles/DS7_maintaining.mp3", "audiofiles/DS8_reducing.mp3"]


# Test lists
testlist1 = exp_A_filename_paths[0:3]
print(testlist1)

testlist2 = exp_B_filename_paths[0:3]
print(testlist2)

# Plays input mp3 playlist in sequence without user interface. Once it starts it cannot be stopped.

# Arguments:
#  playlist = sequence of audio filenames to be played, follows order of audio filenames in input list.
#  pause_duration_secs = how many seconds of pause between playing audio files

def play_unstoppable_audio_sequence(playlist, pause_duration_secs):
    if (isinstance(pause_duration_secs, int) and playlist is not None):
        playlist_length = len(playlist)
        playlist_start_timestamp = datetime.now()
        playlist_start_timestamp_str = playlist_start_timestamp.strftime("%d-%B-%Y %H:%M:%S")
        print(f"\nPlaylist initiated in: {playlist_start_timestamp_str}")
        print(f"Nr. of statements in the playlist: {playlist_length}.")

        start_action = input(
            "\nPress (S) followed by (Enter) to START the playlist.\n"
            "Press (any other key) followed by (Enter) to QUIT.")

        if (start_action.lower() == "s"):
            for count, audiofile in enumerate(playlist, start=1):
                audio_start_time = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
                audio = MP3(audiofile)
                audio_duration = audio.info.length
                print("\nPlaying: {} [{} / {}]".format(re.sub("^audiofiles\/", "", audiofile), count, playlist_length))
                print(f"Started playing at: {audio_start_time}")
                print(f"Duration of statement: {audio_duration:.2f} secs.")
                playsound(audiofile)
                if (count < playlist_length):
                    print(f"\nNext statement will start in {pause_duration_secs} secs...")
                    time.sleep(pause_duration_secs)
                else:
                    finish_time = datetime.now()
                    finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
                    playlist_full_duration = finish_time - playlist_start_timestamp
                    print("\nFinished!")
                    print(f"Sequence completed in: {finish_time_str}")
                    print(
                        f"Full duration of playlist: {round(playlist_full_duration.seconds / 60, 2)} minutes, or {round(playlist_full_duration.seconds, 2)} seconds.")

                time.sleep(pause_duration_secs)
        else:
            print("Playlist aborted.")

    else:
        raise ValueError(
            "Arguments must be a list of filename paths and an integer indicating the desired interval of silence between playing audio files")


# Test function

play_unstoppable_audio_sequence(seq_1, 1)
