/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import * as React from "react";
import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Sparkles, Brain, Loader2, BarChart2, MessageSquare, Target, Compass, Zap, HelpCircle, CheckCircle2 } from "lucide-react";
import { AdAuditStrategy } from "../types";

export default function Auditor() {
  const [businessName, setBusinessName] = useState("");
  const [website, setWebsite] = useState("");
  const [industry, setIndustry] = useState("");
  const [description, setDescription] = useState("");
  const [primaryGoal, setPrimaryGoal] = useState("Lower customer acquisition costs (CAC)");
  const [adSpend, setAdSpend] = useState("500000");

  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [strategy, setStrategy] = useState<AdAuditStrategy | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [promptKeyNeeded, setPromptKeyNeeded] = useState(false);

  const loadingPhrases = [
    "Receiving brand profile coordinates...",
    "Querying Meta & Google India industry bid landscapes...",
    "Engineering scroll-stopping visual hooks with Gemini...",
    "Structuring media allocation weights & personas...",
    "Polishing the final, custom performance roadmap..."
  ];

  const triggerProgressDemo = () => {
    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < loadingPhrases.length - 1) {
        currentStep++;
        setLoadingStep(currentStep);
      } else {
        clearInterval(interval);
      }
    }, 1800);
    return interval;
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!businessName || !industry || !description) return;

    setLoading(true);
    setLoadingStep(0);
    setStrategy(null);
    setErrorMsg(null);
    setPromptKeyNeeded(false);

    const progressInterval = triggerProgressDemo();

    try {
      const response = await fetch("/api/audit", {
         method: "POST",
         headers: { "Content-Type": "application/json" },
         body: JSON.stringify({
           businessName,
           website,
           industry,
           description,
           primaryGoal,
           adSpend
         })
      });

      const data = await response.json();
      clearInterval(progressInterval);

      if (!response.ok) {
        if (data.isMissingKey) {
          setPromptKeyNeeded(true);
          setErrorMsg("Your API key can be found in the Settings > Secrets panel. The server requires this key to build live audits.");
        } else {
          setErrorMsg(data.error || "An unexpected issue occurred while synthesizing the marketing blueprint.");
        }
        setLoading(false);
        return;
      }

      setStrategy(data);
    } catch (err) {
      clearInterval(progressInterval);
      setErrorMsg("Failed to connect to full-stack server endpoints. Please check compile status.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      id="audit"
      className="py-24 bg-white/85 backdrop-blur-[1px] border-t border-zinc-200 px-6 relative"
    >
      <div className="absolute bottom-10 right-10 w-[450px] h-[450px] bg-brand-accent/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        
        {/* Header intro */}
        <div className="max-w-3xl mb-12 select-none">
          <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">On-Demand Campaign architect</span>
          <h2 className="text-4xl md:text-5xl font-black text-zinc-900 mt-1 font-display uppercase tracking-tight">
            INSTANT LAUNCH PORTFOLIO<span className="text-brand-accent">.</span>
          </h2>
          <p className="mt-3 text-sm text-zinc-600 font-sans leading-relaxed">
            Why wait weeks for high-friction agency pitch meetings? Tell us what you build, and our AI Growth Strategist will instantly bundle a structured direct-response roadmap, custom budget weights, and scroll-stopping hooks.
          </p>
        </div>

        {/* Core Layout Split */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-start">
          
          {/* Form input card */}
          <div className="lg:col-span-12 xl:col-span-5 bg-zinc-50 border border-zinc-200 p-8 rounded-none relative shadow-sm">
            <div className="flex items-center gap-2 pb-4 border-b border-zinc-200 mb-6">
              <Brain className="w-4 h-4 text-[#0052FF] animate-pulse" />
              <span className="font-mono text-[10px] text-zinc-600 uppercase tracking-widest font-bold">Brand Credentials</span>
            </div>

            <form onSubmit={handleGenerate} className="flex flex-col gap-5">
              
              {/* Business Name */}
              <div>
                <label className="block text-zinc-600 font-mono text-[10px] uppercase font-bold tracking-wider mb-2" htmlFor="input-biz-name">
                  Business / Brand Name *
                </label>
                <input
                  id="input-biz-name"
                  type="text"
                  required
                  placeholder="e.g., Blue Tokai Coffee, Bombay Shirt Co."
                  value={businessName}
                  onChange={(e) => setBusinessName(e.target.value)}
                  className="w-full bg-white border border-zinc-200 rounded-none px-4 py-3 text-xs text-zinc-800 placeholder-zinc-400 focus:outline-none focus:border-brand-accent focus:bg-white transition-all font-mono"
                />
              </div>

              {/* Website URL */}
              <div>
                <label className="block text-zinc-600 font-mono text-[10px] uppercase font-bold tracking-wider mb-2" htmlFor="input-website">
                  Website / Landing Page (Optional)
                </label>
                <input
                  id="input-website"
                  type="url"
                  placeholder="e.g., https://www.bluetokaicoffee.com"
                  value={website}
                  onChange={(e) => setWebsite(e.target.value)}
                  className="w-full bg-white border border-zinc-200 rounded-none px-4 py-3 text-xs text-zinc-800 placeholder-zinc-400 focus:outline-none focus:border-brand-accent focus:bg-white transition-all font-mono"
                />
              </div>

              {/* Industry Selection */}
              <div>
                <label className="block text-zinc-600 font-mono text-[10px] uppercase font-bold tracking-wider mb-2" htmlFor="input-industry">
                  Industry Vertical *
                </label>
                <input
                  id="input-industry"
                  type="text"
                  required
                  placeholder="e.g., D2C Apparel, Organic Wellness, SaaS"
                  value={industry}
                  onChange={(e) => setIndustry(e.target.value)}
                  className="w-full bg-white border border-zinc-200 rounded-none px-4 py-3 text-xs text-zinc-800 placeholder-zinc-400 focus:outline-none focus:border-brand-accent focus:bg-white transition-colors font-mono"
                />
              </div>

              {/* Business Description */}
              <div>
                <label className="block text-zinc-600 font-mono text-[10px] uppercase font-bold tracking-wider mb-2" htmlFor="input-description">
                  Business & Audience Profile *
                </label>
                <textarea
                  id="input-description"
                  required
                  rows={3}
                  placeholder="What products do you sell? Who are your target customer segments in India?"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full bg-white border border-zinc-200 rounded-none px-4 py-3 text-xs text-zinc-800 placeholder-zinc-400 focus:outline-none focus:border-brand-accent focus:bg-white transition-colors resize-none leading-relaxed font-sans"
                />
              </div>

              {/* Budget Allocation selection */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-zinc-600 font-mono text-[9px] uppercase font-bold tracking-wider mb-2" htmlFor="input-goal">
                    Primary Scale Goal
                  </label>
                  <select
                    id="input-goal"
                    value={primaryGoal}
                    onChange={(e) => setPrimaryGoal(e.target.value)}
                    className="w-full bg-white border border-zinc-200 rounded-none px-3 py-3 text-[11px] text-zinc-700 focus:outline-none focus:border-brand-accent transition-colors cursor-pointer"
                  >
                    <option>Lower acquisition costs (CAC)</option>
                    <option>Scale Meta spend safely</option>
                    <option>Acquire high-ticket clients</option>
                    <option>Maximize overall scale multiplier</option>
                  </select>
                </div>

                <div>
                  <label className="block text-zinc-600 font-mono text-[9px] uppercase font-bold tracking-wider mb-2" htmlFor="input-budget">
                    Monthly Media Spend
                  </label>
                  <select
                    id="input-budget"
                    value={adSpend}
                    onChange={(e) => setAdSpend(e.target.value)}
                    className="w-full bg-white border border-zinc-200 rounded-none px-3 py-3 text-[11px] text-zinc-700 focus:outline-none focus:border-brand-accent transition-colors cursor-pointer"
                  >
                    <option value="150000">₹1,50,000 / mo</option>
                    <option value="500000">₹5,00,000 / mo</option>
                    <option value="1500000">₹15,00,000 / mo</option>
                    <option value="5000000">₹50,00,000 (50L/mo)</option>
                  </select>
                </div>
              </div>

              <button
                id="btn-generate-strategy"
                type="submit"
                disabled={loading || !businessName || !industry || !description}
                className="w-full mt-2 flex items-center justify-center gap-2 py-4 px-6 rounded-none font-display text-xs font-black uppercase tracking-wider text-white bg-[#0052FF] hover:bg-black disabled:bg-zinc-200 disabled:text-zinc-400 disabled:cursor-not-allowed select-none transition-all duration-300 shadow-sm"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-white" />
                    <span>Analyzing Vectors...</span>
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 text-white fill-white" />
                    <span>Generate Scaling Blueprint</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Results strategical deck */}
          <div className="lg:col-span-12 xl:col-span-7 flex flex-col justify-center min-h-[500px]">
            
            {/* Active Loading Screen */}
            {loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center p-12 text-center"
              >
                <div className="w-16 h-16 rounded-none bg-zinc-50 border border-zinc-200 flex items-center justify-center mb-6 relative shadow-sm">
                  <Loader2 className="w-6 h-6 animate-spin text-brand-accent" />
                  <div className="absolute inset-0 bg-brand-accent/5 rounded-none blur-md" />
                </div>
                <h4 className="text-zinc-800 font-display text-xl uppercase tracking-wider font-bold">Assembling Campaign Vectors</h4>
                <p className="text-zinc-500 font-mono text-xs mt-2 h-6 animate-pulse select-none">
                  {loadingPhrases[loadingStep]}
                </p>
                <div className="w-48 bg-zinc-200 h-1 rounded-none overflow-hidden mt-6 border border-zinc-300">
                  <motion.div
                    className="h-full bg-brand-accent"
                    initial={{ width: "0%" }}
                    animate={{ width: `${((loadingStep + 1) / loadingPhrases.length) * 100}%` }}
                    transition={{ ease: "easeInOut", duration: 0.5 }}
                  />
                </div>
              </motion.div>
            )}

            {/* Empty Context Fallback */}
            {!loading && !strategy && !errorMsg && (
              <div className="text-center p-12 select-none border border-dashed border-zinc-200 rounded-none py-20 bg-zinc-50/50 animate-fade-in">
                <Brain className="w-10 h-10 text-zinc-400 mx-auto mb-4 animate-pulse" />
                <h4 className="text-zinc-650 font-display text-lg uppercase tracking-wider font-bold">Strategy Console Stale</h4>
                <p className="text-zinc-550 font-sans text-xs mt-2 max-w-sm mx-auto leading-relaxed">
                  Provide your business credentials on the left, and watch our algorithmic campaign core project target metrics and creative ad copy ideas natively.
                </p>
              </div>
            )}

            {/* Error or Missing Secrets Prompt */}
            {errorMsg && (
              <motion.div
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                className="p-8 bg-zinc-50 border border-red-200 rounded-none shadow-sm"
              >
                <div className="w-10 h-10 rounded-none bg-red-50 border border-red-200 flex items-center justify-center mb-4">
                  <HelpCircle className="w-5 h-5 text-red-550" />
                </div>
                <h4 className="text-zinc-850 font-display text-lg uppercase tracking-wider font-bold">Audit Synthesis Paused</h4>
                <p className="text-zinc-600 font-sans text-xs mt-1.5 leading-relaxed">
                  {errorMsg}
                </p>

                {promptKeyNeeded && (
                  <div className="mt-6 p-4.5 bg-white border border-zinc-200 rounded-none flex gap-3.5 items-start">
                    <CheckCircle2 className="w-4 h-4 text-brand-accent flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="font-mono text-[9px] text-[#0052FF] uppercase tracking-widest block font-bold">Key Synchronization Setup</span>
                      <p className="text-zinc-650 font-sans text-[11px] mt-1 leading-relaxed">
                        To activate, click on the **Settings &gt; Secrets** panel in Google AI Studio, add a secret named <code className="font-mono bg-zinc-100 px-1.5 py-0.5 text-zinc-800 rounded">GEMINI_API_KEY</code>, then generate audits flawlessly.
                      </p>
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {/* Loaded Strategy Blueprint Panel */}
            {strategy && !loading && (
              <motion.div
                initial={{ opacity: 0, scale: 0.97 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4 }}
                className="flex flex-col gap-6"
              >
                {/* Executive Summary */}
                <div className="p-6 bg-zinc-50 border border-zinc-200 rounded-none shadow-sm">
                  <div className="flex items-center gap-1.5 font-mono text-[9px] text-[#0052FF] uppercase tracking-widest mb-2.5 font-bold">
                    <Brain className="w-3.5 h-3.5 animate-pulse" />
                    <span>TNT Strategic Architecture Audit</span>
                  </div>
                  <p className="text-zinc-800 font-sans text-sm font-medium leading-relaxed italic border-l-2 border-[#0052FF] pl-4">
                    "{strategy.executiveSummary}"
                  </p>
                </div>

                {/* Split metrics dashboard */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
                  {/* Predicted ROI Card */}
                  <div className="p-5 bg-zinc-50 border border-zinc-200 rounded-none flex flex-col justify-between shadow-sm">
                    <div>
                      <div className="font-mono text-[9px] text-zinc-500 uppercase tracking-widest leading-none font-bold">Target ROAS Multiplier</div>
                      <div className="text-4xl font-display text-brand-accent mt-3 font-bold">
                        {strategy.projectedMetrics.roasMultiplier.toFixed(2)}x
                      </div>
                    </div>
                    <div className="mt-4 pt-4 border-t border-zinc-200 text-zinc-400 font-mono text-[9px]">
                      Expected Conversion CTR bounds: {strategy.projectedMetrics.ctrLowBound}% - {strategy.projectedMetrics.ctrHighBound}%
                    </div>
                  </div>

                  {/* CPA reductions */}
                  <div className="p-5 bg-zinc-50 border border-zinc-200 rounded-none flex flex-col justify-between shadow-sm">
                    <div>
                      <div className="font-mono text-[9px] text-zinc-500 uppercase tracking-widest leading-none font-bold">CAC Cost Reduction</div>
                      <div className="text-4xl font-display text-[#0052FF] mt-3 font-bold">
                        -{strategy.projectedMetrics.cpaImprovementPct}%
                      </div>
                    </div>
                    <div className="mt-4 pt-4 border-t border-zinc-200 text-zinc-400 font-mono text-[9px]">
                      Net margin benefit applied on attribution
                    </div>
                  </div>
                </div>

                {/* Budget Allocations Progress Bars */}
                <div className="p-6 bg-zinc-50 border border-zinc-200 rounded-none shadow-sm">
                  <div className="flex items-center gap-1.5 font-mono text-[9px] text-zinc-500 uppercase tracking-widest mb-4 font-bold">
                    <BarChart2 className="w-3.5 h-3.5" />
                    <span>Optimized Channel Allocations</span>
                  </div>

                  <div className="flex flex-col gap-4">
                    {/* Meta */}
                    <div>
                      <div className="flex justify-between text-xs mb-1 font-sans">
                        <span className="text-zinc-700 font-semibold">Meta Ads Sequence</span>
                        <span className="font-mono text-zinc-600 font-bold">{strategy.channelAllocation.metaPercent}%</span>
                      </div>
                      <div className="w-full bg-zinc-200 h-1 rounded-none overflow-hidden border border-zinc-300">
                        <div className="bg-brand-accent h-full animate-pulse" style={{ width: `${strategy.channelAllocation.metaPercent}%` }} />
                      </div>
                    </div>

                    {/* Google */}
                    <div>
                      <div className="flex justify-between text-xs mb-1 font-sans">
                        <span className="text-zinc-700 font-semibold">Google High-Intent Search & Video</span>
                        <span className="font-mono text-zinc-600 font-bold">{strategy.channelAllocation.googlePercent}%</span>
                      </div>
                      <div className="w-full bg-zinc-200 h-1 rounded-none overflow-hidden border border-zinc-300">
                        <div className="bg-[#0052FF] h-full" style={{ width: `${strategy.channelAllocation.googlePercent}%` }} />
                      </div>
                    </div>

                    {/* Programmatic */}
                    <div>
                      <div className="flex justify-between text-xs mb-1 font-sans">
                        <span className="text-zinc-700 font-semibold">Private Programmatic Marketplace (PMP)</span>
                        <span className="font-mono text-zinc-600 font-bold">{strategy.channelAllocation.programmaticPercent}%</span>
                      </div>
                      <div className="w-full bg-zinc-200 h-1 rounded-none overflow-hidden border border-zinc-300">
                        <div className="bg-zinc-500 h-full" style={{ width: `${strategy.channelAllocation.programmaticPercent}%` }} />
                      </div>
                    </div>

                    {/* Creative CRO */}
                    <div>
                      <div className="flex justify-between text-xs mb-1 font-sans">
                        <span className="text-zinc-700 font-semibold">Creative Iteration & Landers CRO</span>
                        <span className="font-mono text-[#0052FF] font-bold">{strategy.channelAllocation.creativeCROPercent}%</span>
                      </div>
                      <div className="w-full bg-zinc-200 h-1 rounded-none overflow-hidden border border-zinc-300">
                        <div className="bg-[#0052FF] h-full opacity-60" style={{ width: `${strategy.channelAllocation.creativeCROPercent}%` }} />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Hyper creative Hooks */}
                <div className="p-6 bg-zinc-50 border border-zinc-200 rounded-none shadow-sm">
                  <div className="flex items-center gap-1.5 font-mono text-[9px] text-zinc-500 uppercase tracking-widest mb-4 font-bold">
                    <MessageSquare className="w-3.5 h-3.5" />
                    <span>Gemini Deployed Scroll-Stopping Hooks</span>
                  </div>

                  <div className="flex flex-col gap-4">
                    {strategy.creativeHooks.map((hook, idx) => (
                      <div key={idx} className="p-4 bg-white border border-zinc-200 rounded-none shadow-sm">
                        <div className="flex justify-between items-center text-[10px] font-mono mb-2">
                          <span className="text-brand-accent uppercase font-bold tracking-wider">{hook.angle}</span>
                          <span className="text-[#0052FF] uppercase font-bold">{hook.targetChannel}</span>
                        </div>
                        <p className="font-sans text-xs text-zinc-800 font-medium leading-relaxed italic">
                          "{hook.hookText}"
                        </p>
                        <div className="border-t border-zinc-150 mt-3 pt-2 text-[10px] font-mono text-zinc-500">
                          <strong className="text-zinc-500 font-semibold font-display">Storyboard Visual Concept:</strong> {hook.visualConcept}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Audience Personas */}
                <div className="p-6 bg-zinc-50 border border-zinc-200 rounded-none shadow-sm">
                  <div className="flex items-center gap-1.5 font-mono text-[9px] text-zinc-500 uppercase tracking-widest mb-4 font-bold">
                    <Target className="w-3.5 h-3.5" />
                    <span>Engineered Audience Segments</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {strategy.targetPersonas.map((persona, idx) => (
                      <div key={idx} className="p-4 bg-white border border-zinc-200 rounded-none flex flex-col justify-between shadow-sm">
                        <div>
                          <div className="flex justify-between items-start text-[10px] font-mono mb-1">
                            <span className="text-[#0052FF] font-bold uppercase tracking-wider">{persona.audiencename}</span>
                            <span className="bg-zinc-50 border border-zinc-200 px-1.5 py-0.5 rounded-none font-bold text-zinc-500 uppercase tracking-widest text-[8px]">{persona.funnelPosition}</span>
                          </div>
                          <div className="text-[10px] text-zinc-400 font-mono mt-0.5 leading-snug">
                            {persona.demographicsDetailed}
                          </div>
                        </div>
                        <div className="border-t border-zinc-155 mt-3 pt-3 text-[11px] font-sans text-zinc-650">
                          <strong className="text-zinc-500 font-semibold font-display">Desire / Trigger Points:</strong> {persona.triggerPoints}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action phases roadmap */}
                <div className="p-6 bg-zinc-50 border border-zinc-200 rounded-none shadow-sm">
                  <div className="flex items-center gap-1.5 font-mono text-[9px] text-zinc-500 uppercase tracking-widest mb-4 font-bold">
                    <Compass className="w-3.5 h-3.5" />
                    <span>Chronological Launch Playbook</span>
                  </div>

                  <div className="flex flex-col gap-3 font-sans">
                    {strategy.actionPlanSteps.map((step, idx) => (
                      <div key={idx} className="flex gap-4 items-start p-3.5 bg-white border border-zinc-200 rounded-none animate-fade-in shadow-sm font-sans">
                        <span className="w-5 h-5 flex-shrink-0 flex items-center justify-center font-mono text-[9px] font-black text-white bg-[#0052FF] rounded-none">
                          0{idx + 1}
                        </span>
                        <p className="text-xs text-zinc-700 font-sans leading-relaxed font-semibold">
                          {step}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>

              </motion.div>
            )}

          </div>

        </div>

      </div>
    </section>
  );
}
