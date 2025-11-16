## Spotify Music Discovery Backend

## 📖 About The Project

**Spotify Music Discovery Backend** is a scalable, production-ready REST API service that delivers personalized music recommendations to users. Built with modern backend technologies, this project demonstrates enterprise-level architecture with asynchronous task processing, intelligent caching, user authentication, and comprehensive analytics.

### 🎯 Project Highlights

- ✅ **Backend-Only Architecture** - Pure REST API service ready for any frontend (React, Vue, Angular, Mobile Apps)
- ✅ **Production-Ready** - Fully containerized with Docker Compose for seamless deployment
- ✅ **Scalable Design** - Asynchronous task processing with Celery for handling background jobs
- ✅ **High Performance** - Redis caching layer for lightning-fast response times
- ✅ **Secure** - JWT-based authentication with token refresh and blacklisting
- ✅ **Analytics-Driven** - Track user engagement and trending content
- ✅ **Well-Documented** - Comprehensive API documentation and examples

---

## ✨ Features

### 🔐 Authentication & User Management
- **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- **User Registration & Login** - Complete user lifecycle management
- **Token Refresh** - Automatic token rotation with blacklisting support
- **User Profiles** - Manage music preferences (genres, artists, moods)

### 🎼 Music Recommendations
- **Spotify Integration** - Fetch personalized recommendations using Spotify Web API
- **Preference-Based** - Recommendations based on favorite genres, artists, and moods
- **Async Processing** - Background task execution with Celery workers
- **Smart Caching** - Redis-powered caching for optimized performance
- **Auto-Refresh** - Periodic recommendation updates every 6 hours

### 📊 Analytics & Tracking
- **User Activity Tracking** - Record play, like, and skip interactions
- **Engagement Metrics** - Monitor user activity and preferences
- **Trending Data** - Identify trending genres and artists across users
- **User-Specific Stats** - Personalized engagement summaries

### 🛠️ Developer Features
- **RESTful API** - Clean, intuitive API design following REST principles
- **Rate Limiting** - Protect endpoints with configurable throttling
- **API Versioning** - Support for future API versions
- **Comprehensive Logging** - Detailed logs for debugging and monitoring
- **Unit Tests** - Test suite with pytest and pytest-django

---

## 🏗️ Tech Stack

### **Backend Framework**
- **Django 5.1** - High-level Python web framework
- **Django REST Framework 3.15** - Powerful toolkit for building Web APIs

### **Database & Caching**
- **PostgreSQL 15** - Advanced open-source relational database
- **Redis 7** - In-memory data store for caching and message broker

### **Task Queue**
- **Celery 5.4** - Distributed task queue for async processing
- **Celery Beat** - Periodic task scheduler

### **Authentication**
- **djangorestframework-simplejwt** - JWT authentication for DRF

### **Web Server**
- **Gunicorn** - Python WSGI HTTP Server
- **Nginx** - Reverse proxy and static file serving

### **Containerization**
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration

