"use client";

import React from "react";
import { Music, Eye, Cpu, ShieldCheck, AlertTriangle, XCircle } from "lucide-react";

interface BranchProbs {
  Good: number;
  Borderline: number;
  Bad: number;
}

interface ScanResultData {
  verdict: "Good" | "Borderline" | "Bad" | string;
  fusion_confidence: number;
  acoustic_probs: BranchProbs;
  visual_probs: BranchProbs;
}

interface ResultsDashboardProps {
  results: ScanResultData;
}

export default function ResultsDashboard({ results }: ResultsDashboardProps) {
  const getTopClass = (probs: BranchProbs) => {
    let topLabel = "Good";
    let maxVal = -1;
    if (probs) {
      Object.entries(probs).forEach(([label, val]) => {
        if (val > maxVal) {
          maxVal = val;
          topLabel = label;
        }
      });
    }
    return { label: topLabel, confidence: maxVal > 0 ? maxVal : 0 };
  };

  const acousticTop = getTopClass(results.acoustic_probs);
  const visualTop = getTopClass(results.visual_probs);

  const getVerdictTheme = (verdict: string) => {
    switch (verdict.toLowerCase()) {
      case "good":
        return {
          bg: "bg-emerald-950/30",
          border: "border-emerald-700/50",
          text: "text-emerald-400",
          icon: <ShieldCheck className="w-8 h-8 text-emerald-400" />,
        };
      case "borderline":
        return {
          bg: "bg-amber-950/30",
          border: "border-amber-700/50",
          text: "text-amber-400",
          icon: <AlertTriangle className="w-8 h-8 text-amber-400" />,
        };
      case "bad":
      default:
        return {
          bg: "bg-rose-950/30",
          border: "border-rose-700/50",
          text: "text-rose-400",
          icon: <XCircle className="w-8 h-8 text-rose-400" />,
        };
    }
  };

  const verdictStyle = getVerdictTheme(results.verdict);

  return (
    <div className="w-full max-w-4xl space-y-6">
      {/* UNIMODAL CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* ACOUSTIC BRANCH CARD */}
        <div className="p-6 rounded-2xl bg-[#24231f] border border-[#383630] flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#a3a096]">
              <Music className="w-4 h-4 text-primary" /> Acoustic Branch
            </span>
            <span className="text-xs px-2.5 py-1 rounded-full bg-[#1b1a17] text-[#e6e4df] border border-[#383630] font-mono">
              FFT + MFCC
            </span>
          </div>

          <div className="my-4">
            <p className="text-3xl font-bold text-[#e6e4df] tracking-tight capitalize">
              {acousticTop.label}
            </p>
            <p className="text-xs text-[#a3a096] mt-1">
              Top predicted condition class
            </p>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-mono text-[#a3a096]">
              <span>Confidence</span>
              <span className="text-primary font-bold">
                {(acousticTop.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-[#1b1a17] h-2 rounded-full overflow-hidden border border-[#383630]">
              <div
                className="bg-primary h-full rounded-full transition-all duration-500"
                style={{ width: `${acousticTop.confidence * 100}%` }}
              />
            </div>
          </div>
        </div>

        {/* VISUAL BRANCH CARD */}
        <div className="p-6 rounded-2xl bg-[#24231f] border border-[#383630] flex flex-col justify-between shadow-sm">
          <div className="flex items-center justify-between">
            <span className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#a3a096]">
              <Eye className="w-4 h-4 text-purple-400" /> Visual Branch
            </span>
            <span className="text-xs px-2.5 py-1 rounded-full bg-[#1b1a17] text-[#e6e4df] border border-[#383630] font-mono">
              MobileNetV2
            </span>
          </div>

          <div className="my-4">
            <p className="text-3xl font-bold text-[#e6e4df] tracking-tight capitalize">
              {visualTop.label}
            </p>
            <p className="text-xs text-[#a3a096] mt-1">
              Top predicted surface condition
            </p>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-mono text-[#a3a096]">
              <span>Confidence</span>
              <span className="text-purple-400 font-bold">
                {(visualTop.confidence * 100).toFixed(1)}%
              </span>
            </div>
            <div className="w-full bg-[#1b1a17] h-2 rounded-full overflow-hidden border border-[#383630]">
              <div
                className="bg-purple-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${visualTop.confidence * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {/* LATE FUSION CARD */}
      <div
        className={`p-6 rounded-2xl border ${verdictStyle.bg} ${verdictStyle.border} shadow-md transition-all duration-300 flex flex-col md:flex-row items-center justify-between gap-6`}
      >
        <div className="flex items-center gap-4">
          <div className="p-3.5 bg-[#1b1a17] rounded-2xl border border-[#383630]">
            {verdictStyle.icon}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-primary" />
              <span className="text-xs font-semibold uppercase tracking-wider text-[#a3a096]">
                Late-Fusion Meta Verdict
              </span>
            </div>
            <h3 className={`text-4xl font-extrabold tracking-tight mt-1 capitalize ${verdictStyle.text}`}>
              {results.verdict} Quality
            </h3>
          </div>
        </div>

        <div className="flex flex-col items-end w-full md:w-auto">
          <div className="text-right">
            <span className="text-xs text-[#a3a096] font-mono">Fused Confidence</span>
            <p className="text-3xl font-mono font-bold text-[#e6e4df]">
              {(results.fusion_confidence * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
