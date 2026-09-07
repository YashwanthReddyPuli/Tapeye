"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, BarChart2, FileText } from "lucide-react";

export default function SidebarNavigation() {
  const pathname = usePathname();

  const navItems = [
    {
      label: "Scanner",
      href: "/",
      icon: <LayoutDashboard size={17} strokeWidth={1.5} className="shrink-0" />,
    },
    {
      label: "Metrics",
      href: "/performance",
      icon: <BarChart2 size={17} strokeWidth={1.5} className="shrink-0" />,
    },
    {
      label: "Architecture",
      href: "/about",
      icon: <FileText size={17} strokeWidth={1.5} className="shrink-0" />,
    },
  ];

  return (
    <aside className="w-60 h-screen bg-[#f4f2eb] border-r border-[#e8e5dc] flex flex-col justify-between shrink-0 sticky top-0 z-50 select-none">
      {/* BRAND HEADER */}
      <div className="px-5 py-4 border-b border-[#e8e5dc]">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-[#c96442] text-white flex items-center justify-center font-bold text-xs shadow-xs">
            T
          </div>
          <div>
            <span className="font-serif text-base tracking-tight font-medium text-[#2c2921]">
              TapEye
            </span>
            <div className="flex items-center gap-1.5 mt-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600" />
              <span className="text-[11px] font-mono text-[#85827a]">
                Online
              </span>
            </div>
          </div>
        </Link>
      </div>

      {/* NAVIGATION LINKS */}
      <div className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-2.5 pb-1.5 text-[10px] font-medium tracking-wider text-[#85827a] uppercase">
          Menu
        </div>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition-colors ${
                isActive
                  ? "bg-[#ede9df] text-[#2c2921]"
                  : "text-[#85827a] hover:text-[#2c2921] hover:bg-[#eae6dc]/60"
              }`}
            >
              <span className={isActive ? "text-[#c96442]" : "text-[#85827a]"}>
                {item.icon}
              </span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>

      {/* FOOTER SYSTEM STATUS CARD */}
      <div className="p-3 border-t border-[#e8e5dc] bg-[#f4f2eb]">
        <div className="p-3 rounded-xl bg-white border border-[#e5e2d8] space-y-1.5 text-[11px] font-mono shadow-[0_1px_2px_rgba(0,0,0,0.02)]">
          <div className="flex items-center justify-between text-[#85827a]">
            <span>Environment</span>
            <span className="text-[#2c2921] font-medium">Local</span>
          </div>
          <div className="flex items-center justify-between text-[#85827a]">
            <span>Architecture</span>
            <span className="text-[#2c2921] font-medium">Late Fusion</span>
          </div>
          <div className="flex items-center justify-between pt-1 border-t border-[#e5e2d8] text-[10px] text-[#85827a]">
            <span>Version</span>
            <span className="text-[#2c2921]">v1.2.0</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
