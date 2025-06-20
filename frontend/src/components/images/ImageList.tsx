import { useEffect, useState } from "react";
import { deleteImage, getImages } from '../../api/images.api'
import toast from "react-hot-toast";
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
            toast.error("Login failed:" + error, {
                style: {
                    background: "#450a0a",
                    color: "white",
                },
            });
        console.error("Error loading images", error);
      }
    }
    loadGallery();
  }, []);

  const handleDelete = async (id: number) => {
    try {
        await deleteImage(id);
        setImages(images.filter((img) => img.id !== id));
    } catch (error) {
            toast.error("Login deleting image:" + error, {
        style: {
            background: "#450a0a",
            color: "white",
        },
        });
        console.error("Error deleting image", error);
    }
  };

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
            <button onClick={() => handleDelete(image.id)}>Delete</button>
          </div>
        ))
      )}
    </div>
  );
}
 