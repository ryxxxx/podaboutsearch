# Podcast about Search

Github repository for [podaboutlist.vercel.app](https://podaboutlist.vercel.app), a semantic search engine for transcripts of the podcast ["Podcast about List"](https://www.swagpoop.com/) by Cameron Fetter, Patrick Doran, and Caleb Pitts.


Even though the scripts and files in this repo are specific to this project, the general workflow could easily be adapted to achieve the same result for any podcast (or similar innovations in the audiovisual space):
1. Generate transcripts (for example using [whisperx](https://github.com/m-bain/whisperX)) or if applicable fetch auto-generated subtitles from youtube
2. Generate [vector embeddings](https://huggingface.co/blog/getting-started-with-embeddings) from the transcripts (you will need to seperate the text into [chunks](https://robkerr.ai/chunking-text-into-vector-databases/) first)
3. Input the embeddings along with some metadata (episode title, timestamp) into a [vector database](https://www.pinecone.io/learn/vector-database/) (for example [pinecone](https://www.pinecone.io))
4. Create a back-end API that can receive search requests, generates embeddings for them, and queries the database with those embeddings
5. Create a front-end that allows the user to send text to the back-end and displays the results

Amazingly, all these steps can be achieved for free (if you own hardware that can handle the first step):
* [VoyageAI](https://www.voyageai.com/) offers an embedding API with 50 million free tokens
* [pinecone](https://www.pinecone.io) offers a free solution with which can host up to 100.000 vectors (the ca. 450 transcripts of 60 minute episodes only amount to 80.000 vectors)
* [pythonanywhere](https://www.pythonanywhere.com) offers free hosting for python web applications
* For the front-end there are a lot of different options, since even a statically served page could manage the job (I used [vercel](https://vercel.com) because I wanted to learn next.js + react)