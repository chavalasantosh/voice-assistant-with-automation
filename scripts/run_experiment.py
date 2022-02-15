import os
import sys
import glob
from datetime import datetime
import pandas as pd
from mutagen.mp3 import MP3
from playsound import playsound
import time


# Get project root directory
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories of audio filenames

# Voice assistant introduction
path_va_intro_active = os.path.join(ROOT_DIR, "audiofiles", "va_intro", "active")
path_va_intro_passive = os.path.join(ROOT_DIR, "audiofiles", "va_intro", "passive")
# Voice assistant interaction audio
path_inter = os.path.join(ROOT_DIR, "audiofiles", "inter")
# Experiment A file paths
path_files_exp_a_active = os.path.join(ROOT_DIR, "audiofiles", "exp_a", "active")
path_files_exp_a_passive = os.path.join(ROOT_DIR, "audiofiles", "exp_a", "passive")
# Experiment B file paths
path_files_exp_b_active_pat1 = os.path.join(ROOT_DIR, "audiofiles", "exp_b", "active", "pattern_1")
path_files_exp_b_active_pat2 = os.path.join(ROOT_DIR, "audiofiles", "exp_b", "active", "pattern_2")
path_files_exp_b_passive_pat1 = os.path.join(ROOT_DIR, "audiofiles", "exp_b", "passive", "pattern_1")
path_files_exp_b_passive_pat2 = os.path.join(ROOT_DIR, "audiofiles", "exp_b", "passive", "pattern_2")


# Experiment selector
def select_exp():
    exp_selected = input(f"\nType key then ENTER to select condition:\n"
                         f"A: Experiment A: VA agency\n"
                         f"B: Experiment B: Type of Information x VA autonomy\n")

    if (exp_selected.lower() == "a"):
        exp_tag = "exp_A"
        exp_str = "Experiment A: VA agency"
        print(f"Starting {exp_str}")
    elif (exp_selected.lower() == "b"):
        exp_tag = "exp_B"
        exp_str = "Experiment B: Type of Information x VA autonomy"
        print(f"Starting {exp_str}")
    else:
        exp_str = "Invalid"
        print(f"Terminated. Choice is {exp_str}")
        sys.exit()
    return exp_tag


# Experiment A condition selector
def exp_A_select_condition():
    # Condition selector
    cond_selected = input(f"\nType key then ENTER to select condition:\n"
                          f"1: Active\n"
                          f"2: Passive\n")

    if (cond_selected == str(1)):
        cond_tag = "exp_A_active"
        cond_str = "Active"
        print(f"Starting condition: {cond_str}")
    elif (cond_selected == str(2)):
        cond_tag = "exp_A_passive"
        cond_str = "Passive"
        print(f"Starting condition: {cond_str}")
    else:
        cond_str = "Invalid"
        print(f"Terminated. Choice is {cond_str}")
        sys.exit()
    return cond_tag


# Experiment B condition selector
def exp_B_select_condition():
    # Condition selector
    cond_selected = input(f"\nType number and press ENTER to select condition:\n"
                          f"1: Active - Pattern 1\n"
                          f"2: Active - Pattern 2\n"
                          f"3: Passive - Pattern 1\n"
                          f"4: Passive - Pattern 2\n")

    if (cond_selected == str(1)):
        cond_tag = "exp_B_active_pat1"
        cond_str = "Active - Pattern 1"
        print(f"Starting condition: {cond_str}")
    elif (cond_selected == str(2)):
        cond_tag = "exp_B_active_pat2"
        cond_str = "Active - Pattern 2"
        print(f"Starting condition: {cond_str}")
    elif (cond_selected == str(3)):
        cond_tag = "exp_B_passive_pat1"
        cond_str = "Passive - Pattern 1"
        print(f"Starting condition: {cond_str}")
    elif (cond_selected == str(4)):
        cond_tag = "exp_B_passive_pat2"
        cond_str = "Passive - Pattern 2"
        print(f"Starting condition: {cond_str}")
    else:
        cond_str = "Invalid"
        print(f"Terminated. Choice is {cond_str}")
        sys.exit()
    return cond_tag


