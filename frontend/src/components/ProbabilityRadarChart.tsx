"use client";

import React from "react";
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

interface ProbabilityRadarChartProps {
  acousticProbs: BranchProbs;
  visualProbs: BranchProbs;
  fusedVerdict: string;
  fusedConfidence: number;
}

export default function ProbabilityRadarChart({
  acousticProbs,
  visualProbs,
  fusedVerdict,
  fusedConfidence,
}: ProbabilityRadarChartProps) {
  const getProb = (probs: BranchProbs, key: string) => {
    if (!probs) return 0;
    const lowerKey = key.toLowerCase();
    const upperKey = key.charAt(0).toUpperCase() + key.slice(1);
    return probs[lowerKey as keyof BranchProbs] ?? probs[upperKey as keyof BranchProbs] ?? 0;
  };

  const categories = ["Good", "Borderline", "Bad"];
  
  const chartData = categories.map((cat) => {
    let fusedProb = 0.1;
    if (fusedVerdict.toLowerCase() === cat.toLowerCase()) {
      fusedProb = fusedConfidence;
    } else {
      fusedProb = (1 - fusedConfidence) / 2;
    }

    return {
      classLabel: cat,
      Acoustic: Number((getProb(acousticProbs, cat) * 100).toFixed(1)),
      Visual: Number((getProb(visualProbs, cat) * 100).toFixed(1)),
      Fused: Number((fusedProb * 100).toFixed(1)),
    };
  });

  return (
    <div className="w-full max-w-4xl p-6 rounded-2xl bg-[#24231f] border border-[#383630] shadow-md">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-2">
        <div>
          <h4 className="text-lg font-bold text-[#e6e4df] tracking-tight">
            Probability Distribution Comparison
          </h4>
          <p className="text-xs text-[#a3a096]">
            Side-by-side modal & fused probability vectors across produce quality classes
          </p>
        </div>
        <span className="text-xs px-3 py-1 rounded-full bg-[#1b1a17] text-[#a3a096] border border-[#383630] font-mono self-start md:self-auto">
          Shared Polar Axis (0-100%)
        </span>
      </div>

      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
            <PolarGrid stroke="#383630" />
            <PolarAngleAxis dataKey="classLabel" stroke="#a3a096" tick={{ fill: "#a3a096", fontSize: 13 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#383630" />
            
            <Radar
              name="Acoustic Branch"
              dataKey="Acoustic"
              stroke="#d97757"
              fill="#d97757"
              fillOpacity={0.3}
            />
            <Radar
              name="Visual Branch"
              dataKey="Visual"
              stroke="#8b5cf6"
              fill="#8b5cf6"
              fillOpacity={0.3}
            />
            <Radar
              name="Fused Meta-Classifier"
              dataKey="Fused"
              stroke="#10b981"
              fill="#10b981"
              fillOpacity={0.4}
            />
            
            <Tooltip
              contentStyle={{
                backgroundColor: "#161513",
                borderColor: "#383630",
                borderRadius: "0.5rem",
                color: "#e6e4df",
              }}
              formatter={(value: number) => [`${value}%`]}
            />
            <Legend
              wrapperStyle={{ paddingTop: "10px" }}
              formatter={(value) => <span className="text-xs font-medium text-[#e6e4df]">{value}</span>}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
