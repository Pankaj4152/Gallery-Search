import React, { useState, useRef } from "react";
import { uploadImages } from '../../api/images.api';
import toast from "react-hot-toast";

export function DragDropUpload({ onUploadSuccess }: { onUploadSuccess?: () => void }) {
    const [files, setFiles] = useState<File[]>([]);
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        const droppedFiles = Array.from(e.dataTransfer.files).filter(
            file => file.type.startsWith('image/')
        );
        
        if (droppedFiles.length > 0) {
            setFiles(prev => [...prev, ...droppedFiles]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = Array.from(e.target.files || []);
        setFiles(prev => [...prev, ...selectedFiles]);
    };

    const removeFile = (index: number) => {
        setFiles(files.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (files.length === 0) return;

        setUploading(true);
        const formData = new FormData();
        files.forEach(file => formData.append("image", file));

        try {
            const response = await uploadImages(formData);
            setFiles([]);
            if (inputRef.current) inputRef.current.value = '';
            if (onUploadSuccess) onUploadSuccess();
            
            toast.success(`${files.length} image(s) uploaded successfully!`);
            
            if (response.warnings) {
                response.warnings.forEach((warning: string) => {
                    toast.error(warning);
                });
            }
        } catch (err: any) {
            toast.error("Upload failed: " + (err.response?.data?.error || err.message));
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="py-8 px-4 bg-gradient-to-r from-neutral-800 to-zinc-950 text-white rounded-lg">
            <form onSubmit={handleSubmit} className="space-y-6">
                {/* Drag & Drop Area */}
                <div
                    className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                        dragActive 
                            ? 'border-blue-400 bg-blue-50 bg-opacity-10' 
                            : 'border-gray-400 hover:border-gray-300'
                    }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={() => inputRef.current?.click()}
                >
                    <input
                        ref={inputRef}
                        type="file"
                        accept="image/*"
                        multiple
                        onChange={handleFileChange}
                        className="hidden"
                    />
                    
                    <div className="space-y-4">
                        <div className="text-4xl">📸</div>
                        <div>
                            <p className="text-lg font-medium">
                                Drop your images here, or click to browse
                            </p>
                            <p className="text-sm text-gray-400 mt-2">
                                Supports: JPEG, PNG, WebP • Max 10MB per file
                            </p>
                        </div>
                    </div>
                </div>

                {/* File Previews */}
                {files.length > 0 && (
                    <div className="space-y-4">
                        <div className="text-center">
                            <p className="text-lg">{files.length} file(s) selected</p>
                            <p className="text-sm text-gray-400">
                                Total: {(files.reduce((sum, file) => sum + file.size, 0) / (1024 * 1024)).toFixed(2)} MB
                            </p>
                        </div>
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {files.map((file, index) => (
                                <div key={index} className="relative group">
                                    <img
                                        src={URL.createObjectURL(file)}
                                        alt={`Preview ${index + 1}`}
                                        className="w-full h-24 object-cover rounded-lg"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => removeFile(index)}
                                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm hover:bg-red-600 transition"
                                    >
                                        ×
                                    </button>
                                    <p className="mt-1 text-xs text-gray-400 truncate">{file.name}</p>
                                </div>
                            ))}
                        </div>

                        <div className="flex justify-center gap-4">
                            <button
                                type="submit"
                                disabled={uploading}
                                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-500 transition"
                            >
                                {uploading ? 'Uploading...' : `Upload ${files.length} Image(s)`}
                            </button>
                            <button
                                type="button"
                                onClick={() => setFiles([])}
                                className="px-6 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition"
                            >
                                Clear All
                            </button>
                        </div>
                    </div>
                )}
            </form>
        </div>
    );
}
