import os
import sounddevice as sd
import threading
import numpy as np
import argparse
from pydub import AudioSegment, silence
from pynput import keyboard
from datetime import datetime


def parse_args():

    parser = argparse.ArgumentParser(description="Record audio in intervals.")
    parser.add_argument("--interval", type=int, default=5, help="Time interval for creating separate files in seconds.")
    parser.add_argument("--path", type=str, default=f"Audio/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}", help="Current time as folder name")
    args = parser.parse_args()
    return args.interval, args.path

def on_key_release(key):
    if key == keyboard.Key.esc:
        # Stop the recording and save the final segment
        save_segment(True)
        print("\n\n\nRecording stopped.\n\n\n")

        # move files to processed folder
        for filename in sorted(os.listdir(output_folder)):
            file_path = os.path.join(output_folder, filename)
            if filename.endswith(".wav") and not filename.startswith("SILENCE"):
                os.rename(file_path, f"{output_folder}/Processed/{filename}")

        with open(f"{output_folder}/finished.txt", "w") as f:
            print("Writing Finished File")
            f.write("Finished")

        return False

def save_segment(last=False):
    global audio_data, segment_number, foreground, full_sound
    audio_segment = AudioSegment(data=np.array(audio_data).tobytes(),
                 sample_width=2,
                 frame_rate=sample_rate,
                 channels=1)
    dBFS=audio_segment.dBFS

    # Use threading to process the audio segment asynchronously
    process_thread = threading.Thread(target=process_audio, args=(audio_segment, dBFS, last))
    process_thread.start()

    full_sound += audio_segment
    segment_number += 1
    audio_data.clear()

def process_audio(audio_segment, dBFS, last):
    global segment_number, foreground

    silent_split = silence.split_on_silence(audio_segment, silence_thresh=dBFS-16, min_silence_len=500, keep_silence=100)
    for idx, splits in enumerate(silent_split):
        filename = f"{output_folder}/SILENCE_{datetime.now().strftime('%H-%M-%S')}_{idx}.wav"
        print(f"Exporting file: {filename}")
        splits.export(f"{filename}", format="wav")
        foreground += splits

    if last:
        full_sound.export(f"{output_folder}/FULL_SOUND.wav", format="wav")
        foreground.export(f"{output_folder}/FOREGROUND.wav", format="wav")

def record_audio():
    print("Recording started, press 'Esc' to stop.")
    with sd.InputStream(callback=callback, channels=1, dtype=np.int16):
        with keyboard.Listener(on_release=on_key_release) as listener:
            listener.join()

def callback(indata, frames, time, status):
    global audio_data
    if status:
        print(status, flush=True)

    audio_data.extend(indata.flatten())

    # Check if it's time to save a new segment
    if len(audio_data) >= (sample_rate * segment_duration):
        save_segment()

if __name__ == "__main__":
    segment_duration, output_folder = parse_args()
    sample_rate = 44100

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        os.makedirs(f'{output_folder}/Processed')

    segment_number = 1
    audio_data = []
    full_sound = AudioSegment.empty()
    foreground = AudioSegment.empty()

    # Create a separate thread for recording audio
    audio_thread = threading.Thread(target=record_audio)
    audio_thread.start()

    # Continue processing in the main thread
    audio_thread.join()
