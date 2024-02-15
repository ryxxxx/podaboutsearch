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
      setData(null)
      fetch('https://ryxxxx.pythonanywhere.com/v2search?arg='+search)
        .then((res) => res.json())
        .then((data) => {
          setData(data)
          loadContext.setLoading(false)
        })
    }, [searchParams])


    if(data!=null)
    {
    
      const matches : Array<any> = data["matches"]

      return (
      <div>
      {
        matches.map((value,key) => (
          <Result 
          title={value["metadata"]["title"]} 
          content={value["metadata"]["text"]} 
          similarity={(parseFloat(value["score"])*100).toFixed(3)}
          start={value["metadata"]["start"]}
          end={value["metadata"]["end"]}
          search_string={String(search)}
          link={value["metadata"]["link"]}
          key={key}
        />)
        )
      }
      </div>
      )
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
