import React, { useRef, useEffect } from "react";
import { cn } from "@/lib/utils";

interface HolographicBeamsProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Density of the light pillars.
   * Default: 30
   */
  density?: number;
  /**
   * Speed of the animation.
   * Default: 1
   */
  speed?: number;
  /**
   * Intensity of the chromatic aberration (RGB shift).
   * Default: 2.5
   */
  aberration?: number;
  /**
   * Base color weight (mostly influences the center white-hot area).
   * Default: 50 (opacity percentage)
   */
  opacity?: number;
}

const HolographicBeams = ({
  className,
  density = 30,
  speed = 1,
  aberration = 2.5,
  opacity = 50,
  style,
  ...props
}: HolographicBeamsProps) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let width = container.offsetWidth;
    let height = container.offsetHeight;
    let time = 0;
    let animationFrameId: number;

    // --- NOISE GENERATOR (Sine Superposition) ---
    const noise = (x: number, t: number) => {
      return (
        Math.sin(x * 0.01 + t) +
        Math.sin(x * 0.03 + t * 2) * 0.5 +
        Math.sin(x * 0.1 + t * 4) * 0.25
      ) / 1.75;
    };

    const resize = () => {
      width = container.offsetWidth;
      height = container.offsetHeight;
      canvas.width = width;
      canvas.height = height;
    };

    const drawBeam = (x: number, t: number, color: string, widthMod: number) => {
      const n = noise(x, t * 0.5);
      const beamHeight = height * (0.6 + n * 0.4); 
      const beamWidth = (width / density) * widthMod;

      const gradient = ctx.createLinearGradient(x, height, x, height - beamHeight);
      gradient.addColorStop(0, color);
      gradient.addColorStop(1, "transparent");

      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.moveTo(x - beamWidth / 2, height);
      ctx.lineTo(x + beamWidth / 2, height);
      ctx.lineTo(x + beamWidth, height - beamHeight);
      ctx.lineTo(x - beamWidth, height - beamHeight);
      ctx.fill();
    };

    const draw = () => {
      ctx.clearRect(0, 0, width, height);
      ctx.globalCompositeOperation = "screen";

      time += 0.01 * speed;
      const beamWidth = width / density;

      for (let i = 0; i <= density; i++) {
        const x = i * beamWidth;
        
        // 1. RED CHANNEL
        const rAlpha = (opacity / 100) * (0.5 + 0.5 * Math.cos(i * 0.5 + time));
        drawBeam(
            x - aberration, 
            time + i * 0.1, 
            `rgba(255, 0, 0, ${rAlpha * 0.5})`, 
            1.5
        );

        // 2. BLUE CHANNEL
        const bAlpha = (opacity / 100) * (0.5 + 0.5 * Math.sin(i * 0.6 + time * 1.1));
        drawBeam(
            x + aberration, 
            time + i * 0.12 + 10, 
            `rgba(0, 50, 255, ${bAlpha * 0.5})`, 
            1.5
        );

        // 3. GREEN/WHITE CHANNEL
        const coreAlpha = (opacity / 100) * (0.6 + 0.4 * Math.sin(i * 0.3 - time));
        drawBeam(
            x, 
            time + i * 0.1 + 5, 
            `rgba(200, 255, 255, ${coreAlpha * 0.3})`, 
            0.8
        );
      }

      animationFrameId = requestAnimationFrame(draw);
    };

    window.addEventListener("resize", resize);
    resize();
    draw();

    return () => {
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [density, speed, aberration, opacity]);

  return (
    <div
      ref={containerRef}
      className={cn("absolute inset-0 z-0 overflow-hidden bg-black", className)}
      style={style}
      {...props}
    >
      <canvas 
        ref={canvasRef} 
        className="block w-full h-full filter blur-[4px]"
      />
      
      {/* Texture Overlay (Scanlines) */}
      <div 
        className="absolute inset-0 z-10 pointer-events-none opacity-20"
        style={{
            backgroundImage: "linear-gradient(rgba(0,0,0,0) 50%, rgba(0,0,0,1) 50%), linear-gradient(90deg, rgba(255,0,0,0.06), rgba(0,255,0,0.02), rgba(0,0,255,0.06))",
            backgroundSize: "100% 4px, 3px 100%"
        }}
      />
      
      {/* Vignette */}
      <div className="absolute inset-0 z-20 bg-[radial-gradient(circle_at_center,transparent_0%,#000_100%)]" />
    </div>
  );
};

export default HolographicBeams;
