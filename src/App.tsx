/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import Header from "./components/Header";
import Hero from "./components/Hero";
import Identity from "./components/Identity";
import Services from "./components/Services";
import RoasSimulator from "./components/RoasSimulator";
import CaseStudies from "./components/CaseStudies";
import Auditor from "./components/Auditor";
import Footer from "./components/Footer";
import GravityCanvas from "./components/GravityCanvas";

export default function App() {
  const handleScrollToSegment = (selector: string) => {
    const element = document.querySelector(selector);
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  return (
    <div id="root-container" className="min-h-screen bg-white text-zinc-900 font-sans selection:bg-brand-accent/20 selection:text-zinc-900 antialiased overflow-x-hidden scroll-smooth relative">
      {/* 0. Global Interactive Physics Backdrop System */}
      <div className="fixed inset-0 z-0 pointer-events-none opacity-55 select-none md:opacity-65">
        <GravityCanvas />
      </div>

      {/* 1. Header Navigation */}
      <Header onScrollTo={handleScrollToSegment} />

      {/* 2. Hero Billboard */}
      <Hero onScrollTo={handleScrollToSegment} />

      {/* 3. The Nonchalant Philosophy */}
      <Identity />

      {/* 4. Service Channels Playbook */}
      <Services />

      {/* 5. Interactive ROI Growth Simulator */}
      <RoasSimulator />

      {/* 6. Partner Case Studies */}
      <CaseStudies />

      {/* 7. Gemini-Powered Ad Auditor & Strategist */}
      <Auditor />

      {/* 8. Corporate Footer & Physical Branches */}
      <Footer onScrollTo={handleScrollToSegment} />
    </div>
  );
}
