import { useEffect, useState } from "react";
import { getImages } from '../../api/images.api'
interface Image {
  id: number;
  image_file: string;
  description?: string;
}

export function ImageList() {
  const [images, setImages] = useState<Image[]>([]);

  useEffect(() => {
    async function loadGallery() {
      try {
        const res = await getImages();
        setImages(res.data);
      } catch (error) {
        console.error("Error loading images", error);
      }
    }
    loadGallery();
  }, []);

  return (
    <div>
      {images.length === 0 ? (
        <p>No uploaded images</p>
      ) : (
        images.map((image) => (
          <div key={image.id}>
            <img
              src={`http://localhost:8000${image.image_file}`}
              alt={"Image"}
              style={{ maxWidth: "300px" }}
            />
            {image.description && <p>{image.description}</p>}
          </div>
        ))
      )}
    </div>
  );
}
 