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

def export_audio(audio, path):    
    audio.export(f"{path}", format="mp3")

def get_doc():
    with open("./doc.json", "r", encoding="utf8") as json_file:
        data = json.load(json_file)
    
    return data

def filter_audio_format(file: Path):
    file_format_ls = [".wav", ".mp3"]

    if file.suffix in file_format_ls:
        return True
    return False

def get_mode(auido_ls):
    dc = dict()
    for audio in auido_ls:
        db = round(audio.dBFS)
        if dc.get(db, ""):
            dc[db] += 1
        else:
            dc[db] = 1

    return max(dc.items(), key=operator.itemgetter(1))[0]

def export_audio(audio, mode_db, path, tags):
    gap = round(audio.dBFS) - mode_db
    f = math.modf(audio.dBFS)[0]
    
    # adjust db and create new AudioSegment.
    if gap==0:
        new_file = audio - f

    elif gap>0:
        new_file = audio + gap - f
    
    else:
        new_file = audio - gap - f
    
    new_file.export(
        f"{path}",
        format="mp3",
        tags=tags
    )

if __name__ == '__main__':
    doc_dc = get_doc()

    DIRECTORY = Path(doc_dc["directory"])
    EXPORT_DIRECTORY = Path(doc_dc["export_directory"])

    # lsit of Path.
    path_ls = sorted(
        filter(filter_audio_format, DIRECTORY.rglob('*'))
    )

    # list of AudioSegment.
    auido_ls = list(
        map(lambda file: transfer_audio(file), path_ls)
    )

    mode_db = get_mode(auido_ls)

    for i in range(len(auido_ls)):
        audio = auido_ls[i]
        path = Path(EXPORT_DIRECTORY, path_ls[i].name)
        tags = mediainfo(f"{path_ls[i].name}").get('TAG',None)
        export_audio(audio, mode_db, path, tags)
