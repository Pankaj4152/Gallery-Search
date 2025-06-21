import { Link } from "react-router-dom";
import GalleryButton from "../components/partials/GalleryButton";

export function HomePage() {
  return (
    <div className="bg-gray-50">            
      <section className="py-40 px-4 text-center bg-gradient-to-r from-neutral-800 to-zinc-950 text-white rounded-lg">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Discover & Organize Your Images</h1>
          <p className="text-xl md:text-2xl mb-8">Search anything find something. Upload and manage your visual collection with ease</p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link to="/gallery">
              <GalleryButton text="My Gallery"/>
            </Link>
            <Link to="/upload" >
              <GalleryButton text="Upload Image" />
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16 px-4 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">Key Features</h2>
        
        {/* Feature 1 */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
            <div className="text-cyan-700 mb-4">
              <svg className="w-10 h-10 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center">AI-Powered Search</h3>
            <p className="text-gray-600 text-center">
              Find images using natural language queries powered by FAISS technology.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
            <div className="text-cyan-700 mb-4">
              <svg className="w-10 h-10 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center">Easy Upload</h3>
            <p className="text-gray-600 text-center">
              Drag and drop or select multiple images to upload in seconds.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow">
            <div className="text-cyan-700 mb-4">
              <svg className="w-10 h-10 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center">Smart Gallery</h3>
            <p className="text-gray-600 text-center">
              Automatically organized collections with metadata extraction.
            </p>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 px-4 bg-gray-100">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6 text-gray-800">Ready to organize your images?</h2>
          <p className="text-xl mb-8 text-gray-600">Join thousands of users managing their visual content efficiently</p>
          <Link 
            to="/signup" 
            className="inline-block bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors shadow-lg"
          >
            Get Started for Free
          </Link>
        </div>
      </section>
    </div>
  );
}