from pydub.utils import mediainfo
from traceback import print_exc
from pathlib import Path
import math
import json
import eel

import audio_script

JSON_FILE = "./doc.json"

def get_director():
    with open(JSON_FILE, "r", encoding="utf8") as json_file:
        data = json.load(json_file)
    
    return data

def setup_html():
    data = get_director()    
    eel.set_directory(data)

def save_record(input_directory, output_directory, amplitude):
    dc = {
        "input_directory": input_directory,
        "output_directory": output_directory,
        "amplitude": amplitude
    }

    with open(JSON_FILE, 'w', encoding='utf-8') as json_file:
        json.dump(dc, json_file)

def process_one(audio, db, f):
    gap = round(audio.dBFS) - db

    if gap==0:
        new_file = audio - f

    elif gap>0:
        new_file = audio + gap - f
    
    else:
        new_file = audio - gap - f

    return new_file

def filter_audio_format(file: Path):
    file_format_ls = [".wav", ".mp3", ".flac"]

    if file.suffix in file_format_ls:
        return True
    return False

def execute_audio(input_directory, output_directory, mode, db_num):  
    input_directory = Path(input_directory)
    output_directory = Path(output_directory)

    eel.set_msg("讀取檔案中！請稍後！")
    # lsit of Path.
    path_ls = sorted(
        filter(filter_audio_format, input_directory.rglob('*'))
    )

    # list of AudioSegment.
    auido_ls = list(
        map(
            lambda file: audio_script.transfer_audio(file),
            path_ls
        )
    )

    db_num = db_num if mode !="average" else audio_script.get_mode_num(auido_ls)
    
    for i in range(len(auido_ls)):          
        audio = auido_ls[i]
        path = Path(output_directory, path_ls[i].name)
        tags = mediainfo(f"{path_ls[i].name}").get('TAG',None)
        f = math.modf(audio.dBFS)[0]

        if mode=="plus":
            new_file = audio + db_num - f

        elif mode=="minus":
            new_file = audio - db_num - f
        
        else: # old and average mode.
            new_file = process_one(audio, db_num, f)

        audio_script.export_audio(new_file, path, tags)

        eel.set_msg(f"目前進度：{i+1} / {len(auido_ls)} === {round(audio.dBFS)}db > {db_num}db")
        eel.set_progressbar((i+1)/len(auido_ls)*100)

    return db_num

@eel.expose
def run(data):
    input_directory = data["input"]
    output_directory = data["output"]
    mode = data["mode"]
    num = data["num"]

    try:        
        db_num = execute_audio(input_directory, output_directory, mode, num)
        save_record(input_directory, output_directory, db_num)
        return "Finished !!"

    except Exception as e:   
        print_exc(e)     
        return str(e)

if __name__ == '__main__':
    eel.init("web")

    setup_html()

    eel.start("main.html", size=(800, 350))