/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Check, Calendar, Building2 } from "lucide-react";

interface CaseStudy {
  brandName: string;
  industry: string;
  metricLabel: string;
  metricValue: string;
  headline: string;
  description: string;
  challenge: string;
  playbookSteps: string[];
  metrics: {
    beforeCpa: string;
    afterCpa: string;
    beforeRoas: string;
    afterRoas: string;
    spendScaled: string;
  };
}

export default function CaseStudies() {
  const [activeTab, setActiveTab] = useState(0);

  const cases: CaseStudy[] = [
    {
      brandName: "BLUE TOKAI COFFEE",
      industry: "D2C BEVERAGES & SPECIALTY RETAIL",
      metricLabel: "Attributable Scale Expansion",
      metricValue: "₹18.4 Cr",
      headline: "How we scaled an artisan beverage house during cold-brew season dips.",
      description: "Blue Tokai was struggling with steep Customer Acquisition Costs (CAC) on generic Meta Broad campaigns, experiencing severe conversion dropoffs on complex multi-step mobile cart pages.",
      challenge: "Creative fatigue within 5 days on standard Instagram Reels, leading to immediate CAC inflation and performance chokeholds.",
      playbookSteps: [
        "Filmed 24 high-production micro-hook variants focused on pour-over sensory experience and iced assets",
        "Constructed a lightweight Shopify headless checkout tunnel securing sub-400ms loading bounds",
        "Deployed Meta Conversions API preventing 30%+ client-side browser pixel packet loss",
        "Configured strict horizontal scaling models targeting lookalike cohorts with dynamic budget splits"
      ],
      metrics: {
        beforeCpa: "₹650.00",
        afterCpa: "₹310.00",
        beforeRoas: "1.62x",
        afterRoas: "4.15x",
        spendScaled: "₹12L to ₹75L/mo"
      }
    },
    {
      brandName: "STASHFIN DIGITAL CREDIT",
      industry: "FINTECH & MOBILE CREDIT ACQUISITION",
      metricLabel: "Cost Per Qualified KYC Completed",
      metricValue: "-48.2%",
      headline: "Restructuring programmatic and Google search to lock in premium borrowers.",
      description: "Stashfin was bidding high on competitive credit search fragments (e.g., 'instant loan app'), bleeding capital on non-prime applicant volumes and incomplete applications in tier 2/3 markets.",
      challenge: "Aggressive bidding wars driving Cost-Per-Click past ₹150 on major search queries without down-funnel qualification.",
      playbookSteps: [
        "Configured granular negative exclusions preventing competitor query hijacking and junk clicks",
        "Constructed hyper-fast quiz paths qualifying credit profile vectors prior to high-friction App Store navigation",
        "Migrated standard keywords to precise Google Performance Max for financial verticals",
        "Integrated direct CRM logs via offline feedback loops to calibrate Google bids only on KYC approvals"
      ],
      metrics: {
        beforeCpa: "₹1,450.00",
        afterCpa: "₹751.00",
        beforeRoas: "2.10x",
        afterRoas: "4.30x",
        spendScaled: "₹25L to ₹95L/mo"
      }
    },
    {
      brandName: "SHIPWAY SCALE SAAS",
      industry: "B2B LOGISTICS & SHIPPING INTELLIGENCE",
      metricLabel: "Enterprise Demo Volume Sprints",
      metricValue: "+195%",
      headline: "Scaling premium cargo logistics signups via account-level IP placements.",
      description: "Standard LinkedIn lead-generation strategies had hit severe response saturation, leading to flat outbound demo lines, inflated agency costs, and zero enterprise decision-maker interest.",
      challenge: "High ad fatigue and astronomical B2B CPMs on conventional social feeds.",
      playbookSteps: [
        "Bypassed standard networks to set up Private Marketplace native spots across premium Indian financial journals",
        "Developed custom 'Delivery Delay Impact Calculators' rendering live logistics savings for prospect companies",
        "Applied active reverse-IP lookups serving custom creatives showing target executive problems",
        "Unified multi-channel CRM touchpoints to map perfect cross-channel attribution paths"
      ],
      metrics: {
        beforeCpa: "₹5,800.00",
        afterCpa: "₹2,900.00",
        beforeRoas: "N/A (B2B Lead)",
        afterRoas: "5.4x Pipeline ROI",
        spendScaled: "₹8L to ₹32L/mo"
      }
    }
  ];

  return (
    <section
      id="cases"
      className="py-24 bg-white/85 backdrop-blur-[1px] border-t border-zinc-200 px-6 relative"
    >
      <div className="absolute top-1/2 right-1/4 -translate-y-1/2 w-96 h-96 bg-[#0052FF]/5 rounded-full blur-[110px] pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 select-none">
          <div className="max-w-xl">
            <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">Proven Scale Milestones</span>
            <h2 className="text-4xl md:text-5xl font-black text-zinc-900 mt-1 font-display uppercase tracking-tight">
              QUIETLY SCALE<span className="text-[#0052FF]">.</span>
            </h2>
            <p className="mt-3 text-sm text-zinc-650 font-sans leading-relaxed">
              We let raw net contribution statistics do the talking. Below are actual performance metrics from partners who scaled their budgets confidently with zero retainer fluff.
            </p>
          </div>

          {/* Tab buttons */}
          <div className="mt-6 md:mt-0 flex gap-2 overflow-x-auto pb-2 md:pb-0 scrollbar-none font-mono">
            {cases.map((cs, i) => (
              <button
                key={i}
                id={`case-study-tab-${i}`}
                onClick={() => setActiveTab(i)}
                className={`px-4 py-2 rounded-none text-xs font-bold uppercase tracking-wider transition-all whitespace-nowrap cursor-pointer border ${
                  activeTab === i
                    ? "bg-[#0052FF] text-white border-[#0052FF]"
                    : "bg-zinc-50 text-zinc-500 border-zinc-200 hover:text-zinc-900 hover:bg-zinc-100"
                }`}
              >
                {cs.brandName}
              </button>
            ))}
          </div>
        </div>

        {/* Dynamic Display */}
        <div className="bg-zinc-50 border border-zinc-200 rounded-none p-8 lg:p-12 relative overflow-hidden shadow-sm">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.3 }}
              className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start relative z-10"
            >
              
              {/* Core metrics and brand title */}
              <div className="lg:col-span-4 flex flex-col justify-between h-full select-none">
                <div>
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-white border border-zinc-200 rounded-none font-mono text-[9px] uppercase tracking-widest text-[#0052FF] font-black">
                    <Building2 className="w-3 h-3" />
                    <span>{cases[activeTab].industry}</span>
                  </div>
                  
                  <h3 className="text-3xl font-display uppercase text-zinc-900 mt-4 tracking-tight leading-none font-black">
                    {cases[activeTab].brandName}
                  </h3>
                  
                  <div className="mt-8">
                    <span className="text-zinc-500 font-mono text-[9px] uppercase tracking-widest font-bold">{cases[activeTab].metricLabel}</span>
                    <div className="text-5.5xl md:text-6.5xl font-display text-[#0052FF] mt-2 leading-none font-bold">
                      {cases[activeTab].metricValue}
                    </div>
                  </div>
                </div>

                {/* Micro stat-box comparing CPA / ROAS */}
                <div className="mt-12 bg-white border border-zinc-200 p-6 rounded-none shadow-sm">
                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <div className="text-[9px] font-mono text-zinc-400 uppercase tracking-widest font-bold">Before Scale</div>
                      <div className="mt-2 text-zinc-600 font-sans text-xs">
                        CAC: <span className="font-bold text-zinc-700 font-mono">{cases[activeTab].metrics.beforeCpa}</span>
                      </div>
                      <div className="mt-1 text-zinc-600 font-sans text-xs">
                        Value: <span className="font-bold text-zinc-700 font-mono">{cases[activeTab].metrics.beforeRoas}</span>
                      </div>
                    </div>
                    
                    <div className="border-l border-zinc-200 pl-6">
                      <div className="text-[9px] font-mono text-[#0052FF] uppercase tracking-widest font-black">TNT System Core</div>
                      <div className="mt-2 text-zinc-900 font-sans text-xs font-semibold">
                        CAC: <span className="text-[#0052FF] font-mono font-black">{cases[activeTab].metrics.afterCpa}</span>
                      </div>
                      <div className="mt-1 text-zinc-900 font-sans text-xs font-semibold">
                        Value: <span className="text-[#0052FF] font-mono font-black">{cases[activeTab].metrics.afterRoas}</span>
                      </div>
                    </div>
                  </div>

                  <div className="border-t border-zinc-150 mt-4 pt-4 flex gap-2 items-center text-[10px] font-mono text-zinc-500 uppercase font-bold tracking-wider">
                    <Calendar className="w-3.5 h-3.5 text-[#0052FF]" />
                    <span>Scale Rate: {cases[activeTab].metrics.spendScaled}</span>
                  </div>
                </div>

              </div>

              {/* Study narrative details & playbooks */}
              <div className="lg:col-span-8 flex flex-col gap-8">
                <div>
                  <h4 className="font-display text-xl md:text-2xl uppercase text-zinc-900 tracking-tight leading-snug font-black">
                    "{cases[activeTab].headline}"
                  </h4>
                  <p className="text-sm text-zinc-600 mt-4 leading-relaxed font-sans font-normal">
                    {cases[activeTab].description}
                  </p>
                </div>

                <div className="p-5 bg-white border border-zinc-200 rounded-none shadow-sm">
                  <span className="font-mono text-[9px] text-zinc-500 uppercase tracking-widest leading-none font-bold">Primary Bottleneck Diagnosed</span>
                  <p className="text-xs text-zinc-700 font-sans mt-2 font-medium leading-relaxed">
                    {cases[activeTab].challenge}
                  </p>
                </div>

                <div>
                  <span className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest font-black">Our Execution Playbook</span>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
                    {cases[activeTab].playbookSteps.map((step, sIdx) => (
                      <div key={sIdx} className="flex gap-2.5 items-start p-3.5 bg-white border border-zinc-200 rounded-none hover:border-[#0052FF] transition-all duration-300 shadow-sm">
                        <span className="mt-0.5 w-4 h-4 rounded-none bg-[#0052FF]/5 border border-[#0052FF] flex items-center justify-center flex-shrink-0">
                          <Check className="w-2.5 h-2.5 text-[#0052FF]" />
                        </span>
                        <p className="text-xs text-zinc-800 font-sans leading-tight font-medium">
                          {step}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

              </div>

            </motion.div>
          </AnimatePresence>
        </div>

      </div>
    </section>
  );
}
