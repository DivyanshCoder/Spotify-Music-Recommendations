# Spotify Music Discovery Backend

A scalable Django REST API backend service that provides personalized music recommendations using the Spotify Web API. Features include user profile management, asynchronous task processing with Celery, Redis caching, and comprehensive analytics.

## 🚀 Features

- **User Profile Management**: Create and manage user preferences (genres, artists, moods)
- **Spotify Integration**: Fetch personalized recommendations from Spotify Web API
- **Asynchronous Processing**: Background tasks using Celery for recommendation refresh
- **Redis Caching**: Fast response times with intelligent caching layer
- **Analytics & Reporting**: Track user engagement and trending content
- **Rate Limiting**: Protect API endpoints with configurable throttling
- **Dockerized**: Complete Docker setup with PostgreSQL, Redis, Celery, and Nginx
- **RESTful API**: Clean, well-documented API endpoints

## 📋 Prerequisites

- Docker and Docker Compose
- Spotify Developer Account ([Get credentials here](https://developer.spotify.com/dashboard))

## 🛠️ Setup & Installation

### 1. Clone the Repository

