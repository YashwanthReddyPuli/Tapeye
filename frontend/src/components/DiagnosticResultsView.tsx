"use client";

import React from "react";
import { CheckCircle2, AlertCircle, XCircle, RotateCcw } from "lucide-react";
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";

interface BranchProbs {
  Good?: number;
  Borderline?: number;
  Bad?: number;
  good?: number;
  borderline?: number;
  bad?: number;
}

interface DiagnosticResultsViewProps {
  results: any;
  onReset: () => void;
}

const CustomRadarTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-2xl border border-white/10 bg-black/80 p-4 shadow-2xl backdrop-blur-xl">
        <p className="mb-2 text-xs font-semibold tracking-wider text-[#b7b5a9] uppercase">
          {label} Class
        </p>
        <div className="space-y-1.5">
          {payload.map((entry: any, index: number) => (
            <div key={index} className="flex items-center justify-between gap-4 text-xs">
              <span className="flex items-center gap-2 text-[#e5e5e2]">
                <span
                  className="h-2 w-2 rounded-full"
                  style={{ backgroundColor: entry.color }}
                />
                {entry.name}
              </span>
              <span className="font-mono font-semibold text-[#faf9f5]">
                {entry.value}%
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

export default function DiagnosticResultsView({
  results,
  onReset,
}: DiagnosticResultsViewProps) {
  const getProb = (probs: BranchProbs, key: string) => {
    if (!probs) return 0;
    const lk = key.toLowerCase();
    const uk = key.charAt(0).toUpperCase() + key.slice(1);
    return probs[lk as keyof BranchProbs] ?? probs[uk as keyof BranchProbs] ?? 0;
  };

  const getTop = (probs: BranchProbs) => {
    let top = "Good";
    let max = -1;
    ["Good", "Borderline", "Bad"].forEach((cat) => {
      const v = getProb(probs, cat);
      if (v > max) {
        max = v;
        top = cat;
      }
    });
    return { label: top, confidence: max > 0 ? max : 0 };
  };

  const acousticTop = results.acoustic_branch?.label
    ? { label: results.acoustic_branch.label, confidence: results.acoustic_branch.confidence ?? 0.88 }
    : getTop(results.acoustic_probs || results.acoustic_branch?.probabilities);

  const visualTop = results.visual_branch?.label
    ? { label: results.visual_branch.label, confidence: results.visual_branch.confidence ?? 0.85 }
    : getTop(results.visual_probs || results.visual_branch?.probabilities);

  const verdict = results.final_verdict || results.verdict || "Good";
  const confidence = results.fusion_confidence || 0.85;

  const getVerdictStyle = (v: string) => {
    switch (v.toLowerCase()) {
      case "good":
        return {
          badge: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40",
          cardBg: "bg-emerald-950/30 border-emerald-500/30 backdrop-blur-xl shadow-lg",
          text: "text-emerald-400",
          icon: <CheckCircle2 size={32} className="text-emerald-400" />,
        };
      case "borderline":
        return {
          badge: "bg-amber-500/20 text-amber-300 border border-amber-500/40",
          cardBg: "bg-amber-950/30 border-amber-500/30 backdrop-blur-xl shadow-lg",
          text: "text-amber-400",
          icon: <AlertCircle size={32} className="text-amber-400" />,
        };
      case "bad":
      case "reject":
      default:
        return {
          badge: "bg-rose-500/20 text-rose-300 border border-rose-500/40",
          cardBg: "bg-rose-950/30 border-rose-500/30 backdrop-blur-xl shadow-lg",
          text: "text-rose-400",
          icon: <XCircle size={32} className="text-rose-400" />,
        };
    }
  };

  const vStyle = getVerdictStyle(verdict);

  const categories = ["Good", "Borderline", "Bad"];
  const chartData = results.chart_data
    ? results.chart_data.map((item: any) => ({
        classLabel: item.subject || item.classLabel || item.name,
        Acoustic: item.Acoustic ?? item.acoustic ?? 0,
        Visual: item.Visual ?? item.visual ?? 0,
        Fused: item.Fused ?? item.fused ?? 0,
      }))
    : categories.map((cat) => {
        let fProb = 0.1;
        if (verdict.toLowerCase() === cat.toLowerCase()) {
          fProb = confidence;
        } else {
          fProb = (1 - confidence) / 2;
        }
        return {
          classLabel: cat,
          Acoustic: Number((getProb(results.acoustic_probs, cat) * 100).toFixed(1)),
          Visual: Number((getProb(results.visual_probs, cat) * 100).toFixed(1)),
          Fused: Number((fProb * 100).toFixed(1)),
        };
      });


  return (
    <div className="space-y-5 flex flex-col h-full justify-between text-[#faf9f5]">
      {/* 1. TOP: FUSED VERDICT BANNER */}
      <div
        className={`p-6 rounded-2xl border ${vStyle.cardBg} flex flex-col sm:flex-row items-center justify-between gap-4`}
      >
        <div className="flex items-center gap-4">
          {vStyle.icon}
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-[#b7b5a9]">
                Final Decision
              </span>
              <span className={`text-[10px] font-mono px-2.5 py-0.5 rounded-full ${vStyle.badge} font-bold`}>
                VERDICT
              </span>
            </div>
            <h3 className={`text-3xl font-extrabold tracking-tight capitalize mt-0.5 ${vStyle.text}`}>
              {verdict} Quality
            </h3>
          </div>
        </div>

        <div className="text-right sm:border-l sm:border-white/10 sm:pl-6">
          <span className="text-[11px] font-bold uppercase tracking-wider text-[#b7b5a9] block">
            Confidence
          </span>
          <span className="text-3xl font-mono font-extrabold text-[#f97316]">
            {(confidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* 2. MIDDLE: TWO UNIMODAL BREAKDOWN SUB-CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* ACOUSTIC SUB-CARD */}
        <div className="p-5 rounded-2xl bg-black/20 backdrop-blur-xl border border-white/10 shadow-sm space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-[#faf9f5]">Acoustic Branch</span>
            <span className="text-[10px] font-mono font-semibold text-[#f97316] bg-orange-500/10 px-2 py-0.5 rounded-full border border-orange-500/20">
              SVM (MFCC)
            </span>
          </div>

          <div className="flex items-baseline justify-between">
            <div>
              <p className="text-xl font-bold text-[#faf9f5] capitalize">{acousticTop.label}</p>
              <p className="text-[11px] text-[#b7b5a9]">Internal Resonance</p>
            </div>
            <span className="text-sm font-mono font-extrabold text-[#f97316]">
              {(acousticTop.confidence * 100).toFixed(1)}%
            </span>
          </div>

          <div className="w-full bg-black/40 h-2 rounded-full overflow-hidden">
            <div
              className="bg-gradient-to-r from-orange-500 to-[#b05730] h-full rounded-full transition-all duration-500 shadow-sm"
              style={{ width: `${acousticTop.confidence * 100}%` }}
            />
          </div>
        </div>

        {/* VISUAL SUB-CARD */}
        <div className="p-5 rounded-2xl bg-black/20 backdrop-blur-xl border border-white/10 shadow-sm space-y-3">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-[#faf9f5]">Visual Branch</span>
            <span className="text-[10px] font-mono font-semibold text-[#9c87f5] bg-[#9c87f5]/15 px-2 py-0.5 rounded-full border border-[#9c87f5]/30">
              MobileNetV2
            </span>
          </div>

          <div className="flex items-baseline justify-between">
            <div>
              <p className="text-xl font-bold text-[#faf9f5] capitalize">{visualTop.label}</p>
              <p className="text-[11px] text-[#b7b5a9]">Surface Integrity</p>
            </div>
            <span className="text-sm font-mono font-extrabold text-[#9c87f5]">
              {(visualTop.confidence * 100).toFixed(1)}%
            </span>
          </div>

          <div className="w-full bg-black/40 h-2 rounded-full overflow-hidden">
            <div
              className="bg-gradient-to-r from-[#9c87f5] to-purple-600 h-full rounded-full transition-all duration-500"
              style={{ width: `${visualTop.confidence * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* 3. BOTTOM: RECHARTS PROBABILITY RADAR CHART */}
      <div className="p-5 rounded-2xl bg-black/20 backdrop-blur-xl border border-white/10 shadow-sm space-y-3">
        <div className="flex items-center justify-between text-xs">
          <span className="font-bold text-[#faf9f5]">Modal Probability Distribution</span>
          <span className="text-[10px] font-mono text-[#b7b5a9]">Classes: Good, Borderline, Bad</span>
        </div>

        <div className="w-full h-56">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
              <PolarGrid stroke="rgba(255, 255, 255, 0.08)" />
              <PolarAngleAxis
                dataKey="classLabel"
                stroke="#b7b5a9"
                tick={{ fill: "#faf9f5", fontSize: 12, fontWeight: 500 }}
              />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="rgba(255, 255, 255, 0.08)" tick={false} />
              
              <Radar
                name="Acoustic"
                dataKey="Acoustic"
                stroke="#f97316"
                strokeWidth={2}
                fill="#f97316"
                fillOpacity={0.25}
              />
              <Radar
                name="Visual"
                dataKey="Visual"
                stroke="#9c87f5"
                strokeWidth={2}
                fill="#9c87f5"
                fillOpacity={0.25}
              />
              <Radar
                name="Fused"
                dataKey="Fused"
                stroke="#b05730"
                strokeWidth={2}
                fill="#b05730"
                fillOpacity={0.35}
              />
              
              <Tooltip
                content={<CustomRadarTooltip />}
                cursor={{ fill: "rgba(255, 255, 255, 0.03)", radius: 6 }}
              />
              <Legend
                wrapperStyle={{ paddingTop: "6px" }}
                formatter={(value) => (
                  <span className="text-xs font-semibold text-[#faf9f5]">{value}</span>
                )}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* RESET ACTION */}
      <div className="flex justify-end pt-1">
        <button
          onClick={onReset}
          className="px-4 py-2.5 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 text-[#faf9f5] text-xs font-bold font-mono flex items-center gap-2 transition cursor-pointer shadow-sm"
        >
          <RotateCcw size={14} /> Scan Another Item
        </button>
      </div>
    </div>
  );
}
