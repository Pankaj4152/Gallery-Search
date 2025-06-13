import { useEffect, useState } from "react";
import { getImages } from '../../api/images.api'

export function ImageList() {
    const [images,  setImages] = useState([]);

    useEffect(() => {
        async function loadGallery() {
            const res = await getImages();
            setImages(res.data);
        }
        loadGallery();
    }, []);

    return <div>
        {images.map(image => (
            <div>
                <h1>{ image.image_file }</h1> {/* Delete this is testing (cuz its not running) */}  
            </div>
        ))}
    </div>
    
}