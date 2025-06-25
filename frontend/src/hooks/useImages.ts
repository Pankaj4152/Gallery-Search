import { useEffect, useState } from "react";
import { getImages } from "../api/images.api";

export interface Image {
  id: number;
  image_file: string;
  description: string;
}

export function useImages(limit?: number) {
    const [images, setImages] = useState<Image[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getImages().then((response) => {
            const images = response.data as Image[];
            const sorted = images.sort((a, b) => b.id - a.id);
            setImages(limit ? sorted.slice(0, limit) : sorted);
            setLoading(false);
        });
    }, [limit]);
    
    return { images, loading };
}