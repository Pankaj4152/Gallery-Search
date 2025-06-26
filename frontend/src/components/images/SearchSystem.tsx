interface Image {
  id: number;
  image_file: string;
  description: string;
}

export function ImageResults({ results }: { results: Image[] }) {
  if (!results.length) return null;

  return (
    <div className="px-4 py-16 max-w-7xl mx-auto">
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {results.map((image) => (
          <div key={image.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <img
              src={`http://localhost:8000${image.image_file}`}
              alt="Search Result"
              className="w-full h-60 object-cover"
            />
            <div className="p-4">
              <p className="text-sm text-gray-700">
                {image.description || "No description"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

