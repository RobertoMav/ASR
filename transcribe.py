import whisper
import time
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Transcribe audio segments from folder.")
    parser.add_argument("--path", type=str, default='Audio/segments_5', help="Path to folder with audio segments.")
    args = parser.parse_args()
    return args.path


if __name__ == "__main__":
    path = parse_args()
    assert os.path.exists(path)
    start_time = time.time()
    model = whisper.load_model("medium")
    answer = ''
    results = []
    
    print("Starting transcription...")
    
    # checking if there are files in the folder named finished
    while not os.path.exists(f"{path}/finished.txt") or len(os.listdir(path)) != 2:
        print("Starting Loop, current file number:", len(os.listdir(path)))
        
        for filename in sorted(os.listdir(path)):
            file_path = os.path.join(path, filename)
            if filename.endswith(".wav") and filename.startswith("SILENCE"):
                    print(f"Processing file: {file_path}")
                    str_res = ''.join(results)
                    result = model.transcribe(file_path, word_timestamps=True, language="pt", fp16=False, prompt=f"Context: {str_res}")
                    print(f"\nTRANSCRIPTION: {result['text']}\n")
                    answer += result["text"]
                    if len(results) == 5:
                        results.pop(0)
                    results.append(result["text"])
                    print("--- %s seconds ---" % (time.time() - start_time))
                    os.rename(file_path, f"{path}/Processed/{filename}")
        time.sleep(1)
    
    print(f"\nFINAL TRANSCRIPTION: {answer}\n")
    print("--- %s seconds ---" % (time.time() - start_time))