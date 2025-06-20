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
        <form onSubmit={handleSubmit}>
            <input
                type='file'
                accept="image/*"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
            <button type="submit">Upload</button>
        </form>
    );
}