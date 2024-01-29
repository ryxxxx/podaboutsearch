'use client'
//this file used to be part of the root layout but during deployment vercel told me that layout files cannot export context variables, alas the name quickfix

import Image from "next/image"
import Link from "next/link"
import SearchBar from "@/components/searchbar";
import { createContext } from "react";
import { useState } from "react";

interface ILoadingContext {
  loading: boolean;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
}

export const LoadingContext = createContext<ILoadingContext>({
  loading: false,
  setLoading: () => {}
});


export default function QuickFix({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {

const [loading, setLoading] = useState(false);
const value = { loading, setLoading };

  return (
    <main className="flex flex-col items-center pt-4 pb-8">
    <div className="mb-6 flex flex-col items-center sm:flex-row">
      <Link href="/">
      <Image
      src="/logo.jpg"
      alt="logo"
      width={0}
      height={0}
      sizes="100vw"
      className="w-auto h-16 w-16 rounded-md mr-2"
      />
      </Link>
    <h1 className="text-4xl text-center pt-2 sm:pt-0">Podcast About Search</h1>
    </div>
    <LoadingContext.Provider value={value}>
    <SearchBar/>
    {children}
    </LoadingContext.Provider>
    </main>
  );
}
