"use client";

import React, { useRef, useState } from "react";
import { Upload, Music, Image as ImageIcon, CheckCircle, FileAudio, FileImage, X } from "lucide-react";

interface UploadZoneProps {
  audioFile: File | null;
  imageFile: File | null;
  onAudioChange: (file: File | null) => void;
  onImageChange: (file: File | null) => void;
  audioPreviewUrl: string | null;
  imagePreviewUrl: string | null;
}

export default function UploadZone({
  audioFile,
  imageFile,
  onAudioChange,
  onImageChange,
  audioPreviewUrl,
  imagePreviewUrl,
}: UploadZoneProps) {
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

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
      {/* ACOUSTIC TAP AUDIO DROPZONE */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDraggingAudio(true);
        }}
        onDragLeave={() => setIsDraggingAudio(false)}
        onDrop={handleAudioDrop}
        onClick={() => !audioFile && audioInputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-2xl transition-all duration-300 backdrop-blur-md cursor-pointer ${
          isDraggingAudio
            ? "border-primary bg-primary/10 shadow-[0_0_20px_rgba(217,119,87,0.2)]"
            : audioFile
            ? "border-emerald-500/50 bg-emerald-950/20"
            : "border-neutral-800 bg-neutral-900/60 hover:border-neutral-700 hover:bg-neutral-900/90"
        }`}
      >
        <input
          type="file"
          ref={audioInputRef}
          accept="audio/wav,audio/*"
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              onAudioChange(e.target.files[0]);
            }
          }}
        />

        {audioFile ? (
          <div className="flex flex-col items-center text-center space-y-3 w-full">
            <div className="flex items-center justify-between w-full">
              <span className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
                <CheckCircle className="w-4 h-4" /> Acoustic Sample Ready
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onAudioChange(null);
                }}
                className="p-1 hover:bg-neutral-800 rounded-full text-neutral-400 hover:text-white transition"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="p-3 bg-neutral-800/80 rounded-xl flex items-center gap-3 w-full border border-neutral-700">
              <FileAudio className="w-8 h-8 text-primary shrink-0" />
              <div className="overflow-hidden text-left">
                <p className="text-sm font-medium text-white truncate">{audioFile.name}</p>
                <p className="text-xs text-neutral-400">
                  {(audioFile.size / (1024 * 1024)).toFixed(2)} MB
                </p>
              </div>
            </div>
            {audioPreviewUrl && (
              <audio controls className="w-full h-8 mt-2 accent-primary">
                <source src={audioPreviewUrl} type={audioFile.type || "audio/wav"} />
                Your browser does not support audio playback.
              </audio>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center text-center space-y-3">
            <div className="p-4 bg-neutral-800/50 rounded-full text-primary border border-neutral-700/50 group-hover:scale-105 transition-transform">
              <Music className="w-8 h-8" />
            </div>
            <div>
              <p className="text-sm font-semibold text-neutral-200">Acoustic Audio (.wav)</p>
              <p className="text-xs text-neutral-400 mt-1">
                Drag & drop tap recording or <span className="text-primary underline">browse</span>
              </p>
            </div>
          </div>
        )}
      </div>

      {/* VISUAL PRODUCE IMAGE DROPZONE */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setIsDraggingImage(true);
        }}
        onDragLeave={() => setIsDraggingImage(false)}
        onDrop={handleImageDrop}
        onClick={() => !imageFile && imageInputRef.current?.click()}
        className={`relative flex flex-col items-center justify-center p-6 border-2 border-dashed rounded-2xl transition-all duration-300 backdrop-blur-md cursor-pointer ${
          isDraggingImage
            ? "border-primary bg-primary/10 shadow-[0_0_20px_rgba(217,119,87,0.2)]"
            : imageFile
            ? "border-emerald-500/50 bg-emerald-950/20"
            : "border-neutral-800 bg-neutral-900/60 hover:border-neutral-700 hover:bg-neutral-900/90"
        }`}
      >
        <input
          type="file"
          ref={imageInputRef}
          accept="image/jpeg,image/png,image/*"
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              onImageChange(e.target.files[0]);
            }
          }}
        />

        {imageFile ? (
          <div className="flex flex-col items-center text-center space-y-3 w-full">
            <div className="flex items-center justify-between w-full">
              <span className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-emerald-400">
                <CheckCircle className="w-4 h-4" /> Visual Sample Ready
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onImageChange(null);
                }}
                className="p-1 hover:bg-neutral-800 rounded-full text-neutral-400 hover:text-white transition"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            {imagePreviewUrl ? (
              <div className="relative w-full h-28 rounded-xl overflow-hidden border border-neutral-700">
                <img
                  src={imagePreviewUrl}
                  alt="Produce Preview"
                  className="w-full h-full object-cover"
                />
              </div>
            ) : (
              <div className="p-3 bg-neutral-800/80 rounded-xl flex items-center gap-3 w-full border border-neutral-700">
                <FileImage className="w-8 h-8 text-primary shrink-0" />
                <div className="overflow-hidden text-left">
                  <p className="text-sm font-medium text-white truncate">{imageFile.name}</p>
                  <p className="text-xs text-neutral-400">
                    {(imageFile.size / (1024 * 1024)).toFixed(2)} MB
                  </p>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="flex flex-col items-center text-center space-y-3">
            <div className="p-4 bg-neutral-800/50 rounded-full text-primary border border-neutral-700/50 group-hover:scale-105 transition-transform">
              <ImageIcon className="w-8 h-8" />
            </div>
            <div>
              <p className="text-sm font-semibold text-neutral-200">Visual Image (.jpg / .png)</p>
              <p className="text-xs text-neutral-400 mt-1">
                Drag & drop surface photo or <span className="text-primary underline">browse</span>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
