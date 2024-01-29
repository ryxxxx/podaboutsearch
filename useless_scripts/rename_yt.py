import os
import re

yt_directory = os.fsencode("F:/Code/podaboutlist/json_transcripts_yt")

for f in os.listdir(yt_directory):
    filename = os.fsdecode(f)
    path= os.path.join(os.fsdecode(yt_directory), filename)
    newname=re.sub(r"[()]", "", filename)
    newpath=os.path.join(os.fsdecode(yt_directory), newname)
    os.rename(path,newpath)
