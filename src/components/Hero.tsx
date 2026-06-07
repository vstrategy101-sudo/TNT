/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { motion } from "motion/react";
import { ArrowRight, Sparkles, TrendingUp, ShieldCheck } from "lucide-react";

interface HeroProps {
  onScrollTo: (selector: string) => void;
}

export default function Hero({ onScrollTo }: HeroProps) {
  const stats = [
    { value: "4.30x", label: "CAPITAL SCALE MULTIPLIER", description: "Average partner portfolio scale rate" },
    { value: "₹300Cr+", label: "ACTIVE DISBURSALS METRIC", description: "Bespoke D2C & FinTech architecture" },
    { value: "-85.0%", label: "CAMPAIGN CAC REDUCTION", description: "Average conversion cost reduction" },
    { value: "100%", label: "ATTRIBUTION SIGNAL INTEGRITY", description: "Server-Side GTM & Meta CAPI setups" },
  ];

  return (
    <section
      id="hero"
      className="relative min-h-screen bg-transparent flex flex-col justify-center overflow-hidden pt-36 pb-20 px-6"
    >
      {/* Fine grid overlay */}
      <div className="absolute inset-0 bg-[radial-gradient(rgba(13,13,17,0.015)_1.5px,transparent_1.5px)] [background-size:24px_24px] pointer-events-none z-0" />

      {/* Subtle border separator at top */}
      <div className="absolute top-0 left-0 w-full h-[1px] bg-zinc-100 z-10" />

      {/* Floating Interactive Background Guide Indicator */}
      <div className="absolute bottom-6 left-6 pointer-events-none font-mono text-[9px] text-[#0052FF] opacity-65 uppercase tracking-widest font-black flex items-center gap-2 select-none">
        <span className="w-1.5 h-1.5 bg-[#0052FF] rounded-full animate-ping" />
        <span>Hover cursor anywhere or click empty space to deploy active growth nodes</span>
      </div>

      <div className="max-w-7xl mx-auto w-full relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        {/* Typographical core */}
        <div className="lg:col-span-7 select-none">
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="inline-flex items-center gap-2 px-3 py-1 bg-zinc-50 border border-zinc-200 text-zinc-800 font-mono text-[9px] tracking-[2px] uppercase mb-6 font-bold"
          >
            <Sparkles className="w-3 h-3 text-brand-accent animate-spin-slow" />
            <span>EST. 2018 / ELITE INDEPENDENT PERFORMANCE COHORT</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="font-display text-[65px] md:text-9xl xl:text-11xl font-extrabold text-zinc-900 tracking-tighter leading-[0.75] uppercase"
          >
            tnt<span className="text-brand-[#0052FF]">.</span>
          </motion.h1>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15 }}
            className="mt-6 font-display text-xl md:text-2xl text-brand-accent tracking-wide uppercase italic"
          >
            We solve the business level problems that choke scale.
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-4 font-sans text-sm md:text-md text-zinc-600 max-w-xl leading-relaxed font-normal"
          >
            We are <strong className="text-zinc-900 font-bold">TNT</strong>. A premier, high-precision performance marketing and business economics agency. We solve structural customer acquisition gaps, optimize true unit economics, and deploy custom creative architectures that convert cash into scale. It's not just Ads. It's Core Architecture.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-8 flex flex-col sm:flex-row items-stretch sm:items-center gap-4"
          >
            <button
              id="hero-primary-cta"
              onClick={() => onScrollTo("#audit")}
              className="group relative flex items-center justify-center gap-3 px-8 py-4.5 bg-brand-accent text-white font-mono text-[11px] font-black uppercase tracking-wider hover:bg-zinc-900 transition-all cursor-pointer"
            >
              <span>Instant AI Growth Audit</span>
              <ArrowRight className="w-4 h-4 text-white group-hover:translate-x-1.5 transition-all" />
            </button>
            
            <button
              id="hero-secondary-cta"
              onClick={() => onScrollTo("#simulator")}
              className="flex items-center justify-center gap-2.5 px-8 py-4.5 bg-white hover:bg-zinc-50 border border-zinc-200 text-zinc-800 font-sans font-bold text-xs uppercase tracking-wider transition-all cursor-pointer"
            >
              <TrendingUp className="w-4 h-4 text-brand-accent" />
              <span>Simulate ROI Metric</span>
            </button>
          </motion.div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="mt-10 flex items-center gap-4 text-zinc-400 text-xs font-mono"
          >
            <div className="flex items-center gap-1.5 font-bold">
              <ShieldCheck className="w-4 h-4 text-brand-accent" />
              <span>NO RETAINER FLUFF</span>
            </div>
            <span>•</span>
            <div className="font-bold">PERFORMANCE-BASED COHORTS</div>
          </motion.div>
        </div>

        {/* Brand visual showcase - "The TNT Deck" */}
        <div className="lg:col-span-5 relative">
          <motion.div
            initial={{ opacity: 0, scale: 0.95, rotateY: 10 }}
            animate={{ opacity: 1, scale: 1, rotateY: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="w-full relative aspect-square max-w-[420px] mx-auto bg-white border border-zinc-200 p-6 rounded-none overflow-hidden flex flex-col shadow-xl"
          >
            {/* Visual Header */}
            <div className="flex items-center justify-between border-b border-zinc-100 pb-4 mb-4">
              <div className="flex items-center gap-1.5 font-mono text-[9px] uppercase tracking-widest text-[#0052FF] font-black">
                <span className="w-2 h-2 rounded-full bg-brand-accent animate-pulse inline-block" />
                <span>TNT ACTIVE DECK</span>
              </div>
              <span className="font-mono text-[9px] uppercase tracking-wider text-zinc-400 font-bold">
                MUMBAI / IN HQs
              </span>
            </div>

            {/* Visual Core Content */}
            <div className="flex-1 flex flex-col justify-between">
              <div>
                <div className="text-zinc-400 font-mono text-[9px] tracking-wider uppercase font-bold">CORE PERFORMANCE INFRASTRUCTURE</div>
                <div className="text-zinc-800 font-display text-2xl uppercase mt-1 leading-tight tracking-tight">
                  High-retention storytelling meets algorithmic feedback loops.
                </div>
              </div>

              {/* Minimal creative graph box */}
              <div className="my-5 bg-zinc-50 border border-zinc-150 p-4 flex flex-col justify-between h-[150px]">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-zinc-400 font-mono text-[9px] uppercase tracking-wider block font-bold">SYSTEM VOLUME DEPLOYED</span>
                    <h4 className="text-brand-accent font-display text-[32px] font-black mt-1 leading-none">+300Cr</h4>
                  </div>
                  <span className="bg-brand-accent/5 text-brand-accent font-mono text-[9px] px-2.5 py-0.5 border border-brand-accent/20 tracking-wider font-bold">
                    SIGNAL INGESTION
                  </span>
                </div>
                
                {/* CSS Vector Bars for an aesthetic visual */}
                <div className="flex items-end gap-1 px-1 h-14">
                  {[25, 40, 55, 30, 68, 85, 95, 75, 105, 120, 110, 140].map((val, i) => (
                    <div key={i} className="flex-1 relative group overflow-hidden bg-zinc-200 transition-all" style={{ height: `${(val / 140) * 100}%` }}>
                      <div className="absolute inset-0 bg-[#0052FF] opacity-35 group-hover:opacity-90 transition-all" />
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-between text-zinc-400 font-mono text-[9px] uppercase tracking-widest font-bold border-t border-zinc-100 pt-3">
                <span>MUMBAI CENTER</span>
                <span className="text-zinc-200">|</span>
                <span>ZURICH HQ</span>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Grid of numbers at the bottom of hero */}
      <div className="max-w-7xl mx-auto w-full mt-24 relative z-10 border-t border-zinc-150 pt-12 select-none">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              id={`hero-metrics-card-${i}`}
              className="p-6 bg-white border border-zinc-200 rounded-none group hover:border-brand-accent transition-all duration-350 shadow-sm"
            >
              <div className="font-display text-4xl md:text-5.5xl text-brand-accent group-hover:text-zinc-800 transition-colors tracking-tight leading-none">
                {stat.value}
              </div>
              <div className="font-sans text-[10px] font-black uppercase tracking-wider text-zinc-800 mt-2">
                {stat.label}
              </div>
              <div className="font-sans text-xs text-zinc-500 mt-1 leading-relaxed">
                {stat.description}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
