# TaskFlow - Enterprise Todo Application

A production-ready enterprise Todo application with FastAPI backend and modern SPA frontend. Works on desktop, tablet, and mobile devices.

![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Mobile](https://img.shields.io/badge/Mobile-PWA-brightgreen)

## Features

### Core Features
- **User Authentication** - JWT-based auth with register/login/forgot password
- **Task Management** - Full CRUD operations (Create, Read, Update, Delete)
- **Task Completion** - Mark tasks as completed with visual feedback
- **Priority Levels** - High, Medium, Low with color-coded badges
- **Due Dates** - Set and track deadlines for tasks
- **Categories** - Organize tasks with custom colored categories
- **Drag & Drop** - Reorder tasks with smooth animations (SortableJS)
- **Search** - Find tasks by title/description
- **Filters** - Filter by status (all/pending/completed), priority, category
- **Pagination** - Efficient loading with paginated task lists
- **Dark Mode** - Toggle between light and dark themes

### Mobile App (PWA)
- **Installable** - Add to home screen like a native app
- **Offline Support** - Works offline (basic functionality)
- **Bottom Navigation** - Easy thumb-friendly navigation
- **Responsive Design** - Optimized for all screen sizes
- **Touch Optimized** - Large tap targets, swipe gestures

### UI/UX Features
- Modern SaaS dashboard design
- Responsive layout (mobile + desktop)
- Smooth animations and transitions
- Toast notifications for feedback
- Confirmation dialogs for destructive actions
- Keyboard shortcuts (N: new task, F: search, Esc: close modals)
- Loading indicators
- Empty state UI

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy ORM, Pydantic |
| Database | SQLite |
| Frontend | HTML5, Tailwind CSS, SortableJS |
| Auth | JWT (python-jose, passlib) |
| PWA | Service Worker, Manifest |

## Project Structure

```
taskflow/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Settings
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models/          # User, Task, Category
│   │   ├── schemas/         # Pydantic validation
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # JWT security
│   └── requirements.txt
├── frontend/
│   ├── index.html           # SPA frontend
│   ├── manifest.json        # PWA manifest
│   └── sw.js                # Service worker for offline support
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── render.yaml
└── README.md
```

## Quick Start

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### 3. Access the Application

Open your browser:
```
http://localhost:8000
```

## Mobile App Installation

### iOS (Safari)
1. Open the app in Safari
2. Tap the Share button
3. Tap "Add to Home Screen"
4. Tap "Add"

### Android (Chrome)
1. Open the app in Chrome
2. Tap the menu (⋮)
3. Tap "Install app" or "Add to Home screen"

The app will appear as a native-like icon on your home screen!

## API Documentation

Once the server is running, access the interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login, returns JWT |
| GET | `/api/auth/me` | Get current user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get tasks (with filters) |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get single task |
| PUT | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |
| PATCH | `/api/tasks/reorder` | Reorder tasks |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories` | Get user categories |
| POST | `/api/categories` | Create category |
| PUT | `/api/categories/{id}` | Update category |
| DELETE | `/api/categories/{id}` | Delete category |

## Example API Usage

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Create Task (with token)
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title": "My Task", "priority": "high", "description": "Important task"}'
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `N` | Open new task modal |
| `F` | Focus search input |
| `Esc` | Close any open modal |

## Deployment

### Render.com (Recommended - Free Tier)
1. Push code to GitHub
2. Connect to Render
3. Deploy automatically!

See `DEPLOYMENT.md` for more options.

## License

MIT License
