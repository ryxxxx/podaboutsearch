import time
import feedparser
import json
import os.path
import requests
import re
import whisperx

dt=time.time()

d = feedparser.parse('https://anchor.fm/s/da4e26b0/podcast/rss')

print("Loaded RSS (took %ss)" % str(time.time()-dt))
dt=time.time()

device = "cuda" 
audio_file = "F:/Code/podaboutlist/currentFile.mp3"
batch_size = 16 # reduce if low on GPU mem
compute_type = "float32" # change to "int8" if low on GPU mem (may reduce accuracy)
model_dir = "F:/Code/podaboutlist/"
model = whisperx.load_model("tiny.en", device, compute_type=compute_type, download_root=model_dir)

print("Loaded model (took %ss)" % str(time.time()-dt))

for i in d.entries:
    if "teaser" in i.title.lower() or "unlocked" in i.title.lower():
        print("Skipped episode \"%s\": Teaser for or unlocked premium episode." % i.title)
        continue
    dirty = i.title
    clean = re.sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", "-", dirty)
    jsonFile = "F:/Code/podaboutlist/json_transcripts/"+clean+".json" 
    if os.path.isfile(jsonFile):
        print("Skipped episode \"%s\": There already was a transcript." % i.title) 
        continue

    print("Processing epsiode \"%s\"..." % i.title)

    dt=time.time()
    episodeTime = time.time()

    linkToFile = i.links[1].href
    response = requests.get(linkToFile)
    response.raise_for_status()
    with open(audio_file, 'wb') as file:
        file.write(response.content)

    print("Downloaded File (took %ss)" % str(time.time()-dt))
    dt=time.time()

    audio = whisperx.load_audio(audio_file)

    print("Loaded audio (took %ss)" % str(time.time()-dt))
    dt=time.time()

    result = model.transcribe(audio, batch_size=batch_size)

    print("Transcribed audio (took %ss)" % str(time.time()-dt))
    dt=time.time()

    with open(jsonFile, 'w') as f:
        f.write(json.dumps(result["segments"]))

    print("Processed episode \"%s\" in %ss)"%(i.title, str(time.time()-episodeTime)))
