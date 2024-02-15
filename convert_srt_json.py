import os
import json
import srt
from pathlib import Path

dir = os.fsencode("F:/Code/podaboutlist/v2/transcripts_raw")
target = os.fsencode("F:/Code/podaboutlist/v2/transcripts_raw_json")
meta = os.fsencode("F:/Code/podaboutlist/v2/transcripts_metadata")

for file in os.listdir(dir):
    src_filename = os.path.join(os.fsdecode(dir), os.fsdecode(file))
    
    lines = []

    with open(src_filename, 'r', encoding='utf-8') as src_file:
        data = srt.parse(src_file)
        for i in data:
            lines.append({"text": i.content, "start": i.start.total_seconds(), "end": i.end.total_seconds()})
        
    json_data = {"lines": lines}


    meta_filename = os.path.join(os.fsdecode(meta), Path(src_filename).stem + ".json")

    with open(meta_filename, 'r', encoding='utf-8') as meta_file:
        metadata = json.load(meta_file)
        json_data["title"] = metadata["title"]
        json_data["link"] = metadata["link"]
        json_data["date"] = metadata["published"]
        json_data["id"] = metadata["id"]

    target_filename = os.path.join(os.fsdecode(target), Path(src_filename).stem + ".json")

    with open(target_filename, 'w', encoding='utf-8') as target_file:
        json.dump(json_data, target_file)