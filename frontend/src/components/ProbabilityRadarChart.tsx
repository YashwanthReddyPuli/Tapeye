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
  Good: number;
  Borderline: number;
  Bad: number;
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
  // Construct fused probabilities dictionary for side-by-side radar view
  const categories = ["Good", "Borderline", "Bad"];
  
  const chartData = categories.map((cat) => {
    // Estimate fused curve representation
    let fusedProb = 0.1;
    if (fusedVerdict === cat) {
      fusedProb = fusedConfidence;
    } else {
      fusedProb = (1 - fusedConfidence) / 2;
    }

    return {
      classLabel: cat,
      Acoustic: Number((acousticProbs[cat as keyof BranchProbs] * 100).toFixed(1)),
      Visual: Number((visualProbs[cat as keyof BranchProbs] * 100).toFixed(1)),
      Fused: Number((fusedProb * 100).toFixed(1)),
    };
  });

  return (
    <div className="w-full max-w-4xl p-6 rounded-2xl bg-neutral-900/80 border border-neutral-800 backdrop-blur-md">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-2">
        <div>
          <h4 className="text-lg font-bold text-white tracking-tight">
            Probability Distribution Comparison
          </h4>
          <p className="text-xs text-neutral-400">
            Side-by-side modal & fused probability vectors across produce quality classes
          </p>
        </div>
        <span className="text-xs px-3 py-1 rounded-full bg-neutral-800 text-neutral-300 border border-neutral-700 font-mono self-start md:self-auto">
          Shared Polar Axis (0-100%)
        </span>
      </div>

      <div className="w-full h-80">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
            <PolarGrid stroke="#3e3e38" />
            <PolarAngleAxis dataKey="classLabel" stroke="#c3c0b6" tick={{ fill: "#c3c0b6", fontSize: 13 }} />
            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#52514a" />
            
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
              stroke="#9c87f5"
              fill="#9c87f5"
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
                backgroundColor: "#1f1e1d",
                borderColor: "#3e3e38",
                borderRadius: "0.5rem",
                color: "#c3c0b6",
              }}
              formatter={(value: number) => [`${value}%`]}
            />
            <Legend
              wrapperStyle={{ paddingTop: "10px" }}
              formatter={(value) => <span className="text-xs font-medium text-neutral-300">{value}</span>}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
