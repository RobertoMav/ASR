import argparse
import time
from pydub import AudioSegment
from pydub.playback import play
from pyaudio import PyAudio, paInt16

def record_audio(interval_seconds, output_filename):
    p = PyAudio()
    stream = p.open(format=paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    frames = []
    start_time = time.time()

    while True:
        data = stream.read(1024)
        frames.append(data)

        if time.time() - start_time >= interval_seconds:
            interval_audio = AudioSegment(
                b''.join(frames),
                frame_rate=44100,
                sample_width=2,
                channels=1
            )
            interval_audio.export(f"{output_filename}_{int(time.time())}.wav", format="wav")
            frames = []
            start_time = time.time()

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record audio in intervals.")
    parser.add_argument("--interval", type=int, default=10, help="Time interval for creating separate files in seconds.")
    parser.add_argument("--output", type=str, default="output", help="Output filename prefix.")

    args = parser.parse_args()

    record_audio(args.interval, args.output)
