'use client'

import { useContext, useState } from 'react'

import { ReloadIcon } from "@radix-ui/react-icons"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useRouter } from 'next/navigation'

import { useEffect } from 'react'
import { usePathname } from 'next/navigation'

import { LoadingContext } from "@/app/colocation"


export default function SearchBar() {

  const [queryText, setQueryText] = useState("")
  const router = useRouter();

  const pathname = usePathname()
  const loadContext = useContext(LoadingContext);

 
  useEffect(() => {
    if(pathname=="/transcript" || pathname=="/")
    {
      loadContext.setLoading(false)
    }
  }, [pathname])
  
  return (
      <form className="flex w-1/2 min-w-max items-center space-x-2">
        <Input type="text" placeholder="list" onChange={(e)=>setQueryText(e.target.value)}/>
        {loadContext.loading 
        ?
        <Button type="submit" className="w-28" disabled><ReloadIcon className="mr-2 h-4 w-4 animate-spin" /></Button>
        :
        <Button type="submit" className="w-28" 
        onClick={()=>{
            loadContext.setLoading(true);
            router.push("/search?"+ new URLSearchParams({query: queryText}).toString());
        }}>
            Search
        </Button>
        }
      </form>
  )
}