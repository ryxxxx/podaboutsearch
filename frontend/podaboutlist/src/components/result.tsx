'use client'

import { buttonVariants } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import Link from "next/link"

import { parse_time } from '@/lib/utils'

interface ResultProps {
  title: string;
  similarity: string;
  content: string;
  start: number;
  end: number;
  search_string: string;
  link: string;
}

const Result: React.FC<ResultProps> = ({ title, similarity, content, start, end, search_string, link }) => {
  const regexMetachars = /[(){[*+?.\\^$|]/g;

  const words = search_string.replaceAll("\"","").split(" ")

  const reg_words = words

  for (var i = 0; i < reg_words.length; i++) {
    words[i]=words[i].toLowerCase()
    reg_words[i] = reg_words[i].replace(regexMetachars, "\\$&")
  }
  const regexpression = new RegExp(`\\b(${reg_words.join("|")})\\b`, "gi")


  return (
      <Card className="w-auto mt-6">
      <CardHeader className="flex-row">
        <CardTitle>{title}</CardTitle>
        <CardDescription className="ml-auto">Score: {similarity}%</CardDescription>
      </CardHeader>
      <CardContent className=" max-w-[96vw] text-justify">
      <div className="text-muted-foreground mb-4">{parse_time(start)} - {parse_time(end)}</div>
        {
          content.split(regexpression).map((part, i) => 
              <span key={i} className={words.includes(part.toLowerCase()) ? "font-semibold" : "" }>
                  { part }
              </span>)
        }
      </CardContent>
      <CardFooter className="flex">
      <Link href={"/transcript?query="+title.replace(/[^A-Za-z0-9]/g, "")+"&start="+start+"&end="+end} className={buttonVariants({ variant: "outline" })}>Open Full Transcript</Link>
      <Link target="_blank" href={link} className={"ml-auto " + buttonVariants({ variant: "outline" })}>Episode Link</Link>
      </CardFooter>
    </Card>
  );
};

export default Result;