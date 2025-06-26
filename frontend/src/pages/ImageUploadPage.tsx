import { UploadImage } from "../components/images/ImageUpload";
import { DragDropUpload } from "../components/images/DragDropUpload";
import { useState, type JSX } from "react";
import { ParticlesAnimation } from "../components/partials/ParticlesAnimation";

export function ImageUploadPage(): JSX.Element {
  const [reloadFlag, setReloadFlag] = useState(false);

  return (
    <div className="bg-gray-50">
      <div className="relative h-[60vh]">
        <ParticlesAnimation />
        <div className="z-10 relative flex flex-col items-center justify-center h-full">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Upload Images</h1> 
          <p className="text-sm md:text-lg text-gray-300 mt-2">Upload multiple images and explore our AI processing</p>
        </div>
        {/* Use either UploadImage or DragDropUpload */}
        <UploadImage onUploadSuccess={() => setReloadFlag(!reloadFlag)} />
        {/* <DragDropUpload onUploadSuccess={() => setReloadFlag(!reloadFlag)} /> */}
      </div>
    </div>
  );
}