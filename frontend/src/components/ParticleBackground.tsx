"use client";

import React, { useMemo, useCallback } from "react";
import Particles, { ParticlesProvider } from "@tsparticles/react";
import { loadSlim } from "@tsparticles/slim";
import type { Engine, ISourceOptions } from "@tsparticles/engine";

export default function ParticleBackground() {
  const initEngine = useCallback(async (engine: Engine) => {
    await loadSlim(engine);
  }, []);

  const options: ISourceOptions = useMemo(
    () => ({
      background: {
        color: {
          value: "transparent",
        },
      },
      fpsLimit: 60,
      interactivity: {
        events: {
          onHover: {
            enable: true,
            mode: "grab",
          },
        },
        modes: {
          grab: {
            distance: 140,
            links: {
              opacity: 0.3,
              color: "#f97316",
            },
          },
        },
      },
      particles: {
        color: {
          value: ["#ffffff", "#f97316", "#d97757", "#9c87f5"],
        },
        links: {
          color: "#d97757",
          distance: 125,
          enable: true,
          opacity: 0.1,
          width: 1,
        },
        move: {
          direction: "none",
          enable: true,
          outModes: {
            default: "out",
          },
          random: true,
          speed: 0.6,
          straight: false,
        },
        number: {
          density: {
            enable: true,
            width: 900,
            height: 900,
          },
          value: 45,
        },
        opacity: {
          value: { min: 0.08, max: 0.2 },
        },
        shape: {
          type: "circle",
        },
        size: {
          value: { min: 1, max: 2.5 },
        },
      },
      detectRetina: true,
    }),
    []
  );

  return (
    <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <ParticlesProvider init={initEngine}>
        <Particles id="tsparticles" options={options} className="w-full h-full" />
      </ParticlesProvider>
    </div>
  );
}