### **External APIs**
- **Spotify Web API** - Music data and recommendations

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/) (20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (2.0 or higher)
- [Spotify Developer Account](https://developer.spotify.com/dashboard) (for API credentials)

---

### Quick Start

#### 1️⃣ Clone the Repository
```
git clone https://github.com/yourusername/spotify-music-discovery.git
cd spotify-music-discovery
```

#### 2️⃣ Set Up Environment Variables
```
cp .env.example .env
```

Edit the `.env` file and add your Spotify credentials:
```
Django Settings
DJANGO_SECRET_KEY=your-secret-key-change-in-production
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

Database
POSTGRES_DB=musicdb
POSTGRES_USER=musicuser
POSTGRES_PASSWORD=musicpass
POSTGRES_HOST=db
POSTGRES_PORT=5432

Redis
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

Spotify API - Get credentials from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

#### 3️⃣ Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **"Create an App"**
3. Fill in the app name and description
4. Click **"Create"**
5. Copy **Client ID** and **Client Secret**
6. Paste them into your `.env` file

> **Note:** You can leave the Redirect URI field empty for this project.

#### 4️⃣ Build and Start Services
```
docker-compose up --build -d
```

#### 5️⃣ Run Database Migrations
```
docker-compose exec web python manage.py migrate
```

#### 6️⃣ Create a Superuser (Optional)
```
docker-compose exec web python manage.py createsuperuser
```

#### 7️⃣ Verify Installation

Check that all services are running:
```
docker-compose ps
```

You should see 6 services running:
- ✅ `db` (PostgreSQL)
- ✅ `redis` (Redis)
- ✅ `web` (Django)
- ✅ `celery_worker` (Celery Worker)
- ✅ `celery_beat` (Celery Beat)
- ✅ `nginx` (Nginx)

---

### Access the Application

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **API** | `http://localhost/api/` | Main API endpoint |
| 🔧 **Admin Panel** | `http://localhost/admin/` | Django admin interface |
| 📊 **Database** | `localhost:5432` | PostgreSQL database |
| 🗄️ **Redis** | `localhost:6379` | Redis cache |

---

### Test the API

Register a new user:
```
curl -X POST http://localhost/api/auth/register/
-H "Content-Type: application/json"
-d '{
"email": "test@example.com",
"password": "TestPass123!",
"password2": "TestPass123!",
"first_name": "Test",
"last_name": "User",
"favorite_genres": ["rock", "pop"],
"favorite_artists": ["Coldplay"],
"moods": ["energetic"]
}'
```

Login and get JWT token:
```
curl -X POST http://localhost/api/auth/token/
-H "Content-Type: application/json"
-d '{
"email": "test@example.com",
"password": "TestPass123!"
}'
```

---

### Stopping the Application

Stop all services
```
docker-compose down
```

Stop and remove volumes (⚠️ This will delete all data)
```
docker-compose down -v
```

---

### View Logs

View all logs
```
docker-compose logs
```

View specific service logs
```
docker-compose logs web
docker-compose logs celery_worker
```

Follow logs in real-time
```
docker-compose logs -f
```

---

## 🔧 Development Setup

For development with hot-reload:

Start in development mode
```
docker-compose up
```

Run tests
```
docker-compose exec web pytest
```

Access Django shell
```
docker-compose exec web python manage.py shell
```

Create new Django app
```
docker-compose exec web python manage.py startapp myapp
```

---

## 📦 Project Structure After Installation

spotify-music-discovery/
├── 📂 backend/ # Django settings
│ ├── settings.py # Main configuration
│ ├── celery.py # Celery configuration
│ ├── urls.py # Root URL routing
│ └── wsgi.py # WSGI entry point
├── 📂 users/ # User management
│ ├── models.py # User model with preferences
│ ├── serializers.py # User serializers
│ ├── views.py # Authentication endpoints
│ ├── urls.py # User URL routing
│ └── tests.py # User tests
├── 📂 recommendations/ # Recommendations logic
│ ├── models.py # Recommendation model
│ ├── serializers.py # Recommendation serializers
│ ├── views.py # Recommendation endpoints
│ ├── tasks.py # Celery tasks
│ ├── spotify_client.py # Spotify API client
│ ├── urls.py # Recommendation URL routing
│ └── tests.py # Recommendation tests
├── 📂 analytics/ # Analytics tracking
│ ├── models.py # Activity tracking model
│ ├── serializers.py # Analytics serializers
│ ├── views.py # Analytics endpoints
│ └── urls.py # Analytics URL routing
├── 📂 nginx/ # Nginx configuration
│ ├── Dockerfile # Nginx container
│ └── nginx.conf # Nginx settings
├── 📄 docker-compose.yml # Docker services
├── 📄 Dockerfile # Django container
├── 📄 requirements.txt # Python dependencies
├── 📄 .env # Environment variables
├── 📄 .gitignore # Git ignore rules
├── 📄 pytest.ini # Pytest configuration
└── 📄 README.md # This file
