import type { Metadata } from "next"
import { Inter, Outfit } from "next/font/google"
import "./globals.css"

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
  display: "swap",
})

const outfit = Outfit({
  variable: "--font-heading",
  subsets: ["latin"],
  display: "swap",
})

export const metadata: Metadata = {
  title: "Public Priority Platform | What problems do citizens want solved first?",
  description: "A neutral, data-driven platform that discovers, validates, and ranks public priority issues. Focusing on observable facts, evidence, and citizen priority, without blame or political bias.",
  metadataBase: new URL("http://localhost:3000"),
  openGraph: {
    title: "Public Priority Platform",
    description: "Neutral, data-driven discoverability and ranking of citizen priorities.",
    type: "website",
  }
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${outfit.variable} h-full antialiased dark`}>
      <body className="min-h-full bg-slate-950 text-slate-100 font-sans antialiased flex flex-col selection:bg-teal-500/30 selection:text-teal-200">
        {children}
      </body>
    </html>
  )
}
