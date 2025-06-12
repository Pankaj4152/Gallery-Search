import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ImageSearch } from './pages/ImageSearch';
import { ImageUpload } from './pages/ImageUpload';
import { Gallery } from './pages/Gallery';
import { HomePage } from './pages/HomePage';
import { Navbar } from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/gallery" element={<Gallery />} />
        <Route path="/search" element={<ImageSearch />} />
        <Route path="/upload" element={<ImageUpload />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App