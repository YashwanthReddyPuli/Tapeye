"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { LayoutDashboard, BarChart2, FileText, ScanEye } from "lucide-react";

import ParticleBackground from "@/components/ParticleBackground";

export default function Sidenavbar({ children }: { children: React.ReactNode }) {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const isScanner = pathname === "/";
  const isPerformance = pathname === "/performance";
  const isAbout = pathname === "/about";

  const navItems = [
    { label: "Scanner", href: "/", icon: <LayoutDashboard size={18} className="shrink-0" />, active: isScanner },
    { label: "Performance", href: "/performance", icon: <BarChart2 size={18} className="shrink-0" />, active: isPerformance },
    { label: "Architecture", href: "/about", icon: <FileText size={18} className="shrink-0" />, active: isAbout },
  ];

  return (
    <div className="relative min-h-screen overflow-hidden bg-[#121110] text-[#faf9f5]">
      {/* 0. NEURAL PARTICLE NETWORK BASE LAYER */}
      <ParticleBackground />

      {/* 1. DYNAMIC AMBIENT GRADIENT BACKGROUND LIGHT BLOBS */}
      <div className="pointer-events-none absolute -left-[10%] -top-[10%] h-[500px] w-[500px] animate-[pulse_8s_ease-in-out_infinite] rounded-full bg-[#b05730]/15 blur-[120px]" />
      <div className="pointer-events-none absolute top-[40%] -right-[5%] h-[600px] w-[600px] animate-[pulse_12s_ease-in-out_infinite_reverse] rounded-full bg-[#9c87f5]/15 blur-[150px]" />


      {/* 2. FOREGROUND CONTENT & LIQUID GLASS SIDEBAR */}
      <div className="relative z-10 flex h-screen w-full overflow-hidden">
        {/* LIQUID FROSTED GLASS SIDEBAR */}
        <aside
          onMouseEnter={() => setIsOpen(true)}
          onMouseLeave={() => setIsOpen(false)}
          className={`${
            isOpen ? "w-56" : "w-16"
          } flex flex-col bg-[#1a1918]/40 backdrop-blur-2xl border-r border-white/5 shadow-[4px_0_24px_-2px_rgba(0,0,0,0.2)] transition-all duration-300 ease-in-out shrink-0 select-none z-30`}
        >
          {/* 3. BRAND NEW TAPEYE LOGO */}
          <div className="flex h-16 items-center border-b border-white/5 px-3 overflow-hidden">
            <Link href="/" className="flex items-center gap-3 px-1">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-[#b05730] to-[#8a4223] shadow-lg shadow-[#b05730]/20 border border-white/10">
                <ScanEye className="h-4 w-4 text-white" />
              </div>
              {isOpen && (
                <span className="font-serif text-xl tracking-tight text-white whitespace-nowrap">
                  Tap<span className="text-[#b05730]">Eye</span>
                </span>
              )}
            </Link>
          </div>

          {/* NAVIGATION LINKS */}
          <ScrollArea className="flex-1">
            <nav className="p-2.5 space-y-1.5">
              {navItems.map((item) => (
                <Link key={item.href} href={item.href}>
                  <Button
                    variant="ghost"
                    className={`w-full justify-start gap-3 h-10 px-3 text-xs font-medium rounded-lg transition-all duration-300 ${
                      item.active
                        ? "bg-white/10 text-white border border-white/10 shadow-sm"
                        : "text-[#b7b5a9] hover:bg-white/5 hover:text-white"
                    }`}
                  >
                    {item.icon}
                    {isOpen && <span className="whitespace-nowrap">{item.label}</span>}
                  </Button>
                </Link>
              ))}
            </nav>
          </ScrollArea>
        </aside>

        {/* MAIN VIEWPORT */}
        <main className="flex-1 h-screen overflow-y-auto p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
