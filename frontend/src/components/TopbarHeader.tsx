"use client";

import React from "react";

interface TopbarHeaderProps {
  breadcrumb?: string;
}

export default function TopbarHeader({
  breadcrumb = "Scanner / Dual-Modal Assessment",
}: TopbarHeaderProps) {
  return (
    <header className="h-13 border-b border-[#e8e5dc] bg-[#fbfaf7]/90 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-40 shrink-0 select-none">
      {/* LEFT BREADCRUMB */}
      <div className="flex items-center gap-1.5 text-xs font-mono text-[#85827a]">
        <span>TapEye</span>
        <span>/</span>
        <span className="text-[#2c2921] font-medium">{breadcrumb}</span>
      </div>

      {/* RIGHT TELEMETRY */}
      <div className="flex items-center gap-2">
        <span className="px-2.5 py-1 rounded-lg bg-[#f4f2eb] text-[11px] font-mono text-[#85827a] border border-[#e8e5dc]">
          Engine: PyTorch / TF
        </span>
        <span className="px-2.5 py-1 rounded-lg bg-emerald-50 text-[11px] font-mono text-emerald-800 border border-emerald-200/80">
          API Connected
        </span>
      </div>
    </header>
  );
}
