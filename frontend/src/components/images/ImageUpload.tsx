import React, { useEffect, useState } from "react";
import { uploadImages } from '../../api/images.api';

export function UploadImage({ onUploadSuccess }: { onUploadSuccess?: () => void}) {
    const [file, setFile] = useState<File | null>(null);
    //const [description, setDescription] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return;

        const formData = new FormData();
        formData.append("image", file);
        //formData.append("description", description);

        try {
            await uploadImages(formData);
            setFile(null);
            //setDescription("");
            if (onUploadSuccess) onUploadSuccess();
        } catch (err) {
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
            {/*
            <input
                type="text"
                name="optionalField"
                placeholder="Description (Optional)"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            */}
            <button type="submit">Upload</button>
        </form>
    );
}