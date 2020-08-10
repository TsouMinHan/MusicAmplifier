from pydub.utils import mediainfo
from pydub import AudioSegment
from pathlib import Path
import operator
import json
import math

def transfer_audio(file):
    try:
        return AudioSegment.from_file(f"{file}", format=f"{file.suffix[1:]}") # file.suffix is like .mp3 .
    except Exception as e:
        print(e)
        return None

def get_mode_num(auido_ls):
    dc = dict()
    for audio in auido_ls:
        db = round(audio.dBFS)
        if dc.get(db, ""):
            dc[db] += 1
        else:
            dc[db] = 1

    return max(dc.items(), key=operator.itemgetter(1))[0]

def export_audio(audio, path, tags): 
    audio.export(
        f"{path}",
        format="mp3",
        tags=tags
    )

if __name__ == '__main__':
    pass