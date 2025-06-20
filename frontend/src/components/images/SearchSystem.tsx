import toast from "react-hot-toast";
import { searchImages } from "../../api/images.api";
import { useState } from "react";

interface Image {
    id: number;
    image_file: string;
    description: string;
}

export function ImageSearch() {
    const [query, setQuery] = useState("");
    const [results, setResults] = useState<Image[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) {
            toast('Please enter a search query', {
                icon: '⚠️',
                style: {
                    background: '#713200',
                }
            });
            return;
        }

        try {
            setLoading(true);
            const response = await searchImages(query);
            setResults(response.data);
            if (response.data.length == 0) {
                toast('No results found', {
                    icon: '🏳️',
                });
            } else {
                toast.success('Results loaded successfully!', {
                style: {
                    background: "#022c1e",
                    color: "white"
                    }
                });
            };
        } catch (error) {
            toast.error("Search failed:" + error, {
                style: {
                    background: "#450a0a",
                    color: "white",
                },
            });
            console.error("Search failed" , error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-3">Search Images</h2>

            <div className="input-group mb-4">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Enter a description..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button
                    className="btn btn-primary"
                    onClick={handleSearch}
                    disabled={loading}
                >
                    {loading ? "Searching..." : "Search"}
                </button>
            </div>

            <div className="row">
                {results.map((image) => (
                    <div key={image.id} className="col-md-4 mb-4">
                        <div className="card h-10 shadow-sm">
                            <img
                                src={`http://localhost:8000${image.image_file}`}
                                className="card-img-top"
                                alt="Search Result"
                                style={{ maxWidth: "300px" }}
                            />
                            <div className="card-body">
                                <p className="card-text">{image.description || "No description"}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
