import Particles, { initParticlesEngine } from "@tsparticles/react";
import { type ISourceOptions, MoveDirection, OutMode} from "@tsparticles/engine";
import { loadSlim } from "@tsparticles/slim";
import { useEffect, useMemo, useState } from "react";

export function ParticlesAnimation() {
    const [particlesInitialized, setParticlesInitialized] = useState(true);

    useEffect(() => {
        initParticlesEngine(async (engine) => {
            await loadSlim(engine);
        }).then(() => setParticlesInitialized(true));
        }, []);

    const particlesOptions: ISourceOptions = useMemo(
        () => ({
        fullScreen: { enable: false },
        background: {
        color: { value: "transparent" },
        },
        particles: {
        number: {
            value: 150,
            density: {
            enable: true,
            area: 800,
            },
        },
        color: {
            value: "#ffffff",
        },
        shape: {
            type: "circle",
        },
        opacity: {
            value: 0.5,
            random: true,
        },
        size: {
            value: 3,
            random: true,
        },
        move: {
            enable: true,
            speed: 2,
            direction: MoveDirection.none,
            random: true,
            straight: false,
            outModes: {
            default: OutMode.out,
            },
        },
        links: {
            enable: true,
            distance: 150,
            color: "#ffffff",
            opacity: 0.4,
            width: 1,
        },
        },
        interactivity: {
        events: {
            onHover: {
            enable: true,
            mode: "grab",
            },
            onClick: {
            enable: true,
            mode: "push",
            },
        },
        modes: {
            grab: {
            distance: 140,
            links: {
                opacity: 1,
            },
            },
            push: {
            quantity: 4,
            },
        },
        },
        detectRetina: true,
    }),
    [],
    );
    
  return (
    <>
      {particlesInitialized && (
        <Particles
          id="tsparticles"
          className="absolute inset-0 z-0"
          options={particlesOptions}
        />
      )}
    </>
  );
}