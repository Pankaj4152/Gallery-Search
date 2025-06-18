import { Link } from 'react-router-dom';

export function Navbar() {
    return (
        <nav>
    <div>
        <Link to="/">GalleryAI</Link>
        <button type="button">
            <span></span>
        </button>
        <div id="navbarNav">
            <ul>
                <li>
                    <Link to="/gallery">My Gallery</Link>
                </li>
                <li>
                    <Link to="/upload">Upload</Link>
                </li>
                <li>
                    <Link to="/search">Search</Link>
                </li>
                <li>
                    <Link to="/signup">Sign Up</Link>
                </li>
                <li>
                    <Link to="/login">Login</Link>
                </li>
                <li>
                    <button onClick={logout}>Logout</button>
                </li>
            </ul>
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
