/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useEffect, useRef, useState } from "react";

interface Particle {
  x: number;
  y: number;
  baseX: number;
  baseY: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
  label: string;
  speedMultiplier: number;
  orbitRadius?: number;
  angle?: number;
}

interface Attractor {
  x: number;
  y: number;
  label: string;
  size: number;
  pulse: number;
}

export default function GravityCanvas() {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [attractors, setAttractors] = useState<Attractor[]>([
    { x: 200, y: 180, label: "Server-Side CAPI", size: 5, pulse: 0 },
    { x: 500, y: 350, label: "Attribution Engine", size: 6, pulse: 1.5 },
    { x: 800, y: 220, label: "Bid Multiplier", size: 5, pulse: 3.1 },
  ]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let width = canvas.width = containerRef.current?.clientWidth || 800;
    let height = canvas.height = containerRef.current?.clientHeight || 500;

    // Handle Resize
    const handleResize = () => {
      if (!containerRef.current || !canvas) return;
      width = canvas.width = containerRef.current.clientWidth;
      height = canvas.height = containerRef.current.clientHeight;
    };

    window.addEventListener("resize", handleResize);

    // Create background grid and interactive floating particles
    const particleLabels = [
      "CR Scale", "Hold Rate", "CTR Lift", "Bids Optim", "Server Sync",
      "LTV Bound", "CAPI signal", "GTM Pixel", "Ad Spend", "SOV Dominance",
      "Retention", "Lander CRO", "Friction cut", "Meta CAPI", "Lakhs/Day", "Core ROI"
    ];

    const particles: Particle[] = [];
    // Generate some structured particle points on a grid
    const cols = 15;
    const rows = 10;
    const xSpacing = width / (cols + 1);
    const ySpacing = height / (rows + 1);

    for (let c = 1; c <= cols; c++) {
      for (let r = 1; r <= rows; r++) {
        const baseX = c * xSpacing + (Math.random() - 0.5) * 15;
        const baseY = r * ySpacing + (Math.random() - 0.5) * 15;
        const labelIndex = Math.floor(Math.random() * particleLabels.length);
        
        particles.push({
          x: baseX,
          y: baseY,
          baseX,
          baseY,
          vx: (Math.random() - 0.5) * 0.4,
          vy: (Math.random() - 0.5) * 0.4,
          radius: Math.random() * 2 + 1,
          color: Math.random() > 0.7 ? "#0052FF" : "rgba(13,13,17,0.15)",
          label: Math.random() > 0.88 ? particleLabels[labelIndex] : "",
          speedMultiplier: Math.random() * 0.02 + 0.015,
          angle: Math.random() * Math.PI * 2,
          orbitRadius: Math.random() * 40 + 20
        });
      }
    }

    // Keep track of Mouse Coordinator
    let mouse = { x: -1000, y: -1000, active: false };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = e.clientX - rect.left;
      mouse.y = e.clientY - rect.top;
      mouse.active = true;
    };

    const handleMouseLeave = () => {
      mouse.x = -1000;
      mouse.y = -1000;
      mouse.active = false;
    };

    const handleGlobalClick = (e: MouseEvent) => {
      // Avoid intercepting interactive elements
      const target = e.target as HTMLElement;
      if (
        !target ||
        target.tagName === "BUTTON" ||
        target.tagName === "A" ||
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.tagName === "SELECT" ||
        target.closest("button") ||
        target.closest("a") ||
        target.closest("input") ||
        target.closest("textarea") ||
        target.closest("select")
      ) {
        return;
      }

      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;

      // Add a persistent Attractor corresponding to direct agency architectures!
      const labelOptions = [
        "Server Signal", "Margin attribution", "Recom Bid",
        "CRO Lander", "SOV Hook", "ROAS Multiplier", "LTV Loop"
      ];
      const selectedLabel = labelOptions[Math.floor(Math.random() * labelOptions.length)];

      setAttractors(prev => {
        // Limit to max 6 attractors
        const updated = [...prev, { x: clickX, y: clickY, label: selectedLabel, size: 6, pulse: 0 }];
        if (updated.length > 6) updated.shift();
        return updated;
      });
    };

    window.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseleave", handleMouseLeave);
    window.addEventListener("click", handleGlobalClick);

    // Animation loop mimicking Antigravity aesthetic
    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // 1. Draw elegant lightweight grid background lines
      ctx.strokeStyle = "rgba(13,13,17,0.035)";
      ctx.lineWidth = 1;
      const step = 45;
      for (let x = 0; x < width; x += step) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }
      for (let y = 0; y < height; y += step) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      // Update attractor pulse rates
      attractors.forEach(a => {
        a.pulse += 0.05;
      });

      // 2. Draw attraction fields / orbits
      attractors.forEach(a => {
        const pulseRadius = 30 + Math.sin(a.pulse) * 12;
        // Drawing outer orbit boundaries
        ctx.strokeStyle = "rgba(0, 82, 255, 0.035)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(a.x, a.y, pulseRadius * 2, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = "rgba(13, 13, 17, 0.02)";
        ctx.beginPath();
        ctx.arc(a.x, a.y, pulseRadius * 3.5, 0, Math.PI * 2);
        ctx.stroke();

        // Target core center
        ctx.fillStyle = "#0052FF";
        ctx.beginPath();
        ctx.arc(a.x, a.y, a.size, 0, Math.PI * 2);
        ctx.fill();

        // Micro ripples
        ctx.strokeStyle = "rgba(0, 82, 255, 0.15)";
        ctx.beginPath();
        ctx.arc(a.x, a.y, 4 + Math.sin(a.pulse * 2) * 3, 0, Math.PI * 2);
        ctx.stroke();

        // Technical typography label
        ctx.fillStyle = "rgba(13, 13, 17, 0.65)";
        ctx.font = "italic 9px JetBrains Mono, monospace";
        ctx.textAlign = "center";
        ctx.fillText(a.label, a.x, a.y - 14);
      });

      // 3. Process and draw active physics particles
      particles.forEach(p => {
        // Base orbit oscillations
        if (p.angle !== undefined) {
          p.angle += p.speedMultiplier;
          // Slowly drift original base positions to make the grid breathe
          p.baseX += Math.cos(p.angle) * 0.12;
          p.baseY += Math.sin(p.angle) * 0.12;
        }

        let targetX = p.baseX;
        let targetY = p.baseY;

        // Apply mouse gravity bend
        if (mouse.active) {
          const dx = mouse.x - p.x;
          const dy = mouse.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 185) {
            // Anti-gravity repulsion or push-pull based on distance
            const force = (185 - dist) / 185;
            targetX -= dx * force * 0.45;
            targetY -= dy * force * 0.45;
          }
        }

        // Apply attractors solid orbits
        attractors.forEach(a => {
          const dx = a.x - p.x;
          const dy = a.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 150) {
            const force = (150 - dist) / 150;
            // Guide particles around the attractor
            targetX += (a.x - targetX) * force * 0.15;
            targetY += (a.y - targetY) * force * 0.15;
          }
        });

        // Soft fluid ease towards target positions
        p.vx += (targetX - p.x) * 0.07;
        p.vy += (targetY - p.y) * 0.07;
        p.vx *= 0.85;
        p.vy *= 0.85;

        p.x += p.vx;
        p.y += p.vy;

        // Render point
        ctx.fillStyle = p.color;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();

        // Attractor connector lines
        attractors.forEach(a => {
          const dx = a.x - p.x;
          const dy = a.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 75 && p.color === "#0052FF") {
            ctx.strokeStyle = `rgba(0, 82, 255, ${0.1 * (1 - dist / 75)})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(a.x, a.y);
            ctx.stroke();
          }
        });

        // Typography labels to inject elegant storytelling
        if (p.label) {
          ctx.fillStyle = "rgba(13, 13, 17, 0.4)";
          ctx.font = "8px JetBrains Mono, monospace";
          ctx.textAlign = "left";
          ctx.fillText(p.label, p.x + 6, p.y + 2);
          
          // Tiny anchor dot
          ctx.fillStyle = "#0052FF";
          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius + 0.5, 0, Math.PI * 2);
          ctx.fill();
        }
      });

      // Simple mouse pointer locator indicator
      if (mouse.active) {
        ctx.strokeStyle = "rgba(0, 82, 255, 0.18)";
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, 8, 0, Math.PI * 2);
        ctx.stroke();

        ctx.strokeStyle = "rgba(0, 82, 255, 0.05)";
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, 25, 0, Math.PI * 2);
        ctx.stroke();
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    // Cleanup events
    return () => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseleave", handleMouseLeave);
      window.removeEventListener("click", handleGlobalClick);
      cancelAnimationFrame(animationFrameId);
    };
  }, [attractors]);

  return (
    <div ref={containerRef} className="absolute inset-0 w-full h-full pointer-events-none select-none overflow-hidden">
      <canvas ref={canvasRef} className="block w-full h-full pointer-events-none" />
    </div>
  );
}
