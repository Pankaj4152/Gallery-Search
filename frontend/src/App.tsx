import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ImageSearch } from './pages/ImageSearch';
import { ImageUpload } from './pages/ImageUpload';
import { Gallery } from './pages/Gallery';
import { HomePage } from './pages/HomePage';
import { Navbar } from './components/partials/Navbar';
import { Signup } from './pages/Signup';
import { Login } from './pages/Login';
import { RequireAuth } from './components/RequireAuth';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/search" element={<ImageSearch />} />
        <Route path="/upload" element={<ImageUpload />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/gallery" element={<RequireAuth><Gallery /></RequireAuth>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App