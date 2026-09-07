"use client";

import React from "react";
import {
  Mic,
  Camera,
  ArrowRight,
  Combine,
  Activity,
  Cpu,
  Layers,
  Zap,
} from "lucide-react";
import { motion } from "framer-motion";

export default function ArchitecturePage() {
  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    show: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: "easeOut",
        staggerChildren: 0.12,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: "easeOut" } },
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="show"
      className="max-w-5xl w-full mx-auto space-y-12 text-[#faf9f5] pb-16"
    >
      {/* 1. CENTERED ELEGANT HEADER */}
      <motion.div variants={itemVariants} className="text-center space-y-3 pt-2">
        <span className="inline-flex items-center gap-1.5 text-xs font-mono text-[#f97316] uppercase tracking-widest bg-orange-500/10 px-3 py-1 rounded-full border border-orange-500/20">
          <Zap size={13} /> Architecture Overview
        </span>
        <h1 className="text-4xl md:text-5xl font-serif font-normal tracking-tight text-[#faf9f5]">
          Dual-Modal Late Fusion Pipeline
        </h1>
        <p className="text-sm md:text-base font-sans text-[#b7b5a9] max-w-xl mx-auto leading-relaxed">
          Asynchronous processing of acoustic resonance and spatial features.
        </p>
      </motion.div>

      {/* 2. THE HERO PIPELINE VISUAL (MINIMALIST FLOW) */}
      <motion.div
        variants={itemVariants}
        className="p-8 md:p-10 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[28px] relative overflow-hidden"
      >
        <div className="flex flex-col md:flex-row items-center justify-between gap-6 md:gap-8 max-w-4xl mx-auto">
          {/* LEFT: 2 INPUT PILLS STACKED */}
          <div className="flex flex-col gap-4 w-full md:w-auto flex-1">
            {/* Pill 1: Acoustic */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="flex items-center gap-3.5 px-6 py-4 rounded-2xl bg-black/30 backdrop-blur-xl border border-white/10 shadow-lg"
            >
              <div className="h-10 w-10 rounded-xl bg-orange-500/15 border border-orange-500/30 flex items-center justify-center text-[#f97316] shrink-0">
                <Mic size={20} />
              </div>
              <div className="text-left">
                <div className="text-xs font-mono text-[#f97316] uppercase tracking-wider font-semibold">
                  Audio Branch
                </div>
                <div className="text-sm font-semibold text-[#faf9f5]">
                  Acoustic (MFCC)
                </div>
              </div>
            </motion.div>

            {/* Pill 2: Visual */}
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="flex items-center gap-3.5 px-6 py-4 rounded-2xl bg-black/30 backdrop-blur-xl border border-white/10 shadow-lg"
            >
              <div className="h-10 w-10 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-[#9c87f5] shrink-0">
                <Camera size={20} />
              </div>
              <div className="text-left">
                <div className="text-xs font-mono text-[#9c87f5] uppercase tracking-wider font-semibold">
                  Vision Branch
                </div>
                <div className="text-sm font-semibold text-[#faf9f5]">
                  Visual (MobileNetV2)
                </div>
              </div>
            </motion.div>
          </div>

          {/* CONNECTOR ARROW */}
          <div className="flex items-center justify-center text-[#f97316] p-2">
            <motion.div
              animate={{ x: [0, 4, 0] }}
              transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
            >
              <ArrowRight size={32} className="text-[#f97316]" />
            </motion.div>
          </div>

          {/* RIGHT: PILL 3 LATE-FUSION META-CLASSIFIER */}
          <div className="w-full md:w-auto flex-1">
            <motion.div
              whileHover={{ scale: 1.02 }}
              className="flex items-center gap-4 px-6 py-7 rounded-2xl bg-orange-500/10 backdrop-blur-xl border border-[#f97316]/50 shadow-[0_0_25px_rgba(249,115,22,0.15)]"
            >
              <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-orange-500 to-[#b05730] flex items-center justify-center text-white shrink-0 shadow-md">
                <Combine size={24} />
              </div>
              <div className="text-left">
                <div className="text-xs font-mono text-[#f97316] uppercase tracking-wider font-semibold">
                  Unified Decision
                </div>
                <div className="text-base font-bold text-[#faf9f5]">
                  Late-Fusion Meta-Classifier
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      {/* 3. THE BENTO FEATURE GRID (4 CLEAN CARDS) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* CARD 1: ACOUSTIC ENGINE */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4 }}
          transition={{ duration: 0.2 }}
          className="bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] p-8 space-y-4 relative overflow-hidden flex flex-col justify-between"
        >
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="h-10 w-10 rounded-xl bg-orange-500/15 border border-orange-500/30 flex items-center justify-center text-[#f97316]">
                <Activity size={20} />
              </div>
              <span className="text-xs font-mono text-[#f97316]">Acoustic Engine 🎵</span>
            </div>
            <h2 className="text-xl font-serif text-[#faf9f5]">
              DSP &amp; Frequency Analysis
            </h2>
            <p className="text-sm font-sans text-[#b7b5a9] leading-relaxed">
              Extracts 13 Mel-Frequency Cepstral Coefficients (MFCCs) via Librosa to detect internal tissue voids and turgor pressure loss.
            </p>
          </div>
        </motion.div>

        {/* CARD 2: VISION ENGINE */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4 }}
          transition={{ duration: 0.2 }}
          className="bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] p-8 space-y-4 relative overflow-hidden flex flex-col justify-between"
        >
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="h-10 w-10 rounded-xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-[#9c87f5]">
                <Cpu size={20} />
              </div>
              <span className="text-xs font-mono text-[#9c87f5]">Vision Engine 📷</span>
            </div>
            <h2 className="text-xl font-serif text-[#faf9f5]">
              Spatial Feature Extraction
            </h2>
            <p className="text-sm font-sans text-[#b7b5a9] leading-relaxed">
              Fine-tuned MobileNetV2 backbone analyzes 224x224 RGB inputs for external blemishes, bruising, and skin decay.
            </p>
          </div>
        </motion.div>

        {/* CARD 3: FUSION ARCHITECTURE */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4 }}
          transition={{ duration: 0.2 }}
          className="bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] p-8 space-y-4 relative overflow-hidden flex flex-col justify-between"
        >
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="h-10 w-10 rounded-xl bg-orange-500/15 border border-orange-500/30 flex items-center justify-center text-[#f97316]">
                <Layers size={20} />
              </div>
              <span className="text-xs font-mono text-[#f97316]">Fusion Architecture 🧠</span>
            </div>
            <h2 className="text-xl font-serif text-[#faf9f5]">
              Decision-Level Late Fusion
            </h2>
            <p className="text-sm font-sans text-[#b7b5a9] leading-relaxed">
              Concatenates unimodal probability distributions into a unified 6D tensor, utilizing a Meta-Classifier to resolve sensory conflicts.
            </p>
          </div>
        </motion.div>

        {/* CARD 4: TECH STACK */}
        <motion.div
          variants={itemVariants}
          whileHover={{ y: -4 }}
          transition={{ duration: 0.2 }}
          className="bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] p-8 space-y-4 relative overflow-hidden flex flex-col justify-between"
        >
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <div className="h-10 w-10 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
                <Zap size={20} />
              </div>
              <span className="text-xs font-mono text-emerald-400">Tech Stack ⚡</span>
            </div>
            <h2 className="text-xl font-serif text-[#faf9f5]">
              Edge-to-Cloud Deployment
            </h2>
            <p className="text-sm font-sans text-[#b7b5a9] leading-relaxed">
              FastAPI inference engine, React/Next.js frontend, and Framer Motion UI. Built for sub-100ms classification latency.
            </p>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}
