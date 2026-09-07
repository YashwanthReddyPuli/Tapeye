"use client";

import React, { useState } from "react";
import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import HolographicBeams from "@/components/ui/beams-background";
import UploadZone from "@/components/UploadZone";
import ResultsDashboard from "@/components/ResultsDashboard";
import ProbabilityRadarChart from "@/components/ProbabilityRadarChart";
import { LayoutDashboard, BarChart2, Info, Eye, Sparkles, Loader2, RefreshCw } from "lucide-react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";

const sidebarLinks = [
  {
    label: "Scanner Dashboard",
    href: "/",
    icon: <LayoutDashboard className="text-primary h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Model Performance",
    href: "/performance",
    icon: <BarChart2 className="text-neutral-400 h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "System Architecture",
    href: "/about",
    icon: <Info className="text-neutral-400 h-5 w-5 flex-shrink-0" />,
  },
];

const SCAN_STEPS = [
  "Extracting MFCCs & Spectrograms...",
  "Running MobileNetV2 Vision Inference...",
  "Fusing Tensors & Meta-Classification...",
];

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // File states
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [audioPreviewUrl, setAudioPreviewUrl] = useState<string | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);

  // Inference state
  const [isScanning, setIsScanning] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [results, setResults] = useState<any | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleAudioChange = (file: File | null) => {
    setAudioFile(file);
    if (file) {
      setAudioPreviewUrl(URL.createObjectURL(file));
    } else {
      setAudioPreviewUrl(null);
    }
  };

  const handleImageChange = (file: File | null) => {
    setImageFile(file);
    if (file) {
      setImagePreviewUrl(URL.createObjectURL(file));
    } else {
      setImagePreviewUrl(null);
    }
  };

  const runScan = async () => {
    if (!audioFile || !imageFile) {
      setErrorMsg("Please upload both an Acoustic audio file (.wav) and a Visual image file (.jpg/.png).");
      return;
    }

    setErrorMsg(null);
    setIsScanning(true);
    setCurrentStepIndex(0);
    setResults(null);

    // Simulated stepped progress sequence for UI "Wow" factor
    const stepInterval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev < SCAN_STEPS.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 900);

    try {
      const formData = new FormData();
      formData.append("audio", audioFile);
      formData.append("image", imageFile);

      const response = await fetch("http://localhost:8000/api/scan", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Inference API error: ${response.statusText}`);
      }

      const data = await response.json();
      
      // Ensure smooth completion of animation steps
      setTimeout(() => {
        clearInterval(stepInterval);
        setResults(data);
        setIsScanning(false);
      }, 2700);

    } catch (err: any) {
      clearInterval(stepInterval);
      setIsScanning(false);
      setErrorMsg(err.message || "Failed to communicate with FastAPI backend server.");
    }
  };

  const resetScan = () => {
    setAudioFile(null);
    setImageFile(null);
    setAudioPreviewUrl(null);
    setImagePreviewUrl(null);
    setResults(null);
    setErrorMsg(null);
  };

  return (
    <div className="flex h-screen w-full bg-background overflow-hidden relative">
      {/* BACKGROUND HOLOGRAPHIC LIGHT BEAMS */}
      <HolographicBeams density={20} speed={1.2} aberration={2.5} opacity={40} />

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

      {/* MAIN DASHBOARD CONTENT AREA */}
      <div className="flex-1 h-full overflow-y-auto z-30 p-6 md:p-12 relative flex flex-col items-center">
        <div className="w-full max-w-4xl space-y-8 my-auto">
          {/* HEADER */}
          <div className="text-center space-y-2">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-neutral-900/90 border border-neutral-800 backdrop-blur-md">
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-xs font-semibold text-neutral-300 tracking-wide uppercase">
                Dual-Modal Produce Scanner
              </span>
            </div>
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white">
              TapEye <span className="text-primary font-mono">Late-Fusion</span>
            </h1>
            <p className="text-sm md:text-base text-neutral-400 max-w-xl mx-auto">
              Non-destructive internal quality assessment combining acoustic resonance spectrums with deep surface vision.
            </p>
          </div>

          {/* ERROR ALERT */}
          {errorMsg && (
            <div className="p-4 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-300 text-sm text-center backdrop-blur-md">
              {errorMsg}
            </div>
          )}

          {/* INPUT/SCANNER CONTROLLER AREA */}
          {!results && !isScanning && (
            <div className="flex flex-col items-center gap-8">
              <UploadZone
                audioFile={audioFile}
                imageFile={imageFile}
                onAudioChange={handleAudioChange}
                onImageChange={handleImageChange}
                audioPreviewUrl={audioPreviewUrl}
                imagePreviewUrl={imagePreviewUrl}
              />

              <button
                onClick={runScan}
                disabled={!audioFile || !imageFile}
                className={`px-8 py-4 rounded-2xl font-semibold text-base flex items-center gap-3 transition-all duration-300 shadow-lg ${
                  audioFile && imageFile
                    ? "bg-primary hover:bg-primary/90 text-white shadow-[0_0_25px_rgba(217,119,87,0.4)] cursor-pointer hover:scale-105"
                    : "bg-neutral-800 text-neutral-500 cursor-not-allowed border border-neutral-700/50"
                }`}
              >
                <Sparkles className="w-5 h-5" /> Run Dual-Modal Scan
              </button>
            </div>
          )}

          {/* STEPPED LOADING SEQUENCE ANIMATION */}
          <AnimatePresence>
            {isScanning && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="w-full max-w-xl mx-auto p-8 rounded-2xl bg-neutral-900/90 border border-neutral-800 backdrop-blur-xl flex flex-col items-center text-center space-y-6 shadow-2xl"
              >
                <div className="relative flex items-center justify-center">
                  <div className="w-20 h-20 rounded-full border-4 border-primary/20 border-t-primary animate-spin" />
                  <Loader2 className="w-8 h-8 text-primary absolute animate-pulse" />
                </div>

                <div className="space-y-2">
                  <h3 className="text-xl font-bold text-white tracking-tight">
                    {SCAN_STEPS[currentStepIndex]}
                  </h3>
                  <p className="text-xs text-neutral-400 font-mono">
                    Step {currentStepIndex + 1} of {SCAN_STEPS.length}
                  </p>
                </div>

                {/* Progress bar */}
                <div className="w-full bg-neutral-800 h-2 rounded-full overflow-hidden border border-neutral-700/50">
                  <motion.div
                    className="bg-primary h-full rounded-full"
                    initial={{ width: "0%" }}
                    animate={{ width: `${((currentStepIndex + 1) / SCAN_STEPS.length) * 100}%` }}
                    transition={{ duration: 0.5 }}
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* RESULTS DISPLAY DASHBOARD */}
          {results && !isScanning && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex flex-col items-center gap-8"
            >
              <ResultsDashboard results={results} />
              
              <ProbabilityRadarChart
                acousticProbs={results.acoustic_probs}
                visualProbs={results.visual_probs}
                fusedVerdict={results.verdict}
                fusedConfidence={results.fusion_confidence}
              />

              <button
                onClick={resetScan}
                className="px-6 py-3 rounded-xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 text-neutral-300 font-medium text-sm flex items-center gap-2 transition hover:bg-neutral-800/80 cursor-pointer"
              >
                <RefreshCw className="w-4 h-4" /> Scan Another Sample
              </button>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
}
