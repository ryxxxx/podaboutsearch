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

interface ResultProps {
    title: string;
    similarity: string;
    content: string;
  }
  
  const Result: React.FC<ResultProps> = ({ title, similarity, content }) => {
    // Your component logic here
  
    return (
        <div>
        <Card className="w-auto mt-6">
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>Score: {similarity}%</CardDescription>
        </CardHeader>
        <CardContent className="line-clamp-4 max-w-[96vw] ">
            [...]{content}[...]
        </CardContent>
        <CardFooter className="flex">
        <Link href={"/transcript?query="+title.replace(/[^A-Za-z0-9]/g, "")+"&anchor="+content.replace(/[^A-Za-z0-9]/g, "")} className={buttonVariants({ variant: "outline" })}>Open Full Transcript</Link>
        </CardFooter>
      </Card>
      </div>
    );
  };
  
  export default Result;