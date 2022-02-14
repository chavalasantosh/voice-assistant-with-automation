import os
import glob
import re
from datetime import datetime
from mutagen.mp3 import MP3
from playsound import playsound
import pandas as pd


# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Directory of audio filenames
path_files = os.path.join(ROOT_DIR, "audiofiles")

# Get audio filenames and paths
# Experiment B
exp_B_filename_paths = glob.glob(os.path.join(ROOT_DIR, "audiofiles", "MD*mp3"))
exp_B_filenames = [f for f in os.listdir(path_files) if f.endswith(".mp3") and f.startswith("MD")]
print(exp_B_filenames)

def start_jukebox_B(list_file_paths, condition, group_id):

    # Define input playlist
    input_list = [f for f in list_file_paths]
    # track_names = [re.sub("^audiofiles\/","", f) for f in list_file_paths if f.endswith(".mp3")]
    track_names = [os.path.basename(f) for f in list_file_paths if f.endswith(".mp3")]

    def display_playlist(track_names):
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


    # Timer starts
    play_start_time = datetime.now()
    play_start_time_str = play_start_time.strftime("%d-%B-%Y %H:%M:%S")

    print(f"Started voice assistant control at: {play_start_time_str}")
    display_playlist(track_names)

    # Set default value to control loop
    value = "" # if Q-key is pressed value will change and break out of the loop

    # List to keep track of what is played
    logged_sequence = [str(condition), str(group_id)]

    while value.lower() != "q":
        # Input for the ENTER key press
        value = input()

        if(value == str(1)):
            alexa_statement = input_list[0]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length

            print("*" * 20)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(
                "\nPlaying: {}".format(re.sub("^\.\.\/audiofiles\/", "", alexa_statement)))
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")

            playsound(alexa_statement)

            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 20)

            logged_sequence.append(str(value) + "_" + re.sub("^\.\.\/audiofiles\/", "", alexa_statement))

            display_playlist(track_names)

        if (value == str(2)):
            alexa_statement = input_list[1]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length

            print("*" * 20)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(
                "\nPlaying: {}".format(re.sub("^\.\.\/audiofiles\/", "", alexa_statement)))
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")

            playsound(alexa_statement)

            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 20)

            logged_sequence.append(str(value) + "_" + re.sub("^\.\.\/audiofiles\/", "", alexa_statement))

            display_playlist(track_names)

    exit_time = datetime.now()
    exit_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
    print(f"Voice assistant control terminated by user at {exit_time_str}")

    # Compute total duration of session
    total_session_duration = exit_time - start_time

    # timestamps_df = pd.DataFrame([condition_id, play_start_time_str, exit_time_str, total_session_duration.seconds, (total_session_duration.seconds / 60)],
    #                              columns=["condition_id", "session_start", "session_finish", "session_duration_secs", "session_duration_mins"])

    seq_log_df = pd.DataFrame(logged_sequence, columns=["logged_sequence"])

    # output_timestamps_path = "Experiment_B_timestamps_" + str(condition_id) + ".csv"
    # output_seq_log_path = "Experiment_B_sequence_log_" + str(condition_id) + ".csv"

    # timestamps_df.to_csv("timestamps.csv", sep=",")
    seq_log_df.to_csv("seq.csv", sep=",")



# Run
start_jukebox_B(exp_B_filename_paths, "A", 1234)