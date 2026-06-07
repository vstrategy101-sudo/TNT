/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Layers, Rocket, ShieldCheck, Video, ArrowUpRight, Check, Users, Shield, Cpu, Activity, Lightbulb, TrendingUp } from "lucide-react";

export default function Services() {
  const [activeService, setActiveService] = useState<number | null>(null);

  const capabilities = [
    {
      icon: <Cpu className="w-6 h-6 text-brand-accent" />,
      name: "MARTECH SYSTEMS & TRACKING",
      tagline: "Attribution Signal Integrity",
      metric: "100% SIGNAL",
      bulletTitle: "INFRASTRUCTURE AUDITING",
      description: "Data integrity is our baseline. We solve the attribution gap before scaling a single rupee of budget. By designing custom data pipelines, we bypass platform tracking degradations.",
      playbooks: [
        "Server-Side GTM & Meta Conversions API (CAPI)",
        "Multi-Touch Attribution (MTA) Full-Funnel tracking",
        "First-Party CRM raw lead & customer sync integration",
        "Custom SQL Source-of-Truth ROI scaling dashboards"
      ]
    },
    {
      icon: <TrendingUp className="w-6 h-6 text-brand-accent" />,
      name: "MEDIA BUYING PLATFORMS",
      tagline: "Disciplined Scaled Buying",
      metric: "UNIT ECONOMICS",
      bulletTitle: "AUCTION OPTIMIZATION",
      description: "Disciplined execution on global networks driven entirely by unit economics, not vanity platform metrics. We treat media buying as mathematical asset allocation.",
      playbooks: [
        "Unit Economic-Led mathematical Bidding triggers",
        "Strategic budget guardrails preserving net margins",
        "Account structure hardening preventing overlap waste",
        "Bid multiplier optimizations based on dayparts"
      ]
    },
    {
      icon: <Video className="w-6 h-6 text-brand-accent" />,
      name: "CREATIVE INTELLIGENCE",
      tagline: "Algorithmic Hook Engineering",
      metric: "THUMB STOPPING",
      bulletTitle: "PROMPT ACTION INTAKE",
      description: "Where high-retention direct storytelling meets algorithmic feedback loops. We analyze exactly what stops the scroll and double downstream budget allocations to winning visual angles.",
      playbooks: [
        "Rapid variant iteration: 50+ monthly video angles",
        "Detailed hook-rate & hold-rate video forensics",
        "Aggressive UGC strategy & direct creator coordination",
        "High-retention visual science capturing native feeds"
      ]
    },
    {
      icon: <Layers className="w-6 h-6 text-brand-accent" />,
      name: "REVENUE SPRINTS & CRO",
      tagline: "Lifetime Value Multipliers",
      metric: "FUNNEL VELOCITY",
      bulletTitle: "CRO SYSTEM ROADMAPS",
      description: "We look far beyond standard dashboards to maximize the profit potential of every click. By patching landing page friction, we accelerate your overall acquisition loop.",
      playbooks: [
        "CRO & landing page page speed optimization sprints",
        "Post-purchase sequence structures & LTV loops",
        "Competitor product positioning & ad hook intelligence",
        "Comprehensive, lightweight scale funnel architecture design"
      ]
    }
  ];

  const expertPods = [
    {
      num: "01",
      role: "Strategy Lead",
      desc: "Growth Architect. Visionary coordinator and gatekeeper of high-level account strategy.",
      icon: <Rocket className="w-4 h-4 text-brand-accent" />
    },
    {
      num: "02",
      role: "MarTech Lead",
      desc: "Infrastructure Specialist. Dedicated builder of tracking, automations and data storage systems.",
      icon: <Cpu className="w-4 h-4 text-brand-accent" />
    },
    {
      num: "03",
      role: "Tracking Lead",
      desc: "Signal Integrity Executor. Ensuring absolute 100% data attribution resilience and auditing.",
      icon: <ShieldCheck className="w-4 h-4 text-[#0052FF]" />
    },
    {
      num: "04",
      role: "Media Strategist",
      desc: "Disciplined Media Buyer. Master of multi-channel ad arbitrage, bidding caps and pacing constraints.",
      icon: <Activity className="w-4 h-4 text-brand-accent" />
    },
    {
      num: "05",
      role: "Growth Specialist",
      desc: "CRO & Retention Specialist. Optimizing user flow, landing page speed, and conversion velocity.",
      icon: <Lightbulb className="w-4 h-4 text-brand-accent" />
    },
    {
      num: "06",
      role: "Creative Lead",
      desc: "Visual Storyteller. Crafting hooks and marrying hard statistical data with human emotion.",
      icon: <Users className="w-4 h-4 text-brand-accent" />
    }
  ];

  return (
    <section
      id="channels"
      className="py-24 bg-white/85 backdrop-blur-[1px] border-t border-zinc-200 px-6 relative"
    >
      <div className="absolute bottom-10 left-10 w-96 h-96 bg-brand-accent/5 rounded-full blur-[110px] pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        
        {/* SECTION 1: ARCHITECTURES OF SCALE */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between mb-16 select-none">
          <div className="max-w-xl">
            <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">Scale Architectures</span>
            <h2 className="text-4xl md:text-5xl font-black text-zinc-900 mt-2 font-display uppercase tracking-tight">
              THE INFRASTRUCTURE OF SCALE<span className="text-brand-accent">.</span>
            </h2>
            <p className="mt-4 text-sm text-zinc-600 leading-relaxed font-sans">
              Performance marketing is in crisis. Simple 'media buying' is dead. We scale high-growth brands using strict, data-secure algorithmic layers and custom tracking architectures.
            </p>
          </div>
          <div className="mt-4 lg:mt-0 font-mono text-[10px] text-zinc-500 uppercase tracking-widest bg-zinc-50 border border-zinc-250 px-4 py-2 rounded-none font-bold">
            HOVER CARDS TO REVEAL ACTIVE SPRINT PLAYBOOK
          </div>
        </div>

        {/* Capabilities Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {capabilities.map((channel, idx) => (
            <div
              key={idx}
              id={`capability-card-${idx}`}
              onClick={() => setActiveService(activeService === idx ? null : idx)}
              onMouseEnter={() => setActiveService(idx)}
              onMouseLeave={() => setActiveService(null)}
              className="p-8 bg-zinc-50 border border-zinc-200 rounded-none group hover:border-brand-accent hover:bg-white transition-all duration-300 cursor-pointer flex flex-col justify-between shadow-sm hover:shadow-md"
            >
              <div>
                {/* Header card details */}
                <div className="flex items-start justify-between">
                  <div className="p-3 bg-white border border-zinc-200 rounded-none group-hover:border-brand-accent transition-colors flex-shrink-0">
                    {channel.icon}
                  </div>
                  <span className="font-mono text-[9px] uppercase tracking-widest px-3 py-1 bg-white border border-zinc-200 rounded-none text-brand-accent group-hover:text-white group-hover:bg-brand-accent font-black transition-colors">
                    {channel.metric}
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-zinc-900 mt-6 group-hover:text-brand-accent transition-colors font-display uppercase leading-tight tracking-tight">
                  {channel.name}
                </h3>
                
                <p className="text-xs text-zinc-400 font-mono mt-1 uppercase font-semibold tracking-wider">
                  {channel.tagline}
                </p>

                <p className="text-zinc-650 font-sans text-xs mt-4 leading-relaxed font-normal">
                  {channel.description}
                </p>
              </div>

              {/* Collapsed playbooks section with fade-in and smooth transition */}
              <div className="mt-6 border-t border-zinc-150 pt-5">
                <div className="flex items-center justify-between text-zinc-500 group-hover:text-zinc-900 transition-colors">
                  <span className="font-mono text-[10px] uppercase tracking-widest font-bold">
                    {channel.bulletTitle}
                  </span>
                  <ArrowUpRight className="w-4 h-4 text-zinc-400 group-hover:text-brand-accent transition-colors animate-pulse" />
                </div>

                <div className="mt-3 overflow-hidden">
                  <AnimatePresence initial={false}>
                    {activeService === idx && (
                      <motion.ul
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.25 }}
                        className="flex flex-col gap-2 pt-1"
                      >
                        {channel.playbooks.map((item, pIdx) => (
                          <li key={pIdx} className="flex gap-2 items-start text-xs text-zinc-600">
                            <span className="mt-1 flex-shrink-0 w-3 h-3 flex items-center justify-center rounded-none bg-zinc-100 border border-brand-accent/20">
                              <Check className="w-1.5 h-1.5 text-brand-accent" />
                            </span>
                            <span className="font-sans leading-tight font-medium">{item}</span>
                          </li>
                        ))}
                      </motion.ul>
                    )}
                  </AnimatePresence>
                </div>
              </div>

            </div>
          ))}
        </div>

        {/* SECTION 2: THE 6-EXPERT POD STRUCTURE FROM THE PITCH DECK */}
        <div className="mt-32 pt-16 border-t border-zinc-200">
          <div className="max-w-2xl select-none mb-12">
            <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">The Cohort Ecosystem</span>
            <h2 className="text-4xl md:text-5xl font-black text-zinc-900 mt-2 font-display uppercase tracking-tight">
              THE 6-EXPERT POD STRUCTURE<span className="text-brand-accent">.</span>
            </h2>
            <p className="mt-4 text-sm text-zinc-600 leading-relaxed font-sans">
              Our flat structure guarantees Indian brands direct access to absolute seniority. We have completely eliminated slow, traditional account managers. You work directly with custom-built Growth Architects.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {expertPods.map((pod, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.05 }}
                className="p-6 bg-zinc-50 border border-zinc-200 rounded-none hover:border-[#0052FF] hover:bg-white group transition-all duration-300 flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between border-b border-zinc-150 pb-3 mb-4">
                    <span className="font-mono text-xs font-black text-zinc-400 group-hover:text-brand-accent transition-colors">{pod.num}</span>
                    <div className="p-1.5 bg-white border border-zinc-150 rounded-none group-hover:border-[#0052FF] transition-all">
                      {pod.icon}
                    </div>
                  </div>
                  <h4 className="font-display text-lg uppercase text-zinc-800 font-bold tracking-tight">
                    {pod.role}
                  </h4>
                  <p className="font-sans text-xs text-zinc-600 mt-2 leading-relaxed">
                    {pod.desc}
                  </p>
                </div>
                <div className="mt-6 font-mono text-[9px] uppercase tracking-widest text-[#0052FF] opacity-0 group-hover:opacity-100 transition-opacity font-extrabold flex items-center gap-1">
                  <span>● GROWTH ARCHITECT</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}

