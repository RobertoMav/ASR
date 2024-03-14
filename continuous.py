import subprocess
import multiprocessing
from datetime import datetime


def run_file(file, *args):
    subprocess.run(['python', file] + list(args)) 

def main():
    NOW = f'Audio/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'
    MIC = 'mic.py'
    mic_args = ['--interval', str(15), '--path', NOW]
    TRANSCRIBE = 'transcribe.py'
    trans_args = ['--path', NOW]

    mic_process = multiprocessing.Process(target=run_file, args=(MIC, *mic_args))
    trans_process = multiprocessing.Process(target=run_file, args=(TRANSCRIBE, *trans_args)) 

    mic_process.start()
    trans_process.start()
    
    mic_process.join()  
    trans_process.join()


if __name__ == '__main__':
    main()
