import React, { useState } from "react";
import { uploadImages } from '../../api/images.api';
import toast from "react-hot-toast";

export function UploadImage({ onUploadSuccess }: { onUploadSuccess?: () => void}) {
    const [files, setFiles] = useState<File[]>([]);
    const [uploading, setUploading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFiles = Array.from(e.target.files || []);
        setFiles(selectedFiles);
    };

    const removeFile = (index: number) => {
        setFiles(files.filter((_, i) => i !== index));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (files.length === 0) {
            toast.error("Please select at least one image to upload");
            return;
        }

        setUploading(true);
        const formData = new FormData();
        
        // Append all files with the same key 'image'
        files.forEach(file => {
            formData.append("image", file);
        });

        try {
            const response = await uploadImages(formData);
            setFiles([]);
            
            // Reset the file input
            const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
            if (fileInput) fileInput.value = '';
            
            if (onUploadSuccess) onUploadSuccess();
            
            toast.success(`${files.length} image(s) uploaded successfully!`, {
                style: {
                    background: "#022c1e",
                    color: "white"
                }
            });

            // Show warnings if any files were rejected
            if (response.warnings) {
                response.warnings.forEach((warning: string) => {
                    toast.error(warning, {
                        style: {
                            background: "#450a0a",
                            color: "white",
                        }
                    });
                });
            }
        } catch (err: any) {
            toast.error("Upload failed: " + (err.response?.data?.error || err.message), {
                style: {
                    background: "#450a0a",
                    color: "white",
                }
            });
            console.error("Upload failed", err);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="py-40 px-4 text-center bg-gradient-to-r from-neutral-800 to-zinc-950 text-white rounded-lg">
            <form onSubmit={handleSubmit} className="justify-center text-center">
                
                {/* File Input */}
                <input
                    type='file'
                    accept="image/*"
                    multiple
                    onChange={handleFileChange}
                    className="mt-6 px-6 py-2 bg-white text-black rounded-md font-medium hover:bg-gray-200 transition"
                />
                
                {/* Selected Files Info */}
                {files.length > 0 && (
                    <div className="mt-4 text-sm text-gray-300">
                        <p>{files.length} file(s) selected</p>
                        <p className="text-xs">Total size: {(files.reduce((sum, file) => sum + file.size, 0) / (1024 * 1024)).toFixed(2)} MB</p>
                    </div>
                )}

                {/* Image Previews */}
                {files.length > 0 && (
                    <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
                        {files.map((file, index) => (
                            <div key={index} className="relative group">
                                <img
                                    src={URL.createObjectURL(file)}
                                    alt={`Preview ${index + 1}`}
                                    className="w-full h-32 object-cover rounded-lg shadow-lg"
                                />
                                <button
                                    type="button"
                                    onClick={() => removeFile(index)}
                                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm hover:bg-red-600 transition opacity-0 group-hover:opacity-100"
                                >
                                    ×
                                </button>
                                <p className="mt-2 text-xs text-gray-400 truncate">{file.name}</p>
                                <p className="text-xs text-gray-500">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                            </div>
                        ))}
                    </div>
                )}

                {/* Upload Button */}
                <button 
                    type="submit" 
                    disabled={files.length === 0 || uploading}
                    className={`mt-6 px-6 py-2 rounded-md font-medium transition ${
                        files.length === 0 || uploading
                            ? 'bg-gray-500 text-gray-300 cursor-not-allowed'
                            : 'bg-white text-black hover:bg-gray-200'
                    }`}
                >
                    {uploading ? 'Uploading...' : `Upload ${files.length > 0 ? `${files.length} Image(s)` : 'Images'}`}
                </button>

                {/* Clear All Button */}
                {files.length > 0 && (
                    <button
                        type="button"
                        onClick={() => setFiles([])}
                        className="mt-2 ml-4 px-4 py-2 bg-red-600 text-white rounded-md font-medium hover:bg-red-700 transition"
                    >
                        Clear All
                    </button>
                )}
            </form>
        </div>
    );
}