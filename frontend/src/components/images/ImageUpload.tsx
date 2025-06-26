import React, { useState } from "react";
import { uploadImages } from '../../api/images.api';
import toast from "react-hot-toast";

export function UploadImage({ onUploadSuccess }: { onUploadSuccess?: () => void}) {
    const [file, setFile] = useState<File | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append("image", file);

        try {
            await uploadImages(formData);
            setFile(null);
            //setDescription("");
            if (onUploadSuccess) onUploadSuccess();
            toast.success('Image uploaded succesfully', {
                style: {
                    background: "#022c1e",
                    color: "white"
                }
            });
        } catch (err) {
            toast.error("Login failed: " + err, {
                style: {
                background: "#450a0a",
                color: "white",
                }
            });
            console.error("Upload failed", err);
        }     
    };

    return (
        <div className="py-40 px-4 text-center bg-gradient-to-r from-neutral-800 to-zinc-950 text-white rounded-lg">
            <form onSubmit={handleSubmit} className="justify-center text-center">
                {file && (
                <img
                    src={URL.createObjectURL(file)}
                    alt="Preview"
                    className="mx-auto mt-6 rounded-lg shadow-lg max-w-sm"
                />
                )}
                <input
                    type='file'
                    accept="image/*"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="mt-6 px-6 py-2 bg-white text-black rounded-md font-medium hover:bg-gray-200 transition"
                />
                <button type="submit" className="mt-6 px-6 py-2 bg-white text-black rounded-md font-medium hover:bg-gray-200 transition">Upload</button>
            </form>
        </div>
    );
}