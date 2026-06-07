/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { motion } from "motion/react";
import { Coffee, Layers, BarChart } from "lucide-react";

export default function Identity() {
  const pillars = [
    {
      icon: <Layers className="w-5 h-5 text-brand-accent" />,
      title: "SCALE IS A TECH PROBLEM",
      description: "Modern performance marketing is no longer about guessing. We solve the attribution gap using Server-Side GTM, Meta CAPI, and custom first-party custom SQL dashboards before expanding Rupee spend.",
    },
    {
      icon: <BarChart className="w-5 h-5 text-brand-accent" />,
      title: "CREATIVE INTELLIGENCE",
      description: "Where high-retention direct storytelling meets algorithmic feedback loops. We build and deploy 50+ monthly videography angles, conducting rapid hook-rate and hold-rate forensics to capture attention.",
    },
    {
      icon: <Coffee className="w-5 h-5 text-brand-accent" />,
      title: "DECISIVE REVENUE SPRINTS",
      description: "We look beyond standard dashboards to maximize the profit potential of every single click. We execute CRO sprints, optimize post-purchase LTV loops, and harden account frameworks continuously.",
    },
  ];

  return (
    <section
      id="philosophy"
      className="py-24 bg-white/85 backdrop-blur-[1px] border-t border-zinc-200 px-6 relative overflow-hidden"
    >
      <div className="absolute top-1/2 right-10 -translate-y-1/2 w-96 h-96 bg-brand-accent/5 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
          
          {/* Typographical Dictionary definition Card */}
          <div className="lg:col-span-12 xl:col-span-5 select-none">
            <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">The Verbal Origin</span>
            <h2 className="text-4xl md:text-5xl font-extrabold text-zinc-900 mt-2 font-display uppercase tracking-tight">
              Explosive Scale.<br />Absolute Clarity.
            </h2>
            
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="mt-6 p-6 bg-zinc-50 border border-zinc-200 rounded-none relative"
            >
              <div className="font-mono text-xs text-brand-accent font-bold uppercase tracking-wider">tnt·performance</div>
              <div className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest mt-0.5">/ˌtēˌenˈtē/ • NOUN & SYSTEM</div>
              
              <blockquote className="mt-4 font-sans text-sm text-zinc-700 leading-relaxed font-normal">
                "An elite performance paradigm engineered to detonate growth bottlenecks, optimize unit economics, and solve complex business-level customer acquisition problems with explosive velocity."
              </blockquote>
              
              <div className="border-t border-zinc-200 mt-4 pt-4 text-[10px] font-mono text-zinc-500 flex justify-between items-center">
                <span>REF: SYSTEM DIRECT-HANDLING</span>
                <span className="text-brand-accent font-bold">ACTIVE DEPLOYMENT</span>
              </div>
            </motion.div>

            <p className="mt-6 text-zinc-600 font-sans text-xs leading-relaxed">
              True expertise shouldn't look frantic. Many agencies wrestle with trivial vanity metrics while ignoring true operating margins. At TNT, we target and solve structural business-level bottlenecks with pristine engineering architecture, letting our explosive ROAS speak for itself.
            </p>
          </div>

          {/* Pillars of Effortless Growth */}
          <div className="lg:col-span-12 xl:col-span-7 flex flex-col gap-6">
            <span className="font-mono text-xs text-zinc-500 tracking-[2px] uppercase">Our Action Pillars</span>
            <h3 className="text-2xl font-bold uppercase font-display tracking-wider text-zinc-800">
              THE INTELLECT OF INFRASTRUCTURE
            </h3>

            <div className="grid grid-cols-1 gap-4 mt-2">
              {pillars.map((pillar, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, y: 15 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                  id={`philosophy-pillar-card-${i}`}
                  className="p-6 bg-zinc-50 border border-zinc-200 rounded-none group hover:border-brand-accent hover:bg-white transition-all flex gap-5 items-start"
                >
                  <div className="p-3 bg-white border border-zinc-200 rounded-none group-hover:border-brand-accent transition-colors flex-shrink-0">
                    {pillar.icon}
                  </div>
                  <div>
                    <h4 className="font-display text-lg uppercase text-zinc-800 group-hover:text-brand-accent transition-colors font-bold">
                      {pillar.title}
                    </h4>
                    <p className="font-sans text-xs text-zinc-600 mt-2 leading-relaxed">
                      {pillar.description}
                    </p>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}

