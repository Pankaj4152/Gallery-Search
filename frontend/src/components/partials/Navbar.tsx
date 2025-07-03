import { Link } from 'react-router-dom';
import logo from '../../assets/logo.png';
import { useState, useEffect } from 'react';

export function Navbar() {
    const [showNavbar, setShowNavbar] = useState(false);

    useEffect(() =>{
        const handleScroll = () => {
            if (window.scrollY > 30) {
                setShowNavbar(true);
            } else {
                setShowNavbar(false);
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
    <nav className={`fixed top-0 left-0 w-full z-50 transition-transform duration-500 ease-in-out ${
        showNavbar ? 'translate-y-0 opacity-100' : '-translate-y-full opacity-0'
      } py-3 flex items-center justify-between`}>
      <div className='bg-zinc-900/60 shadow-sm rounded-2xl w-full max-w-[1800px] mx-auto'>
        <div className='flex items-center justify-between h-16 px-4'>
                
                <div className='flex-shrink-0 flex items-center'>
                    <Link to="/" className='flex items-center gap-2'>
                        <img src={logo} alt="GalleryAI Logo" className="h-16 w-auto filter invert" />
                    </Link>
                </div>
             
                <div className='text-gray-400 hidden md:flex md:items-center md:space-x-1'>
                    <Link to="/gallery" className='px-3 py-2 rounded-md text-lg font-medium hover:text-sky-900 hover:bg-gray-50 transition-colors'>
                        My Gallery
                    </Link>
                    <Link to="/upload" className='px-3 py-2 rounded-md text-lg font-medium hover:text-sky-900 hover:bg-gray-50 transition-colors'>
                        Upload
                    </Link>
                    <Link to="/search" className='px-3 py-2 rounded-md text-lg font-medium hover:text-sky-900 hover:bg-gray-50 transition-colors'>
                        Search
                    </Link>
                </div>

                <div className='hidden md:flex md:items-center md:space-x-4'>
                    <Link to="/signup" className='px-3 py-2 text-base font-medium text-cyan-700 hover:text-indigo-500 transition-colors'>
                        Sign Up
                    </Link>
                    <Link to="/login" className='px-3 py-2 text-base font-medium text-gray-400 hover:text-indigo-600 transition-colors'>
                        Login
                    </Link>
                    <button onClick={logout} className='px-3 py-2 text-sm font-medium text-red-600 hover:text-red-800 transition-colors'>
                        Logout
                    </button>
                </div>
            </div>    
        </div>
    </nav>
    )
}

function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "/login";
}
