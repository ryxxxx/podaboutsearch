import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function parse_time(value : number) {
  
  return String(Math.floor(value/60)<10? "0" + Math.floor(value/60) : Math.floor(value/60)) + ":" + String(Math.round(value%60)<10? "0" + Math.round(value%60) : Math.round(value%60));
}