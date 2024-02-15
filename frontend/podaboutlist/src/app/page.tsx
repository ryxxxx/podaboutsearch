'use client'

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import Link from "next/link";

export default function Home() {
  
  return (
      <div>
        <Card className="w-[600px] max-w-[100vw] mt-6">
          <CardHeader>
            <CardTitle className="text-center">About:</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center">
              A semantic search engine for the podcast &quot;Podcast about List&quot; by Cameron Fetter, Patrick Doran, and Caleb Pitts, so that you can more better find your favorite bits of theirs.<br/>
              <br/>
              Check them out on their <a className="text-blue-600" href="https://www.swagpoop.com">Website</a>, <a className="text-blue-600" href="https://www.youtube.com/@PodcastAboutList">Youtube</a>, and their <a className="text-blue-600" href="https://www.patreon.com/podcastaboutlist/posts">Patreon</a>!
            </div>
          </CardContent>
        </Card>
        <Card className="w-[600px] max-w-[100vw] mt-6">
          <CardHeader>
            <CardTitle className="text-center text-sm font-normal">
              The search returns the transcript excerpts that are most similar in meaning to your full query (as estimated by an embedding model), but if you want specific phrases to definitely be included in all results, you can wrap them in quotation marks.
              <br/>
              <br/>
              For evaluating the search, it would be helpful to have a list of example search queries along with the expected result (correct episode and timestamp). So, if you found a bit using the search or have your own examples in mind, you can submit those <Link className="text-blue-600" href="/found_a_bit">here</Link>. 
              <br/>
              <br/>
              If you have any other suggestions, you can send them to me on <Link className="text-blue-600" href="https://www.reddit.com/message/compose/?to=agitpropping">reddit</Link>.
            </CardTitle>
          </CardHeader>
        </Card>
        <Card className="w-[600px] max-w-[100vw] mt-6">
          <CardHeader>
            <CardTitle className="text-center text-blue-600"><Link href="/transcript_list">Transcript List</Link></CardTitle>
            <CardContent className="text-center text-sm"><br/>Now with high quality transcripts by courtesy of @ralphorama!</CardContent>
          </CardHeader>
        </Card>
        <Card className="w-[600px] max-w-[100vw] mt-6">
          <CardHeader>
            <CardTitle className="text-center text-blue-600 text-base font-normal"><Link href="https://github.com/ryxxxx/podaboutsearch">GitHub</Link></CardTitle>
          </CardHeader>
        </Card>
      </div>
  );
}
