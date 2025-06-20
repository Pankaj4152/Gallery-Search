import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ImageSearchPage } from './pages/ImageSearchPage';
import { ImageUploadPage } from './pages/ImageUploadPage';
import { Gallery } from './pages/Gallery';
import { HomePage } from './pages/HomePage';
import { Navbar } from './components/partials/Navbar';
import { Signup } from './pages/Signup';
import { Login } from './pages/Login';
import { RequireAuth } from './components/RequireAuth';
import { Toaster } from 'react-hot-toast';

function App() {
  return (
    <BrowserRouter>
      <div className='min-h-screen flex flex-col'>
        <Navbar/>  
        <main className='flex-grow'>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<ImageSearchPage />} />
            <Route path="/upload" element={<ImageUploadPage />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/login" element={<Login />} />
            <Route path="/gallery" element={<RequireAuth><Gallery /></RequireAuth>} />
          </Routes>
        </main>

        <Toaster/>
      </div>  
    </BrowserRouter>
  );
}

export default App