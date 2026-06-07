/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { ArrowUp, Clock, MapPin } from "lucide-react";
import { useEffect, useState } from "react";
import Logo from "./Logo";

interface FooterProps {
  onScrollTo: (selector: string) => void;
}

export default function Footer({ onScrollTo }: FooterProps) {
  const [indiaTime, setIndiaTime] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const options: Intl.DateTimeFormatOptions = {
        timeZone: "Asia/Kolkata",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false
      };
      setIndiaTime(new Intl.DateTimeFormat("en-IN", options).format(new Date()));
    };
    
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <footer className="bg-white/85 backdrop-blur-[1px] border-t border-zinc-200 pt-20 pb-10 px-6 select-none relative z-10">
      
      {/* Dynamic Locations Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-12 gap-10 items-start pb-16 border-b border-zinc-200">
        
        {/* Brand details */}
        <div className="md:col-span-4 max-w-xs">
          <div className="flex items-center gap-2">
            <Logo className="h-7 text-zinc-900" />
          </div>
          <p className="mt-4 text-xs font-sans text-zinc-500 leading-relaxed font-normal">
            An elite full-funnel performance marketing and creative architecture agency. We solve structural business-level acquisition problems with quiet, bulletproof confidence and technical engineering.
          </p>

          {/* Real-time Local HQ Time */}
          <div className="mt-6 flex items-center gap-2.5 text-zinc-500 font-mono text-[9px] uppercase tracking-wider font-bold">
            <Clock className="w-3.5 h-3.5 text-[#0052FF] animate-pulse" />
            <span>Mumbai HQ Local Time:</span>
            <span className="text-[#0052FF] font-black tracking-widest">{indiaTime} IST</span>
          </div>
        </div>

        {/* Office Location: Mumbai (Extended span to make layout balanced) */}
        <div className="md:col-span-6">
          <div className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest mb-3 flex items-center gap-1.5 font-bold">
            <MapPin className="w-3.5 h-3.5 text-[#0052FF]" />
            <span>HQ Mumbai Division</span>
          </div>
          <div className="font-sans text-xs text-zinc-700 leading-relaxed font-semibold">
            8th Floor, Naman Chambers,<br />
            C-31, G-Block, Bandra-Kurla Complex,<br />
            Bandra East, Mumbai - 400051
          </div>
          <div className="mt-4 font-mono text-[10px] text-zinc-500 hover:text-[#0052FF] transition-colors">
            mumbai@tntagency.com
          </div>
        </div>

        {/* Quick Nav shortcuts */}
        <div className="md:col-span-2 flex flex-col gap-2.5 text-left md:items-end">
          <div className="font-mono text-[9px] text-zinc-400 uppercase tracking-widest mb-1.5 font-bold">Quick Navigation</div>
          <button onClick={() => onScrollTo("#philosophy")} className="font-mono uppercase tracking-wider text-[11px] text-zinc-650 hover:text-[#0052FF] transition-colors cursor-pointer text-left md:text-right">
            Philosophy
          </button>
          <button onClick={() => onScrollTo("#channels")} className="font-mono uppercase tracking-wider text-[11px] text-zinc-650 hover:text-[#0052FF] transition-colors cursor-pointer text-left md:text-right">
            Our Channels
          </button>
          <button onClick={() => onScrollTo("#simulator")} className="font-mono uppercase tracking-wider text-[11px] text-zinc-650 hover:text-[#0052FF] transition-colors cursor-pointer text-left md:text-right">
            ROAS Calculator
          </button>
          <button onClick={() => onScrollTo("#audit")} className="font-mono uppercase tracking-wider text-[11px] text-zinc-650 hover:text-[#0052FF] transition-colors cursor-pointer text-left md:text-right">
            On-Demand Strategist
          </button>
        </div>

      </div>

      {/* Corporate footer details */}
      <div className="max-w-7xl mx-auto mt-10 flex flex-col sm:flex-row items-center justify-between text-[10px] font-mono text-zinc-500 gap-4 uppercase tracking-wider font-semibold">
        <div>
          © {new Date().getFullYear()} TNT Performance. All rights reserved. Precision scale engineered.
        </div>
        
        <div className="flex items-center gap-6">
          <a href="#" className="hover:text-[#0052FF] transition-colors">Terms of Scale</a>
          <span>•</span>
          <a href="#" className="hover:text-[#0052FF] transition-colors">Attribution Privacy</a>
          <span>•</span>
          <button
            onClick={() => onScrollTo("#hero")}
            className="group flex items-center gap-1.5 hover:text-[#0052FF] transition-colors cursor-pointer"
          >
            <span>Scroll To Top</span>
            <ArrowUp className="w-3.5 h-3.5 text-zinc-400 group-hover:text-[#0052FF] group-hover:-translate-y-0.5 transition-all" />
          </button>
        </div>
      </div>

    </footer>
  );
}
