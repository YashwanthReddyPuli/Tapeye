"use client";

import React, { useRef, useState } from "react";
import { UploadCloud, FileAudio, Image as ImageIcon, X } from "lucide-react";
import { motion } from "framer-motion";

interface SensorIntakePanelProps {
  audioFile: File | null;
  imageFile: File | null;
  onAudioChange: (file: File | null) => void;
  onImageChange: (file: File | null) => void;
  audioPreviewUrl: string | null;
  imagePreviewUrl: string | null;
  onExecute: () => void;
  isScanning: boolean;
}

export default function SensorIntakePanel({
  audioFile,
  imageFile,
  onAudioChange,
  onImageChange,
  audioPreviewUrl,
  imagePreviewUrl,
  onExecute,
  isScanning,
}: SensorIntakePanelProps) {
  const audioInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);

  const [isDraggingAudio, setIsDraggingAudio] = useState(false);
  const [isDraggingImage, setIsDraggingImage] = useState(false);

  const handleAudioDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDraggingAudio(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.includes("audio") || file.name.endsWith(".wav")) {
        onAudioChange(file);
      }
    }
  };

  const handleImageDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDraggingImage(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.includes("image") || file.name.endsWith(".jpg") || file.name.endsWith(".png")) {
        onImageChange(file);
      }
    }
  };

  const canExecute = Boolean(audioFile && imageFile && !isScanning);

  return (
    <div className="flex flex-col gap-6 h-full text-[#faf9f5]">
      {/* SECTION HEADER */}
      <div>
        <h2 className="text-xl font-bold tracking-tight text-[#faf9f5]">
          Source Files
        </h2>
        <p className="text-xs text-[#b7b5a9] mt-1">
          Upload an audio tap recording and a produce surface image.
        </p>
      </div>

      {/* AUDIO INTAKE CARD */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="font-semibold text-[#faf9f5] flex items-center gap-1.5">
            <FileAudio size={16} className="text-[#f97316]" /> Acoustic Tap Audio (.wav)
          </span>
          {audioFile && (
            <span className="text-[10px] font-mono font-semibold text-[#f97316] bg-orange-500/10 px-2.5 py-0.5 rounded-full border border-[#f97316]/30">
              Ready
            </span>
          )}
        </div>

        <input
          type="file"
          ref={audioInputRef}
          accept="audio/wav,audio/*"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && onAudioChange(e.target.files[0])}
        />

        {audioFile ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-black/30 backdrop-blur-[30px] rounded-2xl border border-white/[0.08] p-4 space-y-2.5"
          >
            <div className="flex items-center justify-between text-xs">
              <div className="truncate text-left">
                <p className="font-semibold text-[#faf9f5] truncate">{audioFile.name}</p>
                <p className="text-[10px] font-mono text-[#b7b5a9]">
                  {(audioFile.size / 1024).toFixed(1)} KB &bull; 44.1kHz WAV
                </p>
              </div>
              <button
                onClick={() => onAudioChange(null)}
                className="p-1 rounded-lg hover:bg-white/10 text-[#b7b5a9] hover:text-[#faf9f5] transition cursor-pointer"
              >
                <X size={15} />
              </button>
            </div>

            {audioPreviewUrl && (
              <audio controls className="w-full h-8 text-xs accent-[#f97316]">
                <source src={audioPreviewUrl} type={audioFile.type || "audio/wav"} />
              </audio>
            )}
          </motion.div>
        ) : (
          <motion.div
            whileHover={{ y: -4, scale: 1.01 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDraggingAudio(true);
            }}
            onDragLeave={() => setIsDraggingAudio(false)}
            onDrop={handleAudioDrop}
            onClick={() => audioInputRef.current?.click()}
            className={`bg-black/20 backdrop-blur-[20px] border-2 border-dashed rounded-2xl p-8 transition-all duration-300 flex flex-col items-center justify-center cursor-pointer text-center ${
              isDraggingAudio
                ? "border-[#f97316] bg-white/[0.06]"
                : "border-white/5 hover:bg-white/[0.04] hover:border-[#f97316]/50"
            }`}
          >
            <UploadCloud size={24} className="text-[#f97316] mb-2" />
            <p className="text-xs font-semibold text-[#faf9f5]">Drop Audio Tap File</p>
            <p className="text-[11px] text-[#b7b5a9] mt-0.5">Drag and drop or browse (.wav)</p>
          </motion.div>
        )}
      </div>

      {/* VISUAL INTAKE CARD */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs">
          <span className="font-semibold text-[#faf9f5] flex items-center gap-1.5">
            <ImageIcon size={16} className="text-[#9c87f5]" /> Surface Photo (.jpg / .png)
          </span>
          {imageFile && (
            <span className="text-[10px] font-mono font-semibold text-[#9c87f5] bg-[#9c87f5]/20 px-2.5 py-0.5 rounded-full border border-[#9c87f5]/40">
              Ready
            </span>
          )}
        </div>

        <input
          type="file"
          ref={imageInputRef}
          accept="image/jpeg,image/png,image/*"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && onImageChange(e.target.files[0])}
        />

        {imageFile ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-black/30 backdrop-blur-[30px] rounded-2xl border border-white/[0.08] p-4 space-y-2.5"
          >
            <div className="relative rounded-xl overflow-hidden border border-white/10 h-36 bg-black/40 flex items-center justify-center">
              {imagePreviewUrl ? (
                <img src={imagePreviewUrl} alt="Preview" className="w-full h-full object-cover" />
              ) : (
                <ImageIcon size={28} className="text-[#b7b5a9]" />
              )}
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent flex items-end justify-between p-3">
                <span className="text-[10px] font-mono text-white font-medium truncate">{imageFile.name}</span>
                <span className="text-[10px] font-mono text-[#b7b5a9]">
                  {(imageFile.size / 1024).toFixed(1)} KB
                </span>
              </div>
              <button
                onClick={() => onImageChange(null)}
                className="absolute top-2 right-2 p-1 rounded-md bg-black/80 text-white hover:bg-black transition cursor-pointer"
              >
                <X size={14} />
              </button>
            </div>
          </motion.div>
        ) : (
          <motion.div
            whileHover={{ y: -4, scale: 1.01 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDraggingImage(true);
            }}
            onDragLeave={() => setIsDraggingImage(false)}
            onDrop={handleImageDrop}
            onClick={() => imageInputRef.current?.click()}
            className={`bg-black/20 backdrop-blur-[20px] border-2 border-dashed rounded-2xl p-8 transition-all duration-300 flex flex-col items-center justify-center cursor-pointer text-center ${
              isDraggingImage
                ? "border-[#9c87f5] bg-white/[0.06]"
                : "border-white/5 hover:bg-white/[0.04] hover:border-[#f97316]/50"
            }`}
          >
            <UploadCloud size={24} className="text-[#9c87f5] mb-2" />
            <p className="text-xs font-semibold text-[#faf9f5]">Drop Produce Image</p>
            <p className="text-[11px] text-[#b7b5a9] mt-0.5">Drag and drop or browse (.jpg, .png)</p>
          </motion.div>
        )}
      </div>

      {/* ACTION BUTTON */}
      <div className="mt-auto pt-2">
        <motion.button
          whileHover={canExecute ? { scale: 1.02 } : {}}
          whileTap={canExecute ? { scale: 0.98 } : {}}
          onClick={onExecute}
          disabled={!canExecute}
          className={
            canExecute
              ? "w-full py-4 rounded-xl font-semibold tracking-wide bg-gradient-to-r from-orange-500 to-orange-600 shadow-[0_0_20px_rgba(249,115,22,0.3)] text-white border-transparent cursor-pointer transition-all flex items-center justify-center gap-2"
              : "w-full py-4 rounded-xl font-semibold tracking-wide bg-white/5 text-white/30 border border-white/10 cursor-not-allowed transition-all flex items-center justify-center gap-2"
          }
        >
          Run Scan
        </motion.button>
      </div>
    </div>
  );
}
