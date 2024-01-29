'use client'

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

export default function Home() {
  
  return (
      <div>
        <Card className="w-[500px] max-w-[100vw] mt-6">
          <CardHeader>
            <CardTitle className="text-center">About</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              A semantic search engine for the podcast &quot;Podcast about List&quot; by Cameron Fetter, Patrick Doran, and Caleb Pitts, so that you can more better find your favorite bits of theirs.<br/>
              <br/>
              Check them out on their <a className="text-blue-600" href="https://www.swagpoop.com">Website</a>, <a className="text-blue-600" href="https://www.youtube.com/@PodcastAboutList">Youtube</a>, and their <a className="text-blue-600" href="https://www.patreon.com/podcastaboutlist/posts">Patreon</a>!

            </div>
          </CardContent>
        </Card>
      </div>
  );
}
