'use client'

import { FormEvent, FormEventHandler, Fragment } from "react";

import { useState } from "react";

const url = 'https://script.google.com/macros/s/AKfycbxEimZPIqQU7OTuAY96ylDRoux86oFgozpXLgxlCdGQf2sT3xodJMmB7B7PoiKL9kx6/exec';

function submit(query : string, title : string, time: string) {

  return function(event :FormEvent)
  {
    event.preventDefault()
    const formData = new FormData();
    formData.append("query", query);
    formData.append("episode", title);
    formData.append("timestamp", time);

  const data = Object.fromEntries(formData);

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'text/plain;charset=utf-8',
      },
      body: JSON.stringify(data),
    })
      .then((res) => res.json())
      .then((data) => {
        alert("Sucessfully submitted!")
        window.location.reload()
      })
      .catch((err) => console.log('err', err));
  }

}

export default function Found() {
    
  const [queryText, setQueryText] = useState("")
  const [titleText, setTitleText] = useState("")
  const [timeStampText, setTimeStampText] = useState("")

  const [loading, setLoading] = useState(false)


  return(
    <div className="mt-8">
      <form onSubmit={submit(queryText,titleText,timeStampText)} className="flex flex-col">
        <label htmlFor="search_query">Search query:</label>
        <input onChange={(e)=>setQueryText(e.target.value)} className="m-2 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background " type="text" name="search_query" id="search_query" placeholder="spongebob is squidwards nut"/>

        <label htmlFor="title">Episode Title</label>
        <input onChange={(e)=>setTitleText(e.target.value)} className="m-2 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background " type="text" name="title" id="title" placeholder="Premium #127: Scrat Got His Nut: A Panel Discussion (w. Pierce)"/>

        <label htmlFor="timestamp">Timestamp</label>
        <input onChange={(e)=>setTimeStampText(e.target.value)} className="m-2 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background " type="text" name="timestamp" id="timestamp" placeholder="10:13-14:59"/>
        {loading ?
        <button disabled className="mt-4" type="submit">Submitting...</button> :
        <button onClick={(e)=>{setTimeout(()=>{setLoading(true)}, 50)}} className="mt-4" type="submit">Submit</button>
        }
      </form>
    </div>
  )

}
