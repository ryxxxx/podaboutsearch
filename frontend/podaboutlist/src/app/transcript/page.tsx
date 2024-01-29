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


interface transcriptDataInterface {
  text:string;
  start:number;
  anchor:boolean;
}

function extract_data(json_file: any) {
  let data:Array<transcriptDataInterface> = []
  const content=json_file["content"]
  for (let key in content) { 
    data.push({start: content[key]["start"], text: content[key]["text"], anchor:false})
  }
  return data
} 

export default function TranscriptResults() {
    
    const searchParams = useSearchParams()
    const search = searchParams.get("query")
    
    const anchorText = String(searchParams.get("anchor"))
    
    const [data, setData] = useState(null)

  
    useEffect(() => {
      fetch('https://ryxxxx.pythonanywhere.com/transcript?arg='+search)
        .then((res) => res.json())
        .then((data) => {
          setData(data)
          setTimeout(()=> {
            document.getElementById("anchor")?.scrollIntoView()
          }, 100)
        })
    }, [searchParams])

    if(data!=null)
    {
      const title = data["title"]
      const extraction = extract_data(data)

      for(let i=0; i<extraction.length; i++)
      {
        let combinedText = extraction[i].text;
        if(i>0)
          combinedText = extraction[i-1].text + combinedText;
        if(i<extraction.length-1)
          combinedText = combinedText + extraction[i+1];
        if(combinedText.replace(/[^A-Za-z0-9]/g, "").includes(anchorText.substring(0,anchorText.length/2)))
        {
          extraction[i].anchor=true;
          break;
        }
      }
      
      return (
        <div className='mt-8 mx-2'>
          <Table>
          <TableCaption>{title}</TableCaption>
            <TableHeader>
              <TableRow>
                <TableHead className="text-right">Time</TableHead>
                <TableHead>Text</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
            {
            extraction.map((value, key)=>
            <Fragment key={key}>
              {
              value.anchor ?
              <TableRow className="bg-purple-300 hover:bg-purple-300/50" id="anchor">
                <TableCell className="align-top text-right">
                  {Math.floor(value.start/60)<10? "0" + Math.floor(value.start/60) : Math.floor(value.start/60)}:
                  {Math.round(value.start%60)<10? "0" + Math.round(value.start%60) : Math.round(value.start%60)}</TableCell>
                <TableCell className='break-all'>{value.text}</TableCell>
              </TableRow>
              :
              <TableRow>
                <TableCell className="align-top text-right">
                  {Math.floor(value.start/60)<10? "0" + Math.floor(value.start/60) : Math.floor(value.start/60)}:
                  {Math.round(value.start%60)<10? "0" + Math.round(value.start%60) : Math.round(value.start%60)}</TableCell>
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
