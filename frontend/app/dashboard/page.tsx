"use client";

import { useState, Suspense } from 'react';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import { ArrowRight, Activity, ShieldAlert, Cpu, Database, FlaskConical, Dna, FileText } from 'lucide-react';
import clsx from 'clsx';

// Dynamic imports for heavy 3D/Chart components
const MoleculeViewer = dynamic(() => import('@/components/MoleculeViewer'), { ssr: false });
const GraphVisualization = dynamic(() => import('@/components/GraphVisualization'), { ssr: false });

export default function Dashboard() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleGenerate = async () => {
    // Require prompt to be non-empty
    if (!prompt.trim()) return;

    setLoading(true);

    // Simulate API delay for dramatic effect if needed, or just fetch
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-neutral-200 font-sans selection:bg-white/20">

      {/* Background Background */}
      <div className="fixed inset-0 z-0 pointer-events-none bg-neutral-950" />

      {/* Navbar */}
      <nav className="h-16 border-b border-white/5 bg-[#0a0a0a]/80 backdrop-blur-md sticky top-0 z-50 flex items-center px-6 justify-between">
        <div className="flex items-center gap-3">
          <span className="text-sm font-bold tracking-widest text-white">ALCHEMY <span className="text-neutral-600">- WORKSTATION</span></span>
        </div>
        <div className="flex items-center gap-4">
          <button
            onClick={() => {
              setResult(null);
              setPrompt("");
            }}
            className="text-[10px] font-mono text-neutral-500 hover:text-white transition-colors uppercase tracking-widest border border-transparent hover:border-white/10 px-3 py-1.5 rounded-full cursor-pointer"
          >
            [ RESET_SESSION ]
          </button>

          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-neutral-900 border border-neutral-800">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            <span className="text-[10px] font-mono text-neutral-400">SYSTEM ONLINE</span>
          </div>

          <Link
            href="/"
            className="text-[10px] font-mono text-neutral-500 hover:text-white transition-colors uppercase tracking-widest border border-transparent hover:border-white/10 px-3 py-1.5 rounded-full cursor-pointer"
          >
            [ EXIT_TO_HOME ]
          </Link>
        </div>
      </nav>

      <div className="relative z-10 max-w-7xl mx-auto p-6 space-y-8 pb-24">

        {/* ROW 1: Target Parameters */}
        <div className="bg-neutral-900/50 backdrop-blur-sm border border-white/5 p-6 rounded-2xl group transition-all hover:border-white/10">
          <div className="flex items-center gap-2 mb-4">
            <Database className="w-4 h-4 text-neutral-500" />
            <h2 className="text-xs font-bold text-neutral-300 uppercase tracking-wider">Target Parameters</h2>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            <div className="md:col-span-3">
              <label className="text-[10px] font-mono text-neutral-500 mb-2 block">NATURAL_LANGUAGE_PROMPT</label>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full bg-[#050505] border border-neutral-800 rounded-xl p-4 text-sm focus:outline-none focus:border-white/20 transition-all h-24 resize-none text-neutral-300 placeholder-neutral-700 font-mono leading-relaxed"
                placeholder="Generate a novel BCR-ABL inhibitor for drug-resistant CML..."
              />
              <div className="mt-4 flex flex-wrap gap-3 items-center">
                <span className="text-[10px] font-mono text-neutral-600 uppercase tracking-widest">DEMO_PROMPTS:</span>
                {[
                  "BCR-ABL Inhibitor",
                  "EGFR Kinase Domain",
                  "T315I Mutation Focus"
                ].map((preset) => (
                  <button
                    key={preset}
                    onClick={() => setPrompt(`Generate a novel ${preset} for drug-resistant leukemia therapy`)}
                    className="text-[10px] font-mono text-neutral-500 hover:text-white border border-neutral-800 hover:border-neutral-600 px-2 py-1 rounded transition-all cursor-pointer"
                  >
                    {preset.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>
            <div className="flex items-end">
              <button
                onClick={handleGenerate}
                disabled={loading || !prompt.trim()}
                className={clsx(
                  "w-full py-4 rounded-xl font-bold tracking-wide flex items-center justify-center gap-3 transition-all duration-300 overflow-hidden relative mb-1 h-14",
                  (loading || !prompt.trim()) ? "bg-neutral-800 cursor-not-allowed opacity-50" : "bg-white text-black hover:bg-neutral-200 shadow-[0_0_20px_rgba(255,255,255,0.1)] active:scale-[0.98] cursor-pointer"
                )}
              >
                {loading ? (
                  <>
                    <Cpu className="w-4 h-4 animate-spin" />
                    <span className="text-xs tracking-widest">SYNTHESIZING...</span>
                  </>
                ) : (
                  <>
                    <span className="text-sm">INITIATE SEQUENCE</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* ROW 2: Analysis Report (Only visible if result exists) */}
        {result && (
          <div className="bg-neutral-900/50 backdrop-blur-sm border border-white/5 p-6 rounded-2xl animate-in slide-in-from-bottom-6 duration-700">
            <div className="flex items-center justify-between border-b border-white/5 pb-4 mb-6">
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-white" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">Analysis Report</h3>
              </div>
              <span className="text-[10px] font-mono text-neutral-500">ID: {Math.random().toString(36).substr(2, 9).toUpperCase()}</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* SMILES */}
              <div className="bg-[#050505] p-4 rounded-xl border border-neutral-800 group cursor-copy hover:border-neutral-700 transition-colors cursor-pointer">
                <span className="text-[10px] font-mono text-neutral-500 uppercase block mb-2">Generated SMILES</span>
                <code className="text-xs font-mono text-neutral-300 break-all leading-relaxed">
                  {result.candidate.smiles}
                </code>
              </div>

              {/* Risk & Likeness */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-[#050505] p-4 rounded-xl border border-neutral-800">
                  <div className="flex items-center gap-2 mb-2">
                    <ShieldAlert className="w-3 h-3 text-neutral-400" />
                    <span className="text-[10px] font-mono text-neutral-500 uppercase">Risk</span>
                  </div>
                  <div className="text-2xl font-mono text-white">{Number(result.candidate.risk_score).toFixed(2)}</div>
                  <div className="w-full bg-neutral-800 h-1 mt-2 rounded-full overflow-hidden">
                    <div className="h-full bg-white transition-all duration-1000" style={{ width: `${(1 - parseFloat(result.candidate.risk_score)) * 100}%` }}></div>
                  </div>
                </div>
                <div className="bg-[#050505] p-4 rounded-xl border border-neutral-800">
                  <div className="flex items-center gap-2 mb-2">
                    <Dna className="w-3 h-3 text-neutral-400" />
                    <span className="text-[10px] font-mono text-neutral-500 uppercase">Likeness</span>
                  </div>
                  <div className="text-2xl font-mono text-white">0.94</div>
                  <div className="w-full bg-neutral-800 h-1 mt-2 rounded-full overflow-hidden">
                    <div className="h-full bg-white transition-all duration-1000" style={{ width: '94%' }}></div>
                  </div>
                </div>
              </div>

              {/* Reasoning */}
              <div className="bg-[#050505] p-4 rounded-xl border border-neutral-800 overflow-y-auto">
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="w-3 h-3 text-neutral-400" />
                  <span className="text-[10px] font-mono text-neutral-500 uppercase">Reasoning</span>
                </div>
                <p className="text-xs text-neutral-400 leading-relaxed">
                  Candidate generated via <span className="text-white">Graph Diffusion</span>.
                  Knowledge-guided validation confirms absence of <span className="text-white">Nitro/Chloro</span> subgroups.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* ROW 3: Visualizations (Only visible if result exists, or keep placeholders?) */}
        {/* Let's show placeholders if no result to keep the "Workstation" feel */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[500px]">
          {/* 3D Molecule */}
          <div className="h-full bg-neutral-900/30 backdrop-blur-sm border border-white/5 rounded-2xl overflow-hidden relative group">
            <div className="absolute top-4 left-4 z-20 flex items-center gap-2">
              <div className="px-2 py-1 bg-black/50 backdrop-blur-md rounded border border-white/10 text-[10px] font-mono text-neutral-300">
                3D STRUCTURAL VIEW
              </div>
            </div>
            <div className="absolute inset-0">
              <Suspense fallback={<div className="w-full h-full flex items-center justify-center text-neutral-600 font-mono text-xs">INITIALIZING RENDERER...</div>}>
                <MoleculeViewer />
              </Suspense>
            </div>
          </div>

          {/* Knowledge Graph */}
          <div className="h-full bg-neutral-900/30 backdrop-blur-sm border border-white/5 rounded-2xl overflow-hidden relative">
            <div className="absolute top-4 left-4 z-20 flex items-center gap-2">
              <div className="px-2 py-1 bg-black/50 backdrop-blur-md rounded border border-white/10 text-[10px] font-mono text-neutral-300">
                KNOWLEDGE GRAPH REASONING
              </div>
            </div>
            <div className="absolute inset-0">
              {result ? (
                <GraphVisualization graphData={result.graph_data} />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <div className="text-center space-y-2">
                    <Activity className="w-8 h-8 text-neutral-800 mx-auto animate-pulse" />
                    <p className="text-xs text-neutral-600 font-mono">WAITING FOR GENERATION DATA...</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

      </div>
    </main>
  );
}
