from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json
import isodate
import re
import os

videoIDs = []

YOUR_API_KEY=""

r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=UUegMcrgh5QRKO995JzstmTQ&key="+YOUR_API_KEY)
json_data = r.json()
#print(json_data)
nextPageToken = json_data["nextPageToken"]
for i in json_data["items"]:
    videoIDs.append(i["contentDetails"]["videoId"])

while True:
    r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&playlistId=UUegMcrgh5QRKO995JzstmTQ&key="+YOUR_API_KEY+"&pageToken="+nextPageToken)
    json_data = r.json()

    for i in json_data["items"]:
        videoIDs.append(i["contentDetails"]["videoId"])

    if json_data.get("nextPageToken")==None:
        break

    nextPageToken = json_data["nextPageToken"]
    print(nextPageToken)



for i in videoIDs:
    r = requests.get("https://www.googleapis.com/youtube/v3/videos?id="+i+"&key="+YOUR_API_KEY+"&part=contentDetails,snippet")
    json_data = r.json()
    title=json_data["items"][0]["snippet"]["title"]
    title=re.sub(r"[^(A-z)]", "", title)

    if os.path.isfile("F:/Code/podaboutlist/json_transcripts_yt/"+title+".json"):
        continue
    
    duration = json_data["items"][0]["contentDetails"]["duration"]
    duration = isodate.parse_duration(duration)
    if duration.total_seconds() < 60*15:
        continue

    transcript = None
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id=i)
    except:
        print("Error: "+ title)
        continue

    with open("F:/Code/podaboutlist/json_transcripts_yt/"+title+".json", 'w') as f:
        f.write(json.dumps(transcript))