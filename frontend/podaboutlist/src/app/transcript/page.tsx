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

import Link from 'next/link'


interface transcriptDataInterface {
  text:string;
  start:number;
  end:number;
  anchor:boolean;
}

function extract_data(json_file: any) {
  let data:Array<transcriptDataInterface> = []
  const content=json_file["lines"]
  for (let key in content) { 
    data.push({start: content[key]["start"], end: content[key]["end"], text: content[key]["text"], anchor:false})
  }
  return data
} 

export default function TranscriptResults() {
    
    const searchParams = useSearchParams()
    const search = searchParams.get("query")
    
    const start = Number(searchParams.get("start"))
    const end = Number(searchParams.get("end"))
    
    const [data, setData] = useState(null)

  
    useEffect(() => {
      fetch('https://ryxxxx.pythonanywhere.com/transcript?arg='+search)
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
      const title = data["title"]
      const link = data["link"]
      const date = data["date"]
      const extraction = extract_data(data)
      
      return (
        <div className='mt-8 mx-2'>
          <Table className='min-w-[96vw]'>
          <TableCaption>
            <Link className='text-blue-700 text-2xl' href={link}>{title}</Link>
          </TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead className="text-left">Time</TableHead>
                <TableHead>Text</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
            {
            extraction.map((value, key)=>
            <Fragment key={key}>
              {
              value.start >= start && value.start < end ?
              <TableRow className="bg-purple-300 hover:bg-purple-300/50" id="anchor">
                <TableCell className="align-top text-left">
                  {Math.floor(value.start/60)<10? "0" + Math.floor(value.start/60) : Math.floor(value.start/60)}:
                  {Math.round(value.start%60)<10? "0" + Math.round(value.start%60) : Math.round(value.start%60)}</TableCell>
                <TableCell className='break-all'>{value.text}</TableCell>
              </TableRow>
              :
              <TableRow>
                <TableCell className="align-top text-left">
                  {Math.floor(value.start/60)<10? "0" + Math.floor(value.start/60) : Math.floor(value.start/60)}:
                  {Math.round(value.start%60)<10? "0" + Math.round(value.start%60) : Math.round(value.start%60)}
                  </TableCell>
                <TableCell className='break-all'>{value.text}</TableCell>
              </TableRow>
              }
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
