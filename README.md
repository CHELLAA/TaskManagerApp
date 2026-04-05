# TaskFlow - Enterprise Todo Application

A production-ready enterprise Todo application with FastAPI backend and modern SPA frontend.

![TaskFlow](https://img.shields.io/badge/TaskFlow-Todo%20App-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)

## Features

### Core Features
- **User Authentication** - JWT-based auth with register/login
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

## Project Structure

```
taskflow/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Settings
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── models/           # User, Task, Category
│   │   ├── schemas/          # Pydantic validation
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   └── utils/            # JWT security
│   └── requirements.txt
├── frontend/
│   └── index.html            # SPA frontend
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
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

Open your browser and navigate to:
```
http://localhost:8000
```

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

## Features in Detail

### Task Properties
- **Title** (required): Task name
- **Description** (optional): Detailed description
- **Priority**: Low (green), Medium (amber), High (red)
- **Due Date**: Date and time picker
- **Category**: Optional categorization
- **Completed**: Boolean completion status

### Filter Options
- **All Tasks**: View all tasks
- **Pending**: Tasks not yet completed
- **Completed**: Finished tasks
- **By Priority**: High, Medium, Low
- **By Category**: User-defined categories
- **Search**: Text search in titles and descriptions

## Development

### Running in Development
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Database
The SQLite database is automatically created on first run. It's stored as `todos.db` in the backend directory.

## License

MIT License
