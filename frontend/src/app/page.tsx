"use client"

import { useState, useEffect } from "react"

interface ServiceStatus {
  database: "online" | "offline" | "checking"
  redis: "online" | "offline" | "checking"
  server: "online" | "offline" | "checking"
}

interface MockProblem {
  id: string
  title: string
  description: string
  type: "community" | "curated"
  status: "published" | "pending_review"
  votes: number
  hasVoted: boolean
  evidenceCount: number
  locationName: string
  distance?: string
  tags: string[]
}

export default function Home() {
  // Backend health status state
  const [health, setHealth] = useState<ServiceStatus>({
    database: "checking",
    redis: "checking",
    server: "checking",
  })

  // Mock problems list demonstrating unified entity model
  const [problems, setProblems] = useState<MockProblem[]>([
    {
      id: "prob-1",
      title: "NEET Entrance Exam System Failure",
      description:
        "Reported irregularities and paper leaks in the national medical college entrance exam, affecting over 2 million students nationwide.",
      type: "curated",
      status: "published",
      votes: 14205,
      hasVoted: false,
      evidenceCount: 184,
      locationName: "National / Multi-State",
      tags: ["Education", "Paper Leak", "Governance"],
    },
    {
      id: "prob-2",
      title: "Sector 4 Burnt Distribution Transformer",
      description:
        "Main transformer burnt out yesterday at 14:20 PM. Sparks observed before total power failure. Entire sector currently without electricity.",
      type: "community",
      status: "published",
      votes: 342,
      hasVoted: false,
      evidenceCount: 3,
      locationName: "Plot 42, Sector 4, Indiranagar",
      distance: "0.8 km away",
      tags: ["Power Outage", "Infrastructure"],
    },
    {
      id: "prob-3",
      title: "Major Pothole Bottleneck on NH-48",
      description:
        "Deep potholes spanning across three lanes right after the airport exit bridge. Heavy traffic jams and minor accidents observed.",
      type: "community",
      status: "published",
      votes: 728,
      hasVoted: false,
      evidenceCount: 12,
      locationName: "NH-48 Expressway, Exit 4",
      distance: "3.4 km away",
      tags: ["Road Safety", "Pothole", "Heavy Rain"],
    },
    {
      id: "prob-4",
      title: "Government Hospital Medicine Shortage",
      description:
        "Outpatient pharmacy is out of primary diabetes (Metformin) and hypertension (Amlodipine) medications for the past three weeks.",
      type: "curated",
      status: "pending_review",
      votes: 894,
      hasVoted: false,
      evidenceCount: 22,
      locationName: "State General Hospital Network",
      tags: ["Healthcare", "Shortage", "Public Welfare"],
    },
  ])

  // Fetch backend health endpoint on load and every 10 seconds
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch("http://localhost:8000/health")
        if (res.ok) {
          const data = await res.json()
          setHealth({
            server: "online",
            database: data.services.database === "online" ? "online" : "offline",
            redis: data.services.redis === "online" ? "online" : "offline",
          })
        } else {
          setHealth({ server: "offline", database: "offline", redis: "offline" })
        }
      } catch (error) {
        setHealth({ server: "offline", database: "offline", redis: "offline" })
      }
    }

    checkHealth()
    const interval = setInterval(checkHealth, 10000)
    return () => clearInterval(interval)
  }, [])

  // Vote toggle with micro-animation logic
  const handleVote = (id: string) => {
    setProblems((prev) =>
      prev.map((prob) => {
        if (prob.id === id) {
          const voted = !prob.hasVoted
          return {
            ...prob,
            hasVoted: voted,
            votes: voted ? prob.votes + 1 : prob.votes - 1,
          }
        }
        return prob
      }),
    )
  }

  return (
    <div className="min-h-screen radial-grid-bg relative pb-20">
      {/* Decorative Blur Orbs */}
      <div className="absolute top-[-20%] left-[25%] w-[500px] h-[500px] rounded-full bg-indigo-500/10 animate-glow pointer-events-none" />
      <div className="absolute bottom-[10%] right-[10%] w-[400px] h-[400px] rounded-full bg-teal-500/5 animate-glow pointer-events-none" />

      {/* Main Navigation Header */}
      <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-teal-400 flex items-center justify-between p-2 shadow-lg shadow-indigo-500/10 animate-float">
              <span className="text-slate-950 font-black text-xl tracking-tighter m-auto font-heading">P</span>
            </div>
            <div>
              <h1 className="text-lg font-bold font-heading bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
                Public Priority
              </h1>
              <p className="text-[10px] text-teal-400 font-mono tracking-widest uppercase">Platform</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <span className="hidden md:inline-flex text-xs text-slate-400 font-mono bg-slate-900 border border-slate-800 px-3 py-1 rounded-full items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-teal-500 animate-pulse" />
              Phase 1 Sandbox Active
            </span>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="text-xs font-medium text-slate-300 hover:text-white bg-slate-900/60 hover:bg-slate-800 border border-slate-800/80 hover:border-slate-700 px-4 py-2 rounded-xl transition duration-200 shadow-sm"
            >
              API Docs
            </a>
          </div>
        </div>
      </header>

      {/* Main Hero & Content Grid */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 sm:mt-16">
        
        {/* Hero Section */}
        <section className="text-center max-w-3xl mx-auto mb-16 animate-fade-in">
          <span className="text-xs font-semibold tracking-widest text-indigo-400 uppercase bg-indigo-500/10 border border-indigo-500/20 px-3 py-1.5 rounded-full">
            Core Philosophy: Facts Only
          </span>
          <h2 className="text-4xl sm:text-5xl font-black font-heading mt-6 tracking-tight leading-tight bg-gradient-to-b from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
            What public problems do citizens want solved first?
          </h2>
          <p className="text-base sm:text-lg text-slate-400 mt-6 font-sans leading-relaxed">
            A neutral index to discover and rank community infrastructure faults and curated national policy failures. 
            We report observable facts, coordinates, and verifiable evidence—without political finger-pointing.
          </p>
          <div className="mt-8 flex flex-wrap gap-4 justify-center">
            <button className="bg-gradient-to-r from-indigo-500 to-indigo-600 hover:from-indigo-600 hover:to-indigo-700 text-white font-medium px-6 py-3 rounded-xl transition duration-200 shadow-md shadow-indigo-500/20 transform hover:-translate-y-0.5 active:translate-y-0 text-sm">
              Submit Problem
            </button>
            <button className="glass-panel text-slate-300 hover:text-white hover:bg-slate-900/40 px-6 py-3 rounded-xl transition duration-200 text-sm">
              Suggest Curated Issue
            </button>
          </div>
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main List Showcase - Occupies 2 columns */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-bold font-heading flex items-center gap-2">
                Unified Problem List
                <span className="text-xs font-mono font-normal text-slate-500 bg-slate-900 border border-slate-800/80 px-2.5 py-0.5 rounded-full">
                  Mock Data
                </span>
              </h3>
              <div className="flex gap-2">
                <span className="text-xs font-medium px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-slate-400">
                  Top Voted
                </span>
              </div>
            </div>

            {/* Problems Grid/Stack */}
            <div className="space-y-4">
              {problems.map((prob) => (
                <div
                  key={prob.id}
                  className="glass-panel rounded-2xl p-6 hover:border-slate-700 transition-all duration-300 flex flex-col md:flex-row gap-6 relative group overflow-hidden"
                >
                  {/* Interactive subtle hover border glow */}
                  <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/5 to-teal-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

                  {/* Vote Column */}
                  <div className="flex md:flex-col items-center justify-center gap-2 self-start bg-slate-900/50 border border-slate-800/50 px-4 py-2.5 md:py-3.5 rounded-xl min-w-[70px] w-full md:w-auto">
                    <button
                      onClick={() => handleVote(prob.id)}
                      className={`p-1.5 rounded-lg transition-all duration-200 transform active:scale-95 ${
                        prob.hasVoted
                          ? "bg-teal-500 text-slate-950 scale-105"
                          : "text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                      }`}
                      aria-label="Vote up"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={3}
                        stroke="currentColor"
                        className="w-4 h-4"
                      >
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" />
                      </svg>
                    </button>
                    <span className="font-mono text-sm font-bold tracking-tight text-white">
                      {prob.votes.toLocaleString()}
                    </span>
                    <span className="text-[10px] text-slate-500 font-mono hidden md:block">Votes</span>
                  </div>

                  {/* Details Column */}
                  <div className="flex-1 space-y-3">
                    <div className="flex flex-wrap items-center gap-2">
                      {/* Unified problem_type Badges */}
                      {prob.type === "curated" ? (
                        <span className="text-[10px] font-bold uppercase tracking-wider bg-violet-500/10 border border-violet-500/20 text-violet-400 px-2.5 py-0.5 rounded-full">
                          Curated Public Issue
                        </span>
                      ) : (
                        <span className="text-[10px] font-bold uppercase tracking-wider bg-teal-500/10 border border-teal-500/20 text-teal-400 px-2.5 py-0.5 rounded-full">
                          Community Problem
                        </span>
                      )}

                      {/* Status Badges */}
                      {prob.status === "pending_review" && (
                        <span className="text-[10px] font-bold uppercase tracking-wider bg-amber-500/10 border border-amber-500/20 text-amber-400 px-2.5 py-0.5 rounded-full">
                          Under Review
                        </span>
                      )}

                      <span className="text-xs font-mono text-slate-400 flex items-center gap-1.5 ml-auto">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                          className="w-3.5 h-3.5 text-slate-500"
                        >
                          <path
                            fillRule="evenodd"
                            d="M9.69 18.933a1 1 0 0 0 1.42 0l7.224-7.224a5.002 5.002 0 1 0-7.074-7.074l-4.5 4.5a.75.75 0 0 1-1.06-1.06l4.5-4.5a6.5 6.5 0 0 1 9.193 9.193l-7.224 7.224Z"
                            clipRule="evenodd"
                          />
                        </svg>
                        {prob.evidenceCount} Evidence Uploads
                      </span>
                    </div>

                    <h4 className="text-lg font-bold font-heading text-slate-100 leading-snug">
                      {prob.title}
                    </h4>
                    <p className="text-sm text-slate-400 font-sans leading-relaxed">
                      {prob.description}
                    </p>

                    <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-900/60">
                      {/* Location and Distance */}
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 20 20"
                          fill="currentColor"
                          className="w-3.5 h-3.5 text-rose-500"
                        >
                          <path
                            fillRule="evenodd"
                            d="m9.69 18.933.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.009a12.406 12.406 0 0 0 1.19-.69 19.65 19.65 0 0 0 3.557-3.21A10.134 10.134 0 0 0 18 10a8 8 0 1 0-16 0c0 2.492.68 4.708 1.83 6.024a19.66 19.66 0 0 0 3.558 3.21 12.406 12.406 0 0 0 1.19.69l.018.01.005.002ZM10 12a2 2 0 1 0 0-4 2 2 0 0 0 0 4Z"
                            clipRule="evenodd"
                          />
                        </svg>
                        {prob.locationName}
                        {prob.distance && (
                          <span className="text-slate-500 font-mono ml-1 font-semibold">({prob.distance})</span>
                        )}
                      </span>

                      {/* Tags */}
                      <div className="flex gap-1.5 flex-wrap">
                        {prob.tags.map((tag) => (
                          <span
                            key={tag}
                            className="text-[10px] font-mono bg-slate-900 text-slate-300 border border-slate-800 px-2 py-0.5 rounded"
                          >
                            #{tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Architecture Status Panel & Philosophy - Occupies 1 column */}
          <div className="space-y-6">
            
            {/* Server Status Monitor Card */}
            <div className="glass-panel-glow rounded-2xl p-6 space-y-4">
              <h3 className="text-base font-bold font-heading text-slate-100 flex items-center justify-between">
                Infrastructure Health
                <span
                  className={`w-2.5 h-2.5 rounded-full ${
                    health.server === "online"
                      ? "bg-teal-400 shadow-[0_0_8px_rgba(20,184,166,0.6)] animate-pulse"
                      : health.server === "checking"
                      ? "bg-amber-400 animate-pulse"
                      : "bg-rose-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]"
                  }`}
                />
              </h3>
              
              <p className="text-xs text-slate-400 font-sans leading-relaxed">
                This panel communicates directly with our local FastAPI backend to query PostgreSQL extensions (PostGIS + pgvector) and Redis connections.
              </p>

              <div className="space-y-3 pt-2">
                {/* FastAPI Server Status */}
                <div className="flex justify-between items-center bg-slate-900/60 border border-slate-800/60 p-3 rounded-xl">
                  <span className="text-xs font-semibold font-heading text-slate-200">FastAPI API</span>
                  <span
                    className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded uppercase ${
                      health.server === "online"
                        ? "bg-teal-500/10 text-teal-400 border border-teal-500/20"
                        : health.server === "checking"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                    }`}
                  >
                    {health.server}
                  </span>
                </div>

                {/* PostgreSQL Status */}
                <div className="flex justify-between items-center bg-slate-900/60 border border-slate-800/60 p-3 rounded-xl">
                  <div className="flex flex-col">
                    <span className="text-xs font-semibold font-heading text-slate-200">PostgreSQL DB</span>
                    <span className="text-[9px] text-slate-500 font-mono">PostGIS + pgvector</span>
                  </div>
                  <span
                    className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded uppercase ${
                      health.database === "online"
                        ? "bg-teal-500/10 text-teal-400 border border-teal-500/20"
                        : health.database === "checking"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                    }`}
                  >
                    {health.database}
                  </span>
                </div>

                {/* Redis Caching Status */}
                <div className="flex justify-between items-center bg-slate-900/60 border border-slate-800/60 p-3 rounded-xl">
                  <div className="flex flex-col">
                    <span className="text-xs font-semibold font-heading text-slate-200">Upstash Redis</span>
                    <span className="text-[9px] text-slate-500 font-mono">Rate Limiting / Cache</span>
                  </div>
                  <span
                    className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded uppercase ${
                      health.redis === "online"
                        ? "bg-teal-500/10 text-teal-400 border border-teal-500/20"
                        : health.redis === "checking"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                    }`}
                  >
                    {health.redis}
                  </span>
                </div>
              </div>

              {health.server !== "online" && (
                <div className="text-[11px] text-amber-300 bg-amber-500/5 border border-amber-500/10 p-3 rounded-xl font-sans leading-relaxed">
                  💡 <strong>To run backend health check locally</strong>, spin up Docker compose first with <code>npm run db:up</code>, then launch backend and frontend servers via <code>npm run dev</code>.
                </div>
              )}
            </div>

            {/* Philosophy Cards */}
            <div className="space-y-4">
              <h3 className="text-base font-bold font-heading text-slate-300">Product Rules</h3>
              
              {/* Rule 1 */}
              <div className="glass-panel rounded-2xl p-4 space-y-2 border-l-2 border-l-indigo-500">
                <h4 className="text-xs font-bold text-slate-200 font-heading">1. Facts, Not Opinions</h4>
                <p className="text-xs text-slate-400 font-sans leading-relaxed">
                  Only describe what occurred, when it happened, and upload supporting photos/videos. Text is validated by AI moderation to keep tone neutral.
                </p>
              </div>

              {/* Rule 2 */}
              <div className="glass-panel rounded-2xl p-4 space-y-2 border-l-2 border-l-teal-500">
                <h4 className="text-xs font-bold text-slate-200 font-heading">2. Blame-Free Environment</h4>
                <p className="text-xs text-slate-400 font-sans leading-relaxed">
                  Mentioning specific politicians, political parties, or attributing human intention and blame is strictly filtered out. Focus is solely on the public problem itself.
                </p>
              </div>

              {/* Rule 3 */}
              <div className="glass-panel rounded-2xl p-4 space-y-2 border-l-2 border-l-violet-500">
                <h4 className="text-xs font-bold text-slate-200 font-heading">3. Duplicate Protection</h4>
                <p className="text-xs text-slate-400 font-sans leading-relaxed">
                  Submissions pass through semantic similarity checks. If similar problems or national curated issues are found, users are prompted to join the existing thread.
                </p>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  )
}
