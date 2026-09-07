"use client";

import React, { useState } from "react";
import SensorIntakePanel from "@/components/SensorIntakePanel";
import DiagnosticResultsView from "@/components/DiagnosticResultsView";
import { AlertCircle, Terminal } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const TRACE_LOGS = [
  "[INFO] Ingesting multipart/form-data payload...",
  "[INFO] Audio src: parsed 22050Hz .wav",
  "[DEBUG] Extracted 13 MFCC coefficients via Librosa",
  "[INFO] Image src: resampled to 224x224 RGB",
  "[DEBUG] MobileNetV2 spatial feature pooling complete",
  "[INFO] Tensors concatenated. Shape: (1, 6)",
  "[SUCCESS] Late-Fusion SVM inference complete. Yielding verdict.",
];

export default function Home() {
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [audioPreviewUrl, setAudioPreviewUrl] = useState<string | null>(null);
  const [imagePreviewUrl, setImagePreviewUrl] = useState<string | null>(null);

  const [isScanning, setIsScanning] = useState(false);
  const [visibleLogs, setVisibleLogs] = useState<string[]>([]);
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
    if (!audioFile || !imageFile) return;

    setErrorMsg(null);
    setIsScanning(true);
    setVisibleLogs([]);
    setResults(null);

    // Sequential trace logs
    let index = 0;
    const logInterval = setInterval(() => {
      if (index < TRACE_LOGS.length) {
        const nextLog = TRACE_LOGS[index];
        setVisibleLogs((prev) => [...prev, nextLog]);
        index++;
      }
    }, 320);

    try {
      const formData = new FormData();
      formData.append("audio", audioFile);
      formData.append("image", imageFile);

      const response = await fetch("http://127.0.0.1:8000/api/scan", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errDetail = await response.text();
        throw new Error(`Inference Error (${response.status}): ${errDetail || response.statusText}`);
      }

      const data = await response.json();

      clearInterval(logInterval);
      setVisibleLogs(TRACE_LOGS);
      setResults(data);
    } catch (err: any) {
      clearInterval(logInterval);
      setErrorMsg(err.message || "Failed to communicate with FastAPI backend.");
    } finally {
      setIsScanning(false);
    }
  };

  const resetScan = () => {
    setAudioFile(null);
    setImageFile(null);
    setAudioPreviewUrl(null);
    setImagePreviewUrl(null);
    setResults(null);
    setVisibleLogs([]);
    setErrorMsg(null);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="max-w-7xl w-full mx-auto space-y-6 text-[#faf9f5]"
    >
      {/* ERROR BANNER */}
      {errorMsg && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-4 rounded-[20px] bg-rose-950/30 backdrop-blur-[30px] border border-rose-500/30 text-rose-300 text-xs font-mono flex items-center gap-2.5 shadow-lg"
        >
          <AlertCircle size={16} className="text-rose-400 shrink-0" />
          <span>{errorMsg}</span>
        </motion.div>
      )}

      {/* 2-COLUMN SPLIT CONSOLE WITH HYPER-GLASSMORPHISM */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* LEFT COLUMN: SOURCE FILES (5 COLS) */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1, ease: "easeOut" }}
          className="lg:col-span-5 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden p-6 relative"
        >
          <SensorIntakePanel
            audioFile={audioFile}
            imageFile={imageFile}
            onAudioChange={handleAudioChange}
            onImageChange={handleImageChange}
            audioPreviewUrl={audioPreviewUrl}
            imagePreviewUrl={imagePreviewUrl}
            onExecute={runScan}
            isScanning={isScanning}
          />
        </motion.div>

        {/* RIGHT COLUMN: DIAGNOSTIC & RESULTS / LIVE EXECUTION TRACE (7 COLS) */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2, ease: "easeOut" }}
          className="lg:col-span-7 bg-white/[0.01] backdrop-blur-[40px] border border-white/[0.08] shadow-[0_8px_32px_0_rgba(0,0,0,0.5),inset_0_1px_1px_rgba(255,255,255,0.08)] rounded-[24px] overflow-hidden p-6 relative min-h-[520px] flex flex-col justify-between"
        >
          {/* STATE 1: SCANNING STATE (LIVE EXECUTION TRACE) */}
          <AnimatePresence mode="wait">
            {isScanning && (
              <motion.div
                key="scanning"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="space-y-4 my-auto"
              >
                <div className="flex items-center justify-between border-b border-white/[0.08] pb-3">
                  <div className="flex items-center gap-2 text-xs font-mono text-[#b7b5a9]">
                    <Terminal size={14} className="text-[#f97316]" />
                    <span>Live Execution Trace</span>
                  </div>
                  <span className="text-[10px] font-mono text-[#f97316] animate-pulse font-semibold">
                    PROCESSING...
                  </span>
                </div>

                <pre className="bg-black/40 backdrop-blur-md border border-white/5 rounded-xl p-5 font-mono text-[11px] leading-relaxed text-[#b7b5a9] shadow-inner overflow-x-auto space-y-1 min-h-[190px]">
                  {visibleLogs.map((log, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, x: -6 }}
                      animate={{ opacity: 1, x: 0 }}
                      className={
                        log.includes("[SUCCESS]")
                          ? "text-emerald-400 font-semibold"
                          : log.includes("[DEBUG]")
                          ? "text-[#9c87f5]"
                          : "text-zinc-300"
                      }
                    >
                      {log}
                    </motion.div>
                  ))}
                  <span className="inline-block w-1.5 h-3 bg-[#f97316] animate-pulse ml-0.5" />
                </pre>
              </motion.div>
            )}

            {/* STATE 2: RESULTS VIEW */}
            {!isScanning && results && (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, ease: "easeOut" }}
                className="w-full h-full"
              >
                <DiagnosticResultsView results={results} onReset={resetScan} />
              </motion.div>
            )}

            {/* STATE 3: IDLE STATE */}
            {!isScanning && !results && (
              <motion.div
                key="idle"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="my-auto space-y-5"
              >
                <div className="border-b border-white/[0.08] pb-3">
                  <span className="text-[11px] font-mono font-medium uppercase tracking-wider text-[#f97316] block mb-0.5">
                    Execution Telemetry
                  </span>
                  <h3 className="text-xl font-bold text-[#faf9f5]">
                    Awaiting Input Files
                  </h3>
                  <p className="text-xs text-[#b7b5a9] mt-0.5">
                    Provide an acoustic tap .wav and a surface image to initiate pipeline.
                  </p>
                </div>

                {/* IDLE TRACE TERMINAL CONSOLE */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-xs font-mono text-[#85827a]">
                    <Terminal size={14} />
                    <span>System Status: Standby</span>
                  </div>
                  <pre className="bg-black/40 backdrop-blur-md border border-white/5 rounded-xl p-5 font-mono text-[11px] leading-relaxed text-[#b7b5a9] shadow-inner space-y-1">
                    <div>[SYSTEM] TapEye Daemon v1.2.0 initialized.</div>
                    <div>[SYSTEM] DSP engine: Librosa (MFCC, FFT, Spectral Centroid)</div>
                    <div>[SYSTEM] Vision backbone: MobileNetV2 (224x224 input tensor)</div>
                    <div>[SYSTEM] Ready for multipart ingestion...</div>
                  </pre>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>
    </motion.div>
  );
}
