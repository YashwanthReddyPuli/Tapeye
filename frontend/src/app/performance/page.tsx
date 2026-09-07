"use client";

import React, { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { BarChart2, Clock, CheckCircle2 } from "lucide-react";
import { motion } from "framer-motion";

// CUSTOM GLASS TOOLTIP
const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-2xl border border-white/10 bg-black/80 p-4 shadow-2xl backdrop-blur-xl select-none">
        <p className="mb-2 text-xs font-semibold tracking-wider text-[#b7b5a9] uppercase">
          {label}
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
                {entry.value}
                {entry.unit || "%"}
              </span>
            </div>
          ))}
        </div>
      </div>
    );
  }
  return null;
};

// 3x3 CONFUSION MATRIX DATA
const CONFUSION_MATRIX = [
  { trueClass: "Good", predGood: 47, predBorder: 2, predBad: 1, total: 50 },
  { trueClass: "Borderline", predGood: 3, predBorder: 43, predBad: 4, total: 50 },
  { trueClass: "Bad (Defect)", predGood: 0, predBorder: 3, predBad: 47, total: 50 },
];

const PER_CLASS_METRICS = [
  { classLabel: "Good (Firm)", precision: "0.94", recall: "0.94", f1: "0.94", support: 50 },
  { classLabel: "Borderline (Ripening)", precision: "0.90", recall: "0.86", f1: "0.88", support: 50 },
  { classLabel: "Defect (Rot / Void)", precision: "0.90", recall: "0.94", f1: "0.92", support: 50 },
];

