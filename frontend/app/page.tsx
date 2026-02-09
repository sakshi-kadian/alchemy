
import Link from 'next/link';
import { ArrowRight, Dna, Database, ShieldCheck, Sparkles, Activity, Globe, Zap, FlaskConical } from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0a] text-neutral-200 font-sans selection:bg-white/20 overflow-x-hidden relative">

      {/* Dynamic Background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        {/* Dark subtle gradient fallback */}
        <div className="absolute inset-0 bg-neutral-950" />
      </div>

      <main className="relative z-10 pt-20 pb-24 px-6 max-w-7xl mx-auto flex flex-col items-center text-center">

        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-neutral-800 bg-neutral-900/50 text-neutral-400 text-xs font-semibold tracking-wide uppercase mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]"></span>
          <span>Clinical Grade Generative AI</span>
        </div>

        {/* Hero Headline */}
        <h1 className="text-7xl md:text-9xl lg:text-[10rem] font-bold tracking-tighter text-white mb-8 drop-shadow-2xl animate-in fade-in slide-in-from-bottom-6 duration-1000">
          ALCHEMY
        </h1>

        <p className="text-base md:text-lg text-neutral-400 max-w-2xl mx-auto leading-relaxed mb-10 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-100">
          A knowledge-guided framework merging Graph Diffusion Models with Clinical Knowledge Graphs to discover safety-aligned oncology therapeutics.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center gap-4 animate-in fade-in slide-in-from-bottom-10 duration-1000 delay-200">
          <Link href="/dashboard">
            <button className="group relative px-8 py-4 bg-white text-black font-bold text-xl rounded-full shadow-[0_0_20px_rgba(255,255,255,0.1)] hover:shadow-[0_0_30px_rgba(255,255,255,0.2)] hover:-translate-y-1 transition-all duration-300 overflow-hidden cursor-pointer">
              <span className="relative z-10 flex items-center gap-2">
                Start Discovery
                <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
              </span>
            </button>
          </Link>


        </div>

        {/* Stats / Clients */}
        <div className="mt-20 pt-10 border-t border-white/5 grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-16">
          {[
            { label: 'Oncology Graphs', value: '1,400+' },
            { label: 'Validation Strategy', value: 'Knowledge-Guided' },
            { label: 'Inference Latency', value: '<200ms' },
            { label: 'Clinical Validity', value: 'Guaranteed' },
          ].map((stat, i) => (
            <div key={i} className="flex flex-col items-center group cursor-default">
              <span className="text-2xl font-bold text-white group-hover:text-neutral-300 transition-colors">{stat.value}</span>
              <span className="text-xs text-neutral-600 uppercase tracking-widest group-hover:text-neutral-500 transition-colors">{stat.label}</span>
            </div>
          ))}
        </div>

      </main>

      {/* Feature Cards Grid */}
      <section className="relative z-10 py-24 bg-neutral-900/20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="mb-16 md:text-center max-w-3xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">Knowledge-Guided Discovery</h2>
            <p className="text-base text-neutral-400">Our tri-pillar system combines generative creativity with rigorous safety checks.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">

            {/* Card 1 */}
            <div className="bg-gradient-to-b from-neutral-900 to-black backdrop-blur-sm border border-neutral-800 p-8 rounded-3xl group hover:border-neutral-600 transition-colors duration-500">
              <div className="w-12 h-12 rounded-2xl bg-neutral-800 border border-neutral-700 flex items-center justify-center mb-6 group-hover:bg-white group-hover:text-black transition-all duration-500">
                <Dna className="w-6 h-6 text-neutral-300 group-hover:text-black transition-colors" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Generative Diffusion</h3>
              <p className="text-neutral-500 text-sm leading-relaxed group-hover:text-neutral-400 transition-colors">
                Uses Denoising Diffusion Probabilistic Models (DDPM) to construct novel molecular graphs from noise distributions, optimizing for high drug-likeness.
              </p>
            </div>

            {/* Card 2 */}
            <div className="bg-gradient-to-b from-neutral-900 to-black backdrop-blur-sm border border-neutral-800 p-8 rounded-3xl group hover:border-neutral-600 transition-colors duration-500 delay-75">
              <div className="w-12 h-12 rounded-2xl bg-neutral-800 border border-neutral-700 flex items-center justify-center mb-6 group-hover:bg-white group-hover:text-black transition-all duration-500">
                <Database className="w-6 h-6 text-neutral-300 group-hover:text-black transition-colors" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Knowledge Graph</h3>
              <p className="text-neutral-500 text-sm leading-relaxed group-hover:text-neutral-400 transition-colors">
                Built on 1,400+ Elite Oncology drugs, encoding intricate relationships between chemical structures, biological targets, and adverse events.
              </p>
            </div>

            {/* Card 3 */}
            <div className="bg-gradient-to-b from-neutral-900 to-black backdrop-blur-sm border border-neutral-800 p-8 rounded-3xl group hover:border-neutral-600 transition-colors duration-500 delay-150">
              <div className="w-12 h-12 rounded-2xl bg-neutral-800 border border-neutral-700 flex items-center justify-center mb-6 group-hover:bg-white group-hover:text-black transition-all duration-500">
                <ShieldCheck className="w-6 h-6 text-neutral-300 group-hover:text-black transition-colors" />
              </div>
              <h3 className="text-xl font-bold text-white mb-3">Safety Guardrails</h3>
              <p className="text-neutral-500 text-sm leading-relaxed group-hover:text-neutral-400 transition-colors">
                BioBERT-powered semantic enforcement ensures every generated candidate adheres to rigorous safety profiles before visualization, eliminating hallucination risks.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 py-12 border-t border-white/5 bg-[#0a0a0a] text-center">
        <div className="flex items-center justify-center gap-2 mb-4 opacity-30 invert-0">
          <Globe className="w-4 h-4" />
          <span className="text-sm font-bold tracking-widest">GLOBAL RESEARCH INITIATIVE</span>
        </div>
        <p className="text-neutral-600 text-sm">
          &copy; 2026 Alchemy Research Group. All Rights Reserved.
        </p>
      </footer>
    </div>
  );
}
