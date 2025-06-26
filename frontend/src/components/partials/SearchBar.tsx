interface Props {
  query: string;
  setQuery: (value: string) => void;
  handleSearch: () => void;
  loading: boolean;
}

export function SearchBar({ query, setQuery, handleSearch, loading }: Props) {
  return (
    <div className="flex flex-col md:flex-row items-center justify-center gap-3 mt-6">
      <input
        type="text"
        className="w-full md:w-96 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm transition"
        placeholder="Enter a description..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button
        onClick={handleSearch}
        disabled={loading}
        className={`px-5 py-2 rounded-lg font-semibold transition-colors shadow-md ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-indigo-600 hover:bg-indigo-700 text-white"
        }`}
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </div>
  );
}
