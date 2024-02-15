'use client'

import { useSearchParams } from 'next/navigation'

import { useState, useEffect } from 'react'

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

import { Fragment } from 'react'

import { buttonVariants } from "@/components/ui/button"
import Link from 'next/link'


interface transcriptMetadataInterface {
  title:string;
  published_date:Date;
  premium:boolean;
  link:string;
}

function extract_data(json_file: any) {
  let data:Array<transcriptMetadataInterface> = []
  const transcript_list=json_file["transcripts"]
  for (let key in transcript_list) { 
    data.push({
      title: transcript_list[key]["title"], 
      published_date: new Date(transcript_list[key]["date"]), 
      premium: transcript_list[key]["link"].includes("patreon"), 
      link:transcript_list[key]["link"]
    })
  }
  return data
} 

export default function TranscriptResults() {
    
    const searchParams = useSearchParams()
    const search = searchParams.get("query")
    
    const anchorText = String(searchParams.get("anchor"))
    
    const [data, setData] = useState(null)

  
    useEffect(() => {
      setData(null)
      fetch('https://ryxxxx.pythonanywhere.com/transcript_list')
        .then((res) => res.json())
        .then((data) => {
          setData(data)
          setTimeout(()=> {
            document.getElementById("anchor")?.scrollIntoView()
          }, 200)
        })
    }, [searchParams])

    if(data!=null)
    {
      const extraction = extract_data(data)

      return (
        <div className='mt-8 mx-2'>
          <Table className="origin-top scale-50 sm:transform-none">
          <TableCaption>List of all transcripts</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead>Released</TableHead>
                <TableHead>Title</TableHead>
                <TableHead className='text-center'>Free</TableHead>
                <TableHead className='text-center'>Transcript Link</TableHead>
                <TableHead className='text-center'>Episode Link</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
            {
            extraction.map((value, key)=>
            <Fragment key={key}>
              <TableRow>
                <TableCell>{value.published_date.toISOString().substring(0,10)}</TableCell>
                <TableCell>{value.title}</TableCell>
                <TableCell className='text-center'>{value.premium ? "" : "✔" }</TableCell>
                <TableCell className='text-center'><Link href={"/transcript?query="+value.title.replace(/[^A-Za-z0-9]/g, "")} className={"ml-auto " + buttonVariants({ variant: "outline" })}>Transcript</Link></TableCell>
                <TableCell className='text-center'><Link target="_blank" href={value.link} className={"ml-auto " + buttonVariants({ variant: "outline" })}>Episode</Link></TableCell>
              </TableRow>
            </Fragment>
            )}
            </TableBody>
          </Table>
        </div>
      );
    }
    else
    {
      return(
        <div id="loading" className='mt-8'>
          Loading...
        </div>
      )
    }
}