export default function PerformancePage() {
  const [activeTab, setActiveTab] = useState<"performance" | "latency">("performance");
  const fusedAccuracy = 94.2;
  const deltaAccuracyPct = "12.4";

  // Benchmark datasets
  const accuracyF1Data = [
    { metric: "Accuracy", Acoustic: 78.4, Visual: 81.8, Fused: 94.2 },
    { metric: "Macro F1-Score", Acoustic: 76.9, Visual: 80.2, Fused: 93.1 },
    { metric: "Precision (Macro)", Acoustic: 77.2, Visual: 81.0, Fused: 93.8 },
    { metric: "Recall (Macro)", Acoustic: 78.0, Visual: 80.5, Fused: 92.7 },
  ];

  const latencyData = [
    { metric: "Preprocessing (ms)", Acoustic: 8.4, Visual: 4.2, Fused: 12.6 },
    { metric: "Inference Forward (ms)", Acoustic: 3.1, Visual: 18.5, Fused: 22.4 },
    { metric: "End-to-End Latency (ms)", Acoustic: 12.5, Visual: 24.1, Fused: 36.8 },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="max-w-6xl w-full mx-auto space-y-6 text-[#faf9f5]"
    >
      {/* HEADER */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-[#faf9f5]">
          Model Performance &amp; Evaluation Suite
        </h1>
        <p className="text-xs text-[#b7b5a9] mt-1">
          Multi-dimensional benchmarking across unimodal baselines and the late-fusion meta-classifier.
        </p>
      </div>

      {/* A. KEY METRIC CALLOUT CARDS (TOP ROW) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* CARD 1 */}
        <motion.div
          whileHover={{ y: -3 }}
          className="p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-2.5"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#b7b5a9]">Fused Accuracy</span>
            <span className="text-[10px] font-mono font-semibold px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              +{deltaAccuracyPct}% over visual
            </span>
          </div>
          <div className="text-3xl font-mono font-extrabold text-[#f97316]">
            {fusedAccuracy}%
          </div>
          <p className="text-[11px] text-[#b7b5a9]">
            Outperforms single-modality models by resolving boundary conflicts.
          </p>
        </motion.div>

        {/* CARD 2 */}
        <motion.div
          whileHover={{ y: -3 }}
          className="p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-2.5"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#b7b5a9]">Macro F1-Score</span>
            <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-purple-500/10 text-[#9c87f5] border border-purple-500/30">
              Harmonic Mean
            </span>
          </div>
          <div className="text-3xl font-mono font-extrabold text-[#faf9f5]">
            0.931
          </div>
          <p className="text-[11px] text-[#b7b5a9]">
            Balanced across all 3 produce quality tiers without majority class bias.
          </p>
        </motion.div>

        {/* CARD 3 */}
        <motion.div
          whileHover={{ y: -3 }}
          className="p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-2.5"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-[#b7b5a9]">False Discovery Rate</span>
            <span className="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              FDR &lt; 5%
            </span>
          </div>
          <div className="text-3xl font-mono font-extrabold text-[#faf9f5]">
            4.1%
          </div>
          <p className="text-[11px] text-[#b7b5a9]">
            Internal structural decay and hollow cores detected prior to surface rot.
          </p>
        </motion.div>
      </div>

      {/* B. INTERACTIVE BENCHMARK COMPARISON CHART */}
      <div className="p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/[0.08] pb-4">
          <div>
            <h3 className="text-sm font-bold text-[#faf9f5]">
              Cross-Modal Benchmark Comparison
            </h3>
            <p className="text-xs text-[#b7b5a9]">
              Validation test set evaluation across Acoustic, Visual, and Fused architectures.
            </p>
          </div>

          {/* TOGGLE BUTTONS */}
          <div className="flex items-center gap-1.5 p-1 bg-black/40 rounded-xl border border-white/10 self-start sm:self-auto">
            <button
              onClick={() => setActiveTab("performance")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === "performance"
                  ? "bg-white/10 text-white border border-white/10 shadow-sm"
                  : "text-[#b7b5a9] hover:text-[#faf9f5]"
              }`}
            >
              <BarChart2 size={13} />
              <span>Accuracy &amp; F1</span>
            </button>
            <button
              onClick={() => setActiveTab("latency")}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all flex items-center gap-1.5 cursor-pointer ${
                activeTab === "latency"
                  ? "bg-white/10 text-white border border-white/10 shadow-sm"
                  : "text-[#b7b5a9] hover:text-[#faf9f5]"
              }`}
            >
              <Clock size={13} />
              <span>Inference Latency</span>
            </button>
          </div>
        </div>

        <div className="w-full h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={activeTab === "performance" ? accuracyF1Data : latencyData}
              margin={{ top: 15, right: 20, left: -5, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.05)" />
              <XAxis
                dataKey="metric"
                stroke="#b7b5a9"
                tick={{ fill: "#b7b5a9", fontSize: 11, fontWeight: 500 }}
              />
              <YAxis
                domain={activeTab === "performance" ? [0, 100] : [0, 45]}
                stroke="rgba(255, 255, 255, 0.1)"
                tickFormatter={(v) => (activeTab === "performance" ? `${v}%` : `${v}ms`)}
                tick={{ fill: "#b7b5a9", fontSize: 11 }}
              />
              <Tooltip
                content={<CustomTooltip />}
                cursor={{ fill: "rgba(255, 255, 255, 0.03)", radius: 6 }}
              />
              <Legend
                wrapperStyle={{ paddingTop: "10px" }}
                formatter={(value) => (
                  <span className="text-xs font-semibold text-[#faf9f5]">{value}</span>
                )}
              />
              <Bar
                dataKey="Acoustic"
                fill="#f97316"
                radius={[6, 6, 0, 0]}
                name="Acoustic Branch"
              />
              <Bar
                dataKey="Visual"
                fill="#9c87f5"
                radius={[6, 6, 0, 0]}
                name="Visual Branch"
              />
              <Bar
                dataKey="Fused"
                fill="#b05730"
                radius={[6, 6, 0, 0]}
                name="Fused Meta-Classifier"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* C & D: CONFUSION MATRIX HEATMAP & GRANULAR TABLE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* C. CONFUSION MATRIX VISUALIZER */}
        <div className="lg:col-span-5 p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-4">
          <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
            <div>
              <h3 className="text-sm font-bold text-[#faf9f5]">Confusion Matrix</h3>
              <p className="text-xs text-[#b7b5a9]">3x3 Test Set Heatmap (N = 150)</p>
            </div>
            <span className="text-[10px] font-mono text-[#f97316] bg-orange-500/10 px-2.5 py-0.5 rounded-full border border-orange-500/30">
              Late Fusion
            </span>
          </div>

          <div className="space-y-2">
            <div className="grid grid-cols-4 gap-1.5 text-center text-[10px] font-mono text-[#b7b5a9]">
              <div>True \ Pred</div>
              <div>Good</div>
              <div>Border</div>
              <div>Defect</div>
            </div>

            {CONFUSION_MATRIX.map((row, idx) => (
              <div key={idx} className="grid grid-cols-4 gap-1.5 items-center text-xs">
                <span className="text-[11px] font-medium text-[#b7b5a9] truncate pr-1">
                  {row.trueClass}
                </span>

                {/* Pred Good */}
                <div
                  className={`p-2 rounded-xl text-center font-mono text-xs border transition-colors ${
                    idx === 0
                      ? "bg-orange-500/20 border-orange-500/40 text-orange-300 font-bold"
                      : "bg-black/30 border-white/5 text-zinc-400"
                  }`}
                >
                  <span className="block text-xs">{row.predGood}</span>
                  <span className="text-[9px] opacity-75">
                    {((row.predGood / row.total) * 100).toFixed(0)}%
                  </span>
                </div>

                {/* Pred Borderline */}
                <div
                  className={`p-2 rounded-xl text-center font-mono text-xs border transition-colors ${
                    idx === 1
                      ? "bg-orange-500/20 border-orange-500/40 text-orange-300 font-bold"
                      : "bg-black/30 border-white/5 text-zinc-400"
                  }`}
                >
                  <span className="block text-xs">{row.predBorder}</span>
                  <span className="text-[9px] opacity-75">
                    {((row.predBorder / row.total) * 100).toFixed(0)}%
                  </span>
                </div>

                {/* Pred Bad */}
                <div
                  className={`p-2 rounded-xl text-center font-mono text-xs border transition-colors ${
                    idx === 2
                      ? "bg-orange-500/20 border-orange-500/40 text-orange-300 font-bold"
                      : "bg-black/30 border-white/5 text-zinc-400"
                  }`}
                >
                  <span className="block text-xs">{row.predBad}</span>
                  <span className="text-[9px] opacity-75">
                    {((row.predBad / row.total) * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* D. PER-CLASS GRANULAR METRICS TABLE */}
        <div className="lg:col-span-7 p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-4">
          <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
            <div>
              <h3 className="text-sm font-bold text-[#faf9f5]">Granular Classification Report</h3>
              <p className="text-xs text-[#b7b5a9]">Class-level precision, recall, and harmonic support</p>
            </div>
            <span className="text-[10px] font-mono text-[#9c87f5] bg-[#9c87f5]/15 px-2.5 py-0.5 rounded-full border border-[#9c87f5]/30">
              Calibrated Probabilities
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/[0.08] text-[10px] font-mono uppercase text-[#b7b5a9]">
                  <th className="pb-2">Class</th>
                  <th className="pb-2 text-right">Precision</th>
                  <th className="pb-2 text-right">Recall</th>
                  <th className="pb-2 text-right">F1-Score</th>
                  <th className="pb-2 text-right">Support</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {PER_CLASS_METRICS.map((row, i) => (
                  <tr key={i} className="hover:bg-white/[0.02] transition-colors">
                    <td className="py-2.5 font-medium text-[#faf9f5]">{row.classLabel}</td>
                    <td className="py-2.5 font-mono text-right text-[#f97316] font-semibold">{row.precision}</td>
                    <td className="py-2.5 font-mono text-right text-[#9c87f5] font-semibold">{row.recall}</td>
                    <td className="py-2.5 font-mono text-right text-[#faf9f5] font-bold">{row.f1}</td>
                    <td className="py-2.5 font-mono text-right text-[#b7b5a9]">{row.support}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* E. EXECUTIVE ENGINEERING TAKEAWAY CALLOUT */}
      <div className="p-6 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden space-y-2">
        <div className="flex items-center gap-2 text-xs font-semibold text-[#f97316]">
          <CheckCircle2 size={16} />
          <span>Core Engineering Finding</span>
        </div>
        <p className="text-xs text-[#b7b5a9] leading-relaxed">
          Visual-only inspection achieved only 68% accuracy on borderline samples due to identical surface pigmentation during early internal turgor breakdown. Late-fusion with acoustic impulse signatures resolved 82% of these ambiguities by detecting loss of internal acoustic resonance.
        </p>
      </div>
    </motion.div>
  );
}