def exp_A(list_file_paths, selected_exp, selected_cond):
    # Start dictionary to capture data
    results = {"experiment": selected_exp,
               "condition": selected_cond,
               "session_start": None,
               "session_finish": None,
               "session_duration_secs": None,
               "recorded_sequence": []}

    # Define input playlist
    input_list = [f for f in list_file_paths]
    track_names = [os.path.basename(f) for f in list_file_paths if f.endswith(".mp3")]

    def display_playlist(track_names):
        print("\nType key and press ENTER to play statement:\n")
        for idx, track in enumerate(track_names, start=1):
            print(f"{idx}: {track}")
        print("\n(Y): 'Yes, I do'")
        print("(N): 'Sorry, no info'")
        print("(R): 'Would you like me to repeat?'")
        print("\nType Q and press ENTER to stop program.\n")

    # Define VA introduction files
    if(selected_cond in ["exp_A_active", "exp_B_active_pat1", "exp_B_active_pat2"]):
        va_intro_list = glob.glob(os.path.join(path_va_intro_active, "*.mp3"))
        va_intro_list.sort()
    elif(selected_cond in ["exp_A_passive", "exp_B_passive_pat1", "exp_B_passive_pat2"]):
        va_intro_list = glob.glob(os.path.join(path_va_intro_passive, "*.mp3"))
        va_intro_list.sort()

    # Define interactive audio
    inter_yes = os.path.join(path_inter, "inter_yesido.mp3")
    inter_noinfo = os.path.join(path_inter, "inter_noinfo.mp3")
    inter_repeat = os.path.join(path_inter, "inter_repeat.mp3")


    # Timer starts
    play_start_time = datetime.now()
    play_start_time_str = play_start_time.strftime("%d-%B-%Y %H:%M:%S")

    print(f"Started voice assistant control at: {play_start_time_str}")

    # VA introduces itself:
    playsound(va_intro_list[0])
    playsound(va_intro_list[1])

    # Display playlist options
    display_playlist(track_names)

    # Set default value to control loop
    value = ""  # if Q-key is pressed value will change and break out of the loop

    while value.lower() != "q":
        # Input for the ENTER key press
        value = input()

        if (value.lower() == "y"):
            alexa_statement = inter_yes
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append("react_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value.lower() == "n"):
            alexa_statement = inter_noinfo
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append("react_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value.lower() == "r"):
            alexa_statement = inter_repeat
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append("react_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(1)):
            alexa_statement = input_list[0]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(2)):
            alexa_statement = input_list[1]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(3)):
            alexa_statement = input_list[2]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(4)):
            alexa_statement = input_list[3]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(5)):
            alexa_statement = input_list[4]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(6)):
            alexa_statement = input_list[5]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(7)):
            alexa_statement = input_list[6]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(8)):
            alexa_statement = input_list[7]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)


        if (value == str(9)):
            alexa_statement = input_list[8]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(10)):
            alexa_statement = input_list[9]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(11)):
            alexa_statement = input_list[10]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(12)):
            alexa_statement = input_list[11]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(13)):
            alexa_statement = input_list[12]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(14)):
            alexa_statement = input_list[13]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(15)):
            alexa_statement = input_list[14]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(16)):
            alexa_statement = input_list[15]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

    exit_time = datetime.now()
    exit_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
    print(f"Voice assistant control terminated by user at {exit_time_str}")

    # Compute total duration of session
    total_session_duration = exit_time - play_start_time

    # Add duration data to dictionary
    results["session_start"] = play_start_time_str
    results["session_finish"] = exit_time_str
    results["session_duration_secs"] = total_session_duration.seconds

    # # Define output filename based on experimental condition
    current_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
    output_filename = selected_cond + "_" + current_time + ".csv"

    # Save results to file
    results_df = pd.DataFrame({key: pd.Series(value) for key, value in results.items()})
    results_df.to_csv(output_filename, index=False)

    print("Saved the following data:")
    print(results_df)


