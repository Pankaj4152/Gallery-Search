import { ImageList } from "../components/images/ImageList"; 
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useEffect, useMemo, useRef, useState } from "react";
import Particles, { initParticlesEngine } from "@tsparticles/react";
import { type ISourceOptions, MoveDirection, OutMode} from "@tsparticles/engine";
import { loadSlim } from "@tsparticles/slim";
import { useImages } from "../hooks/useImages";

gsap.registerPlugin(ScrollTrigger);

export function Gallery() {
  const pinSectionRef = useRef(null);
  const containerRef = useRef(null);
  const [particlesInitialized, setParticlesInitialized] = useState(true);

  useGSAP(() => {
    ScrollTrigger.create({
      trigger: containerRef.current,
      start: "top top",
      end: "+=80%",
      pin: pinSectionRef.current,
      pinSpacing: true,
      scrub: true,
    });
  }, []);

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

  const { images: previewImages, loading } = useImages(3);

  return (
    <div className="bg-gray-50">
      <div ref={containerRef} className="relative bg-gradient-to-r from-neutral-800 to-zinc-950 text-white">
        {particlesInitialized && (
          <Particles
            id="tsparticles"
            className="absolute inset-0 z-0"
            options={particlesOptions}
          />
        )}
        <div ref={pinSectionRef} className="h-screen flex flex-col items-center justify-center gap-4 relative z-10">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">My Gallery</h1>
          <p className="text-sm md:text-lg text-gray-300 mt-2">
            Explore your intelligent gallery.
          </p>

          {!loading && previewImages.length > 0 && (
            <div className="flex gap-4 mt-6">
              {previewImages.map((img) => (
                <img
                  key={img.id}
                  src={"http://localhost:8000" + img.image_file}
                  alt={img.description}
                  className="w-24 h-24 object-cover rounded-lg opacity-40 hover:opacity-80 transition"
                />
              ))}
            </div>
          )}

          <button
            onClick={() => document.getElementById("gallery-list")?.scrollIntoView({ behavior: "smooth" })}
            className="mt-6 px-6 py-2 bg-white text-black rounded-md font-medium hover:bg-gray-200 transition"
          >
            See gallery
          </button>
        </div>
      </div>

      <div id='gallery-list' className="container mx-auto px-4 py-12 relative z-10">
        <ImageList />
      </div>
    </div>
  );
}