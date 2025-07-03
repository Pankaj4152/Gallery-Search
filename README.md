# Gallery Search AI

**Gallery Search IA** is a modern image storage and management web application powered by AI. It allows users to upload images and later retrieve them using **natural language search queries**.
Built with a powerful **Django + FAISS + BLIP backend** and a polished **React + TailwindCSS + TypeScript** frontend, this application combines fast vector similarity search with elegant UI to offer a seamless experience.

---

## 🚀 Features Overview
- 🔍 **AI-Powered Semantic Search** 
    Use natural language descriptions to find images based on content and context, powered by FAISS vector search.

- 🧠 **Automatic Image Captioning** 
    Automatically generate human-like image descriptions using BLIP and store them for reference or search.

- 📂 **Image Upload & Storage**  
  Easily upload multiple images to your gallery, where they are processed, described, embedded, and stored.

- 🧬 **Vector Similarity Search**  
  Search is performed using sentence-transformers and FAISS, ensuring high-speed and accurate semantic matches.

- 🔐 **Authentication & Authorization**  
  Secure user authentication using **JWT tokens** via Django SimpleJWT.

- 🎨 **Modern UI**  
  Responsive and intuitive UI with animated effects, particle backgrounds, and clean layouts.

- 🖼️ **Personal Image Gallery**  
  Each authenticated user has access to their own collection, including upload and deletion capabilities.

---

## 🖼️ Screenshots

| Signup Page | Gallery Search | Upload Form |
|-------------|----------------|-------------|
| _Add image_ | _Add image_    | _Add image_ |

--- 

## 🛠️ Tech Stack

### Frontend
- React (with Vite)
- TypeScript
- TailwindCSS
- React Hook Form
- Axios
- React Router DOM v7
- Gsap & tsparticles for animations
- Hot Toast for notifications

### Backend
- Django + Django REST Framework
- PostgreSQL
- Celery + Redis for async tasks
- FAISS (Facebook AI Similarity Search)
- BLIP (Bootstrapped Language-Image Pretraining)
- SentenceTransformers (multi-qa-mpnet-base-dot-v1)
- Django SimpleJWT for authentication

---
## Structure

├── frontend/ # React frontend (this project)
│ ├── src/
│ │ ├── pages/ # Main pages (Signup, Login, Gallery)
│ │ ├── components/ # Reusable UI components
│ │ ├── api/ # Axios instance and API service files
│ │ ├── styles/ # Tailwind CSS setup
│ └── public/ # Public assets (favicon, etc.)
├── backend/ # Django backend (served via web & worker)
│ ├── gallery/ # Main app: views, models, serializers
│ ├── users/ # Authentication (signup/login endpoints)
│ ├── media/ # Uploaded image files
│ ├── GallerySearch/ # Django project root
├── docker-compose.yml
├── Dockerfile
└── README.md

---
## Getting Started

### 1. Clone repository

```sh
git clone https://github.com/Pankaj4152/Gallery-Search.git
```

### 2. Environment Configuration
Create a .env file in **frontend** folder and set:
```sh
VITE_API_URL=http://localhost:8000  
```

### 3. Run docker container

```sh
docker-compose up --build
```
or
```sh
docker-compose build
docker-compose up
```

The app will be available at:
Frontend: [http://localhost:5173]
Backend API: [http://localhost:8000]

### 4. Run Frontend server mannualy (for development)
```sh
cd frontend
npm install 
npm run dev
```

## Project Structure

- `src/` — Main source code
- `src/pages/` — Page components (e.g., Signup, Login, Gallery)
- `src/components/` — Reusable UI components
- `src/api/axiosInstance.ts` — Axios instance with JWT support

## Environment Variables

If you need to configure API endpoints or secrets, create a `.env` file in this directory.