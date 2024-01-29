'use client'

import { useSearchParams } from 'next/navigation'

import Result from '@/components/result'

import { useState, useEffect, useContext } from 'react'


import { LoadingContext } from "@/app/colocation"


export default function SearchResults() {
    
    const searchParams = useSearchParams()
    const search = searchParams.get("query")
    
    const [data, setData] = useState(null)

    const loadContext = useContext(LoadingContext);

    useEffect(() => {
      fetch('https://ryxxxx.pythonanywhere.com/query?arg='+search)
        .then((res) => res.json())
        .then((data) => {
          setData(data)
          loadContext.setLoading(false)
        })
    }, [searchParams])


    if(data!=null)
    {
    
      const matches = data["matches"]
    
      const output = []

      for(let i=0;i<10;i++)
      {
        output.push(<Result title={matches[i]["metadata"]["title"]} content={matches[i]["metadata"]["text"]} similarity={(parseFloat(matches[i]["score"])*100).toString()}/>)
      }
      return (
      <div id="test">
        {output}
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
