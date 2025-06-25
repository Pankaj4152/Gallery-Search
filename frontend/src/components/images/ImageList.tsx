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
    const [selectedImage, setSelectedImage] = useState<Image | null>(null);

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
    <div className="grid grid-cols-1 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-1">
        {images.length === 0 ? (
        <p>No uploaded images</p>
        ) : (
        images.map((image) => (
            <div key={image.id}>
            <img
                onClick={() => setSelectedImage(image)}
                src={`http://localhost:8000${image.image_file}`}
                alt={"Image"}
                className="w-60 h-60 object-cover rounded-lg cursor-pointer hover:scale-105 transition"
            />
            {image.description && <p>{image.description}</p>}
            <button onClick={() => handleDelete(image.id)}>Delete</button>
            </div>
            ))
        )}

      {selectedImage && (
        <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg max-w-2xl w-full relative shadow-xl">
            <button
              onClick={() => setSelectedImage(null)}
              className="absolute top-2 right-3 text-2xl font-bold text-black hover:text-red-500"
            >
              ×
            </button>
            <img
              src={`http://localhost:8000${selectedImage.image_file}`}
              alt={selectedImage.description}
              className="w-full max-h-[70vh] object-contain rounded"
            />
            <p className="mt-4 text-gray-800">{selectedImage.description}</p>
          </div>
        </div>
      )}
    </div>
    );
}
