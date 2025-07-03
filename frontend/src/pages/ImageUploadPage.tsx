import { UploadImage } from "../components/images/ImageUpload";
import { useState, type JSX } from "react";
import { ParticlesAnimation } from "../components/partials/ParticlesAnimation";

export function ImageUploadPage(): JSX.Element {
  const [reloadFlag, setReloadFlag] = useState(false);

  return (
    <div className="bg-gray-50">
      <div className="relative h-[60vh]">
        <ParticlesAnimation />
        <div className="bg-zinc-900 z-10 relative flex flex-col items-center justify-center h-full">
          <h1 className="text-white text-4xl md:text-5xl font-bold mb-6">Upload Images</h1> 
          <p className="text-sm md:text-lg text-gray-300 mt-2">Upload your images and explore our IA processing</p>
        </div>
        <UploadImage onUploadSuccess={() => setReloadFlag(!reloadFlag)} />
      </div>
    </div>
  );
}