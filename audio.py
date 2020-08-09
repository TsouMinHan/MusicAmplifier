from pydub.utils import mediainfo
from pydub import AudioSegment
from pathlib import Path
import operator
import json
import math

import audio

def transfer_audio(file):
    try:
        return AudioSegment.from_file(f"{file}", format=f"mp3")
    except Exception as e:
        print(e)
        return None

if __name__ == "__main__":
    a = transfer_audio("C:\\Users\\Tsou\\Desktop\\program\\python\\MusicAmplifier\\Adventure Time - Francis forever.mp3")
    print(mediainfo("C:\\Users\\Tsou\\Desktop\\program\\python\\MusicAmplifier\\Adventure Time - Francis forever.mp3").get('TAG',None))