import { ImageList } from "../components/images/ImageList"; 
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useRef} from "react";
import { useImages } from "../hooks/useImages";
import { ParticlesAnimation } from "../components/partials/ParticlesAnimation";

gsap.registerPlugin(ScrollTrigger);

export function Gallery() {
  const pinSectionRef = useRef(null);
  const containerRef = useRef(null);

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

  const { images: previewImages, loading } = useImages(3);

  return (
    <div className="bg-gray-50">
      <div ref={containerRef} className="relative bg-gradient-to-r from-neutral-800 to-zinc-950 text-white">
        <ParticlesAnimation />
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