'use client'

import { Inter } from "next/font/google";
import "./globals.css";
import QuickFix from "./colocation";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <head><title>Podaboutlist Search</title></head>
      <body className={inter.className}>
        <QuickFix>
          {children}
        </QuickFix>
      </body>
    </html>
  );
}