def exp_B(list_file_paths, selected_exp, selected_cond):
    # Start dictionary to capture data
    results = {"experiment": selected_exp,
               "condition": selected_cond,
               "session_start": None,
               "session_finish": None,
               "session_duration_secs": None,
               "recorded_sequence": []}

    # Define input playlist
    input_list = [f for f in list_file_paths]
    track_names = [os.path.basename(f) for f in list_file_paths if f.endswith(".mp3")]

    def display_playlist(track_names):
        print("\nType key and press ENTER to play statement:\n")
        for idx, track in enumerate(track_names, start=1):
            print(f"{idx}: {track}")
        print("\n(Y): 'Yes, I do'")
        print("(N): 'Sorry, no info'")
        print("(R): 'Would you like me to repeat?'")
        print("\nType Q and press ENTER to stop program.\n")

    # Define VA introduction files
    if(selected_cond in ["exp_A_active", "exp_B_active_pat1", "exp_B_active_pat2"]):
        va_intro_list = glob.glob(os.path.join(path_va_intro_active, "*.mp3"))
        va_intro_list.sort()
    elif(selected_cond in ["exp_A_passive", "exp_B_passive_pat1", "exp_B_passive_pat2"]):
        va_intro_list = glob.glob(os.path.join(path_va_intro_passive, "*.mp3"))
        va_intro_list.sort()

    # Define interactive audio
    inter_yes = os.path.join(path_inter, "inter_yesido.mp3")
    inter_noinfo = os.path.join(path_inter, "inter_noinfo.mp3")
    inter_repeat = os.path.join(path_inter, "inter_repeat.mp3")


    # Timer starts
    play_start_time = datetime.now()
    play_start_time_str = play_start_time.strftime("%d-%B-%Y %H:%M:%S")

    print(f"Started voice assistant control at: {play_start_time_str}")

    # VA introduces itself:
    playsound(va_intro_list[0])
    playsound(va_intro_list[1])

    # Display playlist options
    display_playlist(track_names)

    # Set default value to control loop
    value = ""  # if Q-key is pressed value will change and break out of the loop

    while value.lower() != "q":
        # Input for the ENTER key press
        value = input()

        if (value.lower() == "y"):
            alexa_statement = inter_yes
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append("react_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value.lower() == "n"):
            alexa_statement = inter_noinfo
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append("react_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value.lower() == "r"):
            alexa_statement = inter_repeat
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append("react_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(1)):
            alexa_statement = input_list[0]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(2)):
            alexa_statement = input_list[1]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(3)):
            alexa_statement = input_list[2]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(4)):
            alexa_statement = input_list[3]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(5)):
            alexa_statement = input_list[4]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(6)):
            alexa_statement = input_list[5]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(7)):
            alexa_statement = input_list[6]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

        if (value == str(8)):
            alexa_statement = input_list[7]
            audio = MP3(alexa_statement)
            audio_duration = audio.info.length
            print("*" * 40)
            start_time = datetime.now()
            start_time_str = start_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Started playing at: {start_time_str}")
            print(f"\nPlaying: {os.path.basename(alexa_statement)}")
            print(f"Duration of statement: {audio_duration:.2f} secs.\n")
            playsound(alexa_statement)
            finish_time = datetime.now()
            finish_time_str = finish_time.strftime("%d-%B-%Y %H:%M:%S")
            print(f"Finished statement at: {finish_time_str}")
            print("*" * 40)
            results["recorded_sequence"].append(str(value) + "_" + os.path.basename(alexa_statement))
            display_playlist(track_names)

    exit_time = datetime.now()
    exit_time_str = datetime.now().strftime("%d-%B-%Y %H:%M:%S")
    print(f"Voice assistant control terminated by user at {exit_time_str}")

    # Compute total duration of session
    total_session_duration = exit_time - play_start_time

    # Add duration data to dictionary
    results["session_start"] = play_start_time_str
    results["session_finish"] = exit_time_str
    results["session_duration_secs"] = total_session_duration.seconds

    # # Define output filename based on experimental condition
    current_time = time.strftime("%m.%d.%y %H:%M", time.localtime())
    output_filename = selected_cond + "_" + current_time + ".csv"

    # Save results to file
    results_df = pd.DataFrame({key: pd.Series(value) for key, value in results.items()})
    results_df.to_csv(output_filename, index=False)

    print("Saved the following data:")
    print(results_df)


# Run experiment

# Selection of experiment via user input
selected_exp = select_exp()

# Automatically open list of conditions for selected experiment so user can choose the desired condition
if (selected_exp == "exp_A"):
    selected_cond = exp_A_select_condition()
elif (selected_exp == "exp_B"):
    selected_cond = exp_B_select_condition()
else:
    selected_cond = None

# Define playlist based on selected experiment and respective condition
if (selected_cond == "exp_A_active"):
    # Get audio filenames and paths
    playlist_paths = glob.glob(os.path.join(path_files_exp_a_active, "*mp3"))
    playlist_paths.sort()
    print(playlist_paths)
elif (selected_cond == "exp_A_passive"):
    # Get audio filenames and paths
    playlist_paths = glob.glob(os.path.join(path_files_exp_a_passive, "*mp3"))
    playlist_paths.sort()
    print(playlist_paths)
elif (selected_cond == "exp_B_active_pat1"):
    # Get audio filenames and paths
    playlist_paths = glob.glob(os.path.join(path_files_exp_b_active_pat1, "*mp3"))
    playlist_paths.sort()
    print(playlist_paths)
elif (selected_cond == "exp_B_active_pat2"):
    # Get audio filenames and paths
    playlist_paths = glob.glob(os.path.join(path_files_exp_b_active_pat2, "*mp3"))
    playlist_paths.sort()
    print(playlist_paths)
elif (selected_cond == "exp_B_passive_pat1"):
    # Get audio filenames and paths
    playlist_paths = glob.glob(os.path.join(path_files_exp_b_passive_pat1, "*mp3"))
    print(playlist_paths)
elif (selected_cond == "exp_B_passive_pat2"):
    # Get audio filenames and paths
    playlist_paths = glob.glob(os.path.join(path_files_exp_b_passive_pat2, "*mp3"))
    playlist_paths.sort()
    print(playlist_paths)


if(selected_exp == "exp_A"):
    start_confirm = input("Press (S) to start.")
    if (start_confirm.lower() == "s"):
        exp_A(playlist_paths, selected_exp, selected_cond)
    else:
        sys.exit("Interrupted.")

elif(selected_exp == "exp_B"):
    start_confirm = input("Press (S) to start.")
    if (start_confirm.lower() == "s"):
        exp_B(playlist_paths, selected_exp, selected_cond)
    else:
        sys.exit("Interrupted.")

