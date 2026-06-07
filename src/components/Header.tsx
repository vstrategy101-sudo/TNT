/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect } from "react";
import { Menu, X, Rocket, Zap, ArrowRight } from "lucide-react";
import Logo from "./Logo";

interface HeaderProps {
  onScrollTo: (selector: string) => void;
}

export default function Header({ onScrollTo }: HeaderProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navItems = [
    { label: "PHILOSOPHY", target: "#philosophy" },
    { label: "CHANNELS", target: "#channels" },
    { label: "GROWTH MODEL", target: "#simulator" },
    { label: "CASE STUDIES", target: "#cases" },
    { label: "CAMPAIGN AUDIT", target: "#audit" },
  ];

  const handleNavClick = (target: string) => {
    setMobileMenuOpen(false);
    onScrollTo(target);
  };

  return (
    <header
      id="main-nav-header"
      className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-white/90 backdrop-blur-md border-b border-zinc-150 py-3 shadow-sm"
          : "bg-transparent py-5"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        {/* Brand Logo */}
        <button
          id="btn-logo-home"
          onClick={() => handleNavClick("#hero")}
          className="group flex items-center text-left focus:outline-none"
        >
          <Logo className="h-7 md:h-8 text-zinc-900 group-hover:opacity-85 transition-opacity" />
        </button>

        {/* Desktop Navigation */}
        <nav id="desktop-navbar" className="hidden md:flex items-center gap-2 border-l border-r border-zinc-200/80 px-6 py-1 font-mono">
          {navItems.map((item) => (
            <button
              key={item.target}
              id={`nav-link-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
              onClick={() => handleNavClick(item.target)}
              className="px-3.5 py-1.5 font-mono text-[10px] font-bold tracking-widest text-zinc-500 hover:text-zinc-900 transition-all cursor-pointer relative group"
            >
              <span>{item.label}</span>
              <span className="absolute bottom-0 left-3.5 right-3.5 h-[2px] bg-brand-accent scale-x-0 group-hover:scale-x-100 transition-transform origin-left" />
            </button>
          ))}
        </nav>

        {/* Desktop Call to Action */}
        <div className="hidden md:flex items-center">
          <button
            id="btn-header-cta"
            onClick={() => handleNavClick("#audit")}
            className="group relative inline-flex items-center gap-2 px-5 py-2.5 font-sans text-xs font-black tracking-widest text-zinc-900 border border-zinc-900 hover:bg-brand-accent hover:border-brand-accent hover:text-white transition-all uppercase cursor-pointer"
          >
            <Zap className="w-3 h-3 text-brand-accent group-hover:text-white transition-colors animate-pulse" />
            <span>GET FREE AUDIT</span>
            <ArrowRight className="w-3.5 h-3.5 text-zinc-900 group-hover:text-white group-hover:translate-x-1 transition-all" />
          </button>
        </div>

        {/* Mobile menu toggle */}
        <button
          id="btn-mobile-menu-toggle"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 text-zinc-500 hover:text-zinc-900 rounded-lg focus:outline-none"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer Overlay */}
      {mobileMenuOpen && (
        <div
          id="mobile-drawer-overlay"
          className="fixed inset-0 top-[60px] bg-white z-40 flex flex-col px-6 py-6 md:hidden transition-all duration-300 animate-fade-in"
        >
          <div className="flex flex-col gap-4">
            <div className="text-[10px] uppercase font-mono text-zinc-400 tracking-widest border-b border-zinc-100 pb-2">Navigation</div>
            {navItems.map((item) => (
              <button
                key={item.target}
                id={`mobile-nav-link-${item.label.toLowerCase().replace(/\s+/g, '-')}`}
                onClick={() => handleNavClick(item.target)}
                className="w-full text-left py-2 font-display text-3xl font-bold text-zinc-800 hover:text-brand-accent"
              >
                {item.label}
              </button>
            ))}
            
            <div className="mt-8">
              <button
                id="btn-mobile-header-cta"
                onClick={() => handleNavClick("#audit")}
                className="w-full flex items-center justify-center gap-2 py-4 px-6 font-display text-lg tracking-widest text-white bg-brand-accent hover:bg-brand-accent/90 transition-colors"
              >
                <Rocket className="w-5 h-5" />
                <span>GENERATE FREE AD AUDIT</span>
              </button>
            </div>
            
            <div className="mt-auto py-8 flex flex-col gap-2 text-zinc-400 font-mono text-[9px] uppercase tracking-widest text-center">
              <span>Performance Marketing Agency</span>
              <span>Mumbai • Zurich • London</span>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}

