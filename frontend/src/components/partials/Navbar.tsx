import { Link } from 'react-router-dom';

export function Navbar() {
    return (
    <nav className='fixed w-full top-2 z-50'>
      <div className='bg-zinc-900 shadow-sm rounded-2xl w-full max-w-[1800px] mx-auto'>
        <div className='flex items-center justify-between h-16 px-4'>
                
                <div className='flex-shrink-0 flex items-center'>
                    <Link to="/" className='text-xl font-bold text-cyan-800 hover:text-sky-900 transition-colors'>
                        GalleryAI
                    </Link>
                </div>
             
                <div className='hidden md:flex md:items-center md:space-x-1'>
                    <Link to="/gallery" className='px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-sky-900 hover:bg-gray-50 transition-colors'>
                        My Gallery
                    </Link>
                    <Link to="/upload" className='px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-sky-900 hover:bg-gray-50 transition-colors'>
                        Upload
                    </Link>
                    <Link to="/search" className='px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-sky-900 hover:bg-gray-50 transition-colors'>
                        Search
                    </Link>
                </div>

                <div className='hidden md:flex md:items-center md:space-x-4'>
                    <Link to="/signup" className='px-3 py-2 text-sm font-medium text-sky-900 hover:text-indigo-800 transition-colors'>
                        Sign Up
                    </Link>
                    <Link to="/login" className='px-3 py-2 text-sm font-medium text-gray-700 hover:text-indigo-600 transition-colors'>
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
