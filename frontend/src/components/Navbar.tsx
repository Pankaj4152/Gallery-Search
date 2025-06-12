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
                {/* User authentication pending
                <li className="nav-item d-flex align-items-center">
                    {% if user.is_authenticated %}
                        <span className="me-2">Welcome, <strong>{{ user.username }}</strong></span>
                        <form method="post" action="{% url 'logout' %}" style="display:inline;">
                            {% csrf_token %}
                            <button type="submit" className="btn btn-outline-danger btn-sm ms-2">Logout</button>
                        </form>
                    {% else %}
                        <a href="{% url 'login' %}" className="btn btn-outline-primary btn-sm me-2">Login</a>
                        <a href="{% url 'signup' %}" className="btn btn-primary btn-sm">Sign Up</a>
                    {% endif %}
                </li>
                */} 
            </ul>
        </div>
    </div>
</nav>
)
}