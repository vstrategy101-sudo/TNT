/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Sparkles, Percent, ShoppingBag, Eye, TrendingUp } from "lucide-react";

export default function RoasSimulator() {
  const [adSpend, setAdSpend] = useState(500000); // 5 Lakhs default
  const [ctr, setCtr] = useState(1.5);
  const [conversionRate, setConversionRate] = useState(1.8);
  const [avgOrderValue, setAvgOrderValue] = useState(1500); // INR 1500 default

  // Math models for Indian market CPM scales
  // Current Baseline Specs
  const baselineImpressions = adSpend * 5; // Assumed ₹200 CPM standard on Meta/Google India
  const baselineClicks = Math.round((baselineImpressions * ctr) / 100);
  const baselineCpc = baselineClicks > 0 ? adSpend / baselineClicks : 0;
  const baselinePurchases = Math.round((baselineClicks * conversionRate) / 100);
  const baselineRevenue = baselinePurchases * avgOrderValue;
  const baselineROAS = adSpend > 0 ? baselineRevenue / adSpend : 0;
  const baselineCPA = baselinePurchases > 0 ? adSpend / baselinePurchases : 0;

  // TNT Optimized Specs
  // We model: CTR increases by 1.35x, Conversion Rate increases by 1.5x (better landing page + hook matches), CPM decreases by 10% (better ad quality score)
  const tntCTR = Number((ctr * 1.35).toFixed(2));
  const tntConvs = Number((conversionRate * 1.5).toFixed(2));
  
  const optimizedImpressions = adSpend * 5.55; // CPM falls from ₹200 to ₹180 due to better quality ad scores
  const optimizedClicks = Math.round((optimizedImpressions * tntCTR) / 100);
  const optimizedPurchases = Math.round((optimizedClicks * tntConvs) / 100);
  const optimizedRevenue = optimizedPurchases * avgOrderValue;
  const optimizedROAS = adSpend > 0 ? optimizedRevenue / adSpend : 0;
  const optimizedCPA = optimizedPurchases > 0 ? adSpend / optimizedPurchases : 0;

  // Lift comparison
  const revenueLift = optimizedRevenue - baselineRevenue;
  const cpaSaving = baselineCPA - optimizedCPA;
  const cpaSavingPercent = baselineCPA > 0 ? (cpaSaving / baselineCPA) * 100 : 0;

  // Chart data
  const chartData = [
    { name: "INDUSTRY BASELINE", revenue: baselineRevenue, cpa: baselineCPA, label: `Revenue: ₹${baselineRevenue.toLocaleString('en-IN')}` },
    { name: "TNT OPTIMIZED COHORT", revenue: optimizedRevenue, cpa: optimizedCPA, label: `Revenue: ₹${optimizedRevenue.toLocaleString('en-IN')}` }
  ];

  return (
    <section
      id="simulator"
      className="py-24 bg-white/85 backdrop-blur-[1px] border-t border-zinc-200 px-6 relative animate-fade-in"
    >
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-brand-accent/5 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        <div className="max-w-3xl mb-12 select-none">
          <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">Data Intelligence Tool</span>
          <h2 className="text-4xl md:text-5xl font-black text-zinc-900 mt-1 font-display uppercase tracking-tight">
            PERFORMATIVE ROAS SCALES<span className="text-brand-accent">.</span>
          </h2>
          <p className="mt-3 text-sm text-zinc-600 font-sans leading-relaxed">
            Stop guessing your scales. Adjust the parameters of your current India performance metrics below, and watch our dynamic mathematical model show what effortless optimization does to your bottom line.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-stretch font-sans">
          
          {/* Slider input metrics deck */}
          <div className="lg:col-span-5 bg-zinc-50 border border-zinc-200 p-8 rounded-none flex flex-col justify-between">
            <div>
              <div className="flex items-center gap-2 pb-4 border-b border-zinc-200">
                <Sparkles className="w-4 h-4 text-brand-accent animate-pulse" />
                <span className="font-mono text-[10px] text-zinc-600 uppercase tracking-widest font-black">Active Model Controls</span>
              </div>

              {/* Slider 1: Ad Spend */}
              <div className="mt-6">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-1.5 font-sans text-xs font-bold uppercase tracking-wider text-zinc-700">
                    <TrendingUp className="w-3.5 h-3.5 text-brand-accent" />
                    <span>Monthly Ad Spend</span>
                  </div>
                  <span className="font-mono text-xs font-bold text-white bg-[#0052FF] px-2.5 py-0.5 rounded-none">
                    ₹{adSpend.toLocaleString('en-IN')}
                  </span>
                </div>
                <input
                  id="simulator-range-adspend"
                  type="range"
                  min="50000"
                  max="5000000"
                  step="50000"
                  value={adSpend}
                  onChange={(e) => setAdSpend(Number(e.target.value))}
                  className="w-full h-1 bg-zinc-200 rounded-none appearance-none cursor-pointer accent-brand-accent"
                />
                <div className="flex justify-between text-[9px] font-mono text-zinc-400 mt-1 uppercase font-bold">
                  <span>₹50,000</span>
                  <span>₹50,00,000 (50 Lakhs)</span>
                </div>
              </div>

              {/* Slider 2: CTR */}
              <div className="mt-6">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-1.5 font-sans text-xs font-bold uppercase tracking-wider text-zinc-700">
                    <Eye className="w-3.5 h-3.5 text-brand-accent" />
                    <span>Current CTR (Click-Through)</span>
                  </div>
                  <span className="font-mono text-xs font-bold text-white bg-[#0052FF] px-2.5 py-0.5 rounded-none">
                    {ctr}%
                  </span>
                </div>
                <input
                  id="simulator-range-ctr"
                  type="range"
                  min="0.5"
                  max="5"
                  step="0.1"
                  value={ctr}
                  onChange={(e) => setCtr(Number(e.target.value))}
                  className="w-full h-1 bg-zinc-200 rounded-none appearance-none cursor-pointer accent-brand-accent"
                />
                <div className="flex justify-between text-[9px] font-mono text-zinc-400 mt-1 uppercase font-bold">
                  <span>0.5%</span>
                  <span>5.0%</span>
                </div>
              </div>

              {/* Slider 3: Conversion Rate */}
              <div className="mt-6">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-1.5 font-sans text-xs font-bold uppercase tracking-wider text-zinc-700">
                    <Percent className="w-3.5 h-3.5 text-brand-accent" />
                    <span>Current Conversion Rate</span>
                  </div>
                  <span className="font-mono text-xs font-bold text-white bg-[#0052FF] px-2.5 py-0.5 rounded-none">
                    {conversionRate}%
                  </span>
                </div>
                <input
                  id="simulator-range-conv"
                  type="range"
                  min="0.5"
                  max="6"
                  step="0.1"
                  value={conversionRate}
                  onChange={(e) => setConversionRate(Number(e.target.value))}
                  className="w-full h-1 bg-zinc-200 rounded-none appearance-none cursor-pointer accent-brand-accent"
                />
                <div className="flex justify-between text-[9px] font-mono text-zinc-400 mt-1 uppercase font-bold">
                  <span>0.5%</span>
                  <span>6.0%</span>
                </div>
              </div>

              {/* Slider 4: Average Order Value */}
              <div className="mt-6">
                <div className="flex justify-between items-center mb-2">
                  <div className="flex items-center gap-1.5 font-sans text-xs font-bold uppercase tracking-wider text-zinc-700">
                    <ShoppingBag className="w-3.5 h-3.5 text-brand-accent" />
                    <span>Average Client Value / AOV</span>
                  </div>
                  <span className="font-mono text-xs font-bold text-white bg-[#0052FF] px-2.5 py-0.5 rounded-none">
                    ₹{avgOrderValue.toLocaleString('en-IN')}
                  </span>
                </div>
                <input
                  id="simulator-range-aov"
                  type="range"
                  min="100"
                  max="15000"
                  step="100"
                  value={avgOrderValue}
                  onChange={(e) => setAvgOrderValue(Number(e.target.value))}
                  className="w-full h-1 bg-zinc-200 rounded-none appearance-none cursor-pointer accent-brand-accent"
                />
                <div className="flex justify-between text-[9px] font-mono text-zinc-400 mt-1 uppercase font-bold">
                  <span>₹100</span>
                  <span>₹15,000</span>
                </div>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-zinc-200 text-zinc-400 font-mono text-[9px] flex justify-between uppercase font-bold">
              <span>*Metrics assume standardized Indian media bidding</span>
              <span>v2.1</span>
            </div>
          </div>

          {/* Results comparisons and charts */}
          <div className="lg:col-span-7 grid grid-cols-1 md:grid-cols-2 gap-6 items-stretch">
            
            {/* Visual Comparative Graph Card */}
            <div className="bg-zinc-50 border border-zinc-200 p-6 rounded-none flex flex-col justify-between shadow-sm">
              <div>
                <span className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest font-bold">Revenue Output Modeling</span>
                <h3 className="text-zinc-800 font-display text-xl uppercase tracking-wider mt-1 font-bold">Direct Comparative Lift</h3>
              </div>

              {/* Recharts Component block */}
              <div className="h-56 mt-4 relative w-full select-none" id="simulated-chart-container font-mono text-xs">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 15, right: 10, left: 10, bottom: 5 }}>
                    <XAxis
                      dataKey="name"
                      stroke="#888888"
                      fontSize={8}
                      fontFamily="JetBrains Mono"
                      tickLine={false}
                      axisLine={false}
                    />
                    <YAxis
                      stroke="#888888"
                      fontSize={8}
                      fontFamily="JetBrains Mono"
                      type="number"
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={(v) => `₹${v >= 100000 ? (v / 100000).toFixed(0) + 'L' : v}`}
                    />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#ffffff", borderColor: "rgba(13,13,17,0.1)", borderRadius: "0px" }}
                      labelStyle={{ color: "#333333", fontSize: "10px", fontWeight: "bold", fontFamily: "JetBrains Mono" }}
                      itemStyle={{ color: "#0052FF", fontSize: "11px", fontWeight: "bold" }}
                      formatter={(v: any) => [`₹${v.toLocaleString('en-IN')}`, "Estimated Revenue"]}
                    />
                    <Bar dataKey="revenue" radius={[0, 0, 0, 0]} maxBarSize={50}>
                      <Cell fill="#a1a1aa" />
                      <Cell fill="url(#nonchalantGradient)" />
                    </Bar>
                    {/* Glowing digital-blue gradient specs inside svg */}
                    <defs>
                      <linearGradient id="nonchalantGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor="#0052FF" stopOpacity={0.9} />
                        <stop offset="100%" stopColor="#0052FF" stopOpacity={0.25} />
                      </linearGradient>
                    </defs>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Mini statistic banner */}
              <div className="mt-4 p-4 bg-white rounded-none border border-zinc-200 flex justify-between items-center shadow-sm">
                <div>
                  <div className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest font-bold">Ad Spend Net Lift</div>
                  <div className="font-display text-3xl text-brand-accent mt-0.5 leading-none font-bold">
                    +₹{revenueLift.toLocaleString('en-IN')}
                  </div>
                </div>
                <div className="text-right">
                  <div className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest font-bold">Attributable ROAS</div>
                  <div className="font-display text-2xl text-zinc-800 px-2.5 py-1 bg-zinc-50 border border-zinc-200 rounded-none mt-1 leading-none inline-block font-bold">
                    {optimizedROAS.toFixed(2)}X
                  </div>
                </div>
              </div>
            </div>

            {/* Split statistics comparisons */}
            <div className="flex flex-col gap-4">
              
              {/* Stat card 1: ROAS breakdown */}
              <div className="flex-grow bg-zinc-50 border border-zinc-200 p-6 rounded-none flex flex-col justify-between shadow-sm">
                <div>
                  <span className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest font-bold">Return on Ad Spend</span>
                  <h4 className="text-zinc-800 font-display text-lg uppercase tracking-wider mt-1 font-bold">ROAS Optimization</h4>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-4 items-end">
                  <div>
                    <div className="text-[10px] font-mono text-zinc-400 uppercase font-bold">Industry Avg</div>
                    <div className="text-3xl font-display text-zinc-500 mt-0.5 leading-none">{baselineROAS.toFixed(2)}x</div>
                  </div>
                  <div className="border-l border-zinc-200 pl-4">
                    <div className="text-[10px] font-mono text-brand-accent uppercase font-bold">TNT System</div>
                    <div className="text-4.5xl font-display text-brand-accent mt-0.5 leading-none font-bold">{optimizedROAS.toFixed(2)}x</div>
                  </div>
                </div>
              </div>

              {/* Stat card 2: CPA stats */}
              <div className="flex-grow bg-zinc-50 border border-zinc-200 p-6 rounded-none flex flex-col justify-between shadow-sm">
                <div>
                  <span className="font-mono text-[9px] text-zinc-500 uppercase tracking-widest font-bold">Customer Acquisition Costs</span>
                  <h4 className="text-zinc-800 font-display text-lg uppercase tracking-wider mt-1 font-bold">CPA Compression</h4>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-4 items-end">
                  <div>
                    <div className="text-[10px] font-mono text-zinc-400 uppercase font-bold">Baseline CPA</div>
                    <div className="text-3xl font-display text-zinc-500 mt-0.5 leading-none">₹{Math.round(baselineCPA).toLocaleString('en-IN')}</div>
                  </div>
                  <div className="border-l border-zinc-200 pl-4">
                    <div className="text-[10px] font-mono text-brand-accent uppercase font-bold">Compress Target</div>
                    <div className="text-4.5xl font-display text-brand-accent mt-0.5 leading-none font-bold">₹{Math.round(optimizedCPA).toLocaleString('en-IN')}</div>
                  </div>
                </div>
                
                {cpaSavingPercent > 0 && (
                  <div className="mt-3.5 text-[9px] font-mono text-brand-accent flex items-center gap-1 bg-brand-accent/5 border border-brand-accent/20 px-2 py-1 rounded-none w-fit uppercase font-semibold">
                    <span>Compressing CPA by {cpaSavingPercent.toFixed(1)}%</span>
                  </div>
                )}
              </div>

            </div>

          </div>

        </div>
      </div>
    </section>
  );
}

