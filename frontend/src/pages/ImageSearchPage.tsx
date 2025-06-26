import { useState } from "react";
import toast from "react-hot-toast";
import { searchImages } from "../api/images.api";
import { ParticlesAnimation } from "../components/partials/ParticlesAnimation";
import { SearchBar } from "../components/partials/SearchBar";
import { ImageResults } from "../components/images/SearchSystem";

export function ImageSearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) {
      toast('Please enter a search query', { icon: '⚠️' });
      return;
    }

    try {
      setLoading(true);
      const response = await searchImages(query);
      setResults(response.data);
      if (response.data.length === 0) {
        toast('No results found', { icon: '🏳️' });
      } else {
        toast.success('Results loaded successfully!');
      }
    } catch (error) {
      toast.error("Search failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50">
      {/* Hero + Search */}
      <div className="relative h-[110vh]">
        <ParticlesAnimation />
        <div className="z-10 relative flex flex-col items-center justify-center h-full text-white text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">Search Images</h1>
          <p className="text-sm md:text-lg text-gray-300 max-w-md mb-4">
            Search your images using natural language, we'll know where to find them.
          </p>
          <SearchBar
            query={query}
            setQuery={setQuery}
            handleSearch={handleSearch}
            loading={loading}
          />
        </div>
      </div>

      {/* Results section */}
      <ImageResults results={results} />
    </div>
  );
}
