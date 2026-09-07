"use client";

import React, { useState } from "react";
import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import HolographicBeams from "@/components/ui/beams-background";
import { LayoutDashboard, BarChart2, Info, Eye, Cpu, Layers, ShieldCheck, Server, Globe } from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";

const sidebarLinks = [
  {
    label: "Scanner Dashboard",
    href: "/",
    icon: <LayoutDashboard className="text-neutral-400 h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Model Performance",
    href: "/performance",
    icon: <BarChart2 className="text-neutral-400 h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "System Architecture",
    href: "/about",
    icon: <Info className="text-primary h-5 w-5 flex-shrink-0" />,
  },
];

export default function AboutPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden relative">
      <HolographicBeams density={15} speed={0.8} aberration={1.8} opacity={30} />

      {/* SIDEBAR COMPONENT */}
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen}>
        <SidebarBody className="justify-between gap-10">
          <div className="flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
            <Link href="/" className="font-bold flex space-x-2 items-center text-sm py-2 relative z-20">
              <div className="h-6 w-6 bg-primary rounded-lg flex items-center justify-center text-white">
                <Eye className="w-4 h-4" />
              </div>
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="font-extrabold text-white text-base tracking-wider whitespace-pre"
              >
                TapEye OS
              </motion.span>
            </Link>
            <div className="mt-8 flex flex-col gap-2">
              {sidebarLinks.map((link, idx) => (
                <SidebarLink key={idx} link={link} />
              ))}
            </div>
          </div>
        </SidebarBody>
      </Sidebar>

      {/* CONTENT AREA */}
      <div className="flex-1 h-full overflow-y-auto z-30 p-6 md:p-12 relative flex flex-col items-center">
        <div className="w-full max-w-4xl space-y-8 my-auto">
          {/* HEADER */}
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-neutral-900/90 border border-neutral-800 backdrop-blur-md">
              <Cpu className="w-4 h-4 text-primary" />
              <span className="text-xs font-semibold text-neutral-300 tracking-wide uppercase">
                System Design & Late-Fusion Architecture
              </span>
            </div>
            <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-white">
              About TapEye Architecture
            </h1>
            <p className="text-sm text-neutral-400 max-w-2xl">
              Understanding dual-modal acoustic-visual fusion, software-in-the-loop validation, and decoupled full-stack implementation.
            </p>
          </div>

          {/* LATE FUSION RATIONALE CARD */}
          <div className="p-6 rounded-2xl bg-neutral-900/80 border border-neutral-800 backdrop-blur-md space-y-4">
            <div className="flex items-center gap-3">
              <Layers className="w-6 h-6 text-primary" />
              <h3 className="text-xl font-bold text-white">Why Late-Fusion Meta-Classification?</h3>
            </div>
            <p className="text-sm text-neutral-300 leading-relaxed">
              Traditional early-fusion methods concatenate raw audio spectrums and image pixels at input time, leading to high-dimensional feature explosion and vulnerability to modality-specific noise. TapEye employs <span className="text-primary font-semibold">Late Fusion</span>:
            </p>
            <ul className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-neutral-300 pt-2">
              <li className="p-4 rounded-xl bg-neutral-800/50 border border-neutral-700/50">
                <strong className="text-white block text-sm mb-1">Acoustic Branch (SVM)</strong>
                Processes physical resonance, density, and elasticity via 13 MFCC coefficients and raw FFT magnitudes to reveal internal hollows or rot.
              </li>
              <li className="p-4 rounded-xl bg-neutral-800/50 border border-neutral-700/50">
                <strong className="text-white block text-sm mb-1">Visual Branch (MobileNetV2)</strong>
                Fine-tuned Transfer Learning model evaluating surface blemishes, discoloration, skin integrity, and ripeness.
              </li>
            </ul>
          </div>

          {/* TECH STACK GRID */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 rounded-2xl bg-neutral-900/80 border border-neutral-800 backdrop-blur-md space-y-3">
              <Server className="w-6 h-6 text-emerald-400" />
              <h4 className="text-base font-bold text-white">FastAPI Backend</h4>
              <p className="text-xs text-neutral-400">
                High-performance async Python backend executing ML inference, temporary payload isolation, and metrics parsing.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-neutral-900/80 border border-neutral-800 backdrop-blur-md space-y-3">
              <Globe className="w-6 h-6 text-purple-400" />
              <h4 className="text-base font-bold text-white">Next.js Frontend</h4>
              <p className="text-xs text-neutral-400">
                Modern React App Router interface with animated drag-and-drop, stepped inference feedback, and Recharts visualization.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-neutral-900/80 border border-neutral-800 backdrop-blur-md space-y-3">
              <ShieldCheck className="w-6 h-6 text-primary" />
              <h4 className="text-base font-bold text-white">Core ML Suite</h4>
              <p className="text-xs text-neutral-400">
                Librosa for acoustic feature extraction, Scikit-Learn SVM, OpenCV, PyTorch MobileNetV2, and Logistic Regression meta-classifier.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
