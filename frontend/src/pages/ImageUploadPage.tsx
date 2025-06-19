import { UploadImage } from "../components/images/ImageUpload";
import React, { useState, type JSX } from "react";

export function ImageUploadPage(): JSX.Element {
  const [reloadFlag, setReloadFlag] = useState(false);

  return (
    <div className="container mt-4">
      <h1 className="mb-4">Upload an Image</h1>
      <div className="card shadow-sm p-4">
        <UploadImage onUploadSuccess={() => setReloadFlag(!reloadFlag)} />
      </div>
    </div>
  );
}