# Student Information System

A full-stack web application for managing student records, academic programs, and college departments. Built with Vue.js frontend and Flask backend with PostgreSQL database.

## Features

-  **Student Management** - Add, edit, delete, and search student records
-  **Program Management** - Manage academic programs and their associations with colleges
-  **College Management** - Organize departments and colleges
-  **Dashboard** - View statistics and insights about students, programs, and colleges
-  **Authentication** - Secure user registration and login with JWT tokens
-  **Search & Filter** - Advanced search and sorting capabilities
-  **Pagination** - Efficient data display with customizable page sizes

## Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v20.19.0 or v22.12.0+)
- **Python** (v3.13)
- **PostgreSQL** (v12+)
- **pip** (Python package manager)
- **npm** (Node package manager)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd student-information-system
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install pipenv
pipenv install
```

#### Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
JWT_SECRET_KEY=your-secret-key-here
```

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd ../frontend
npm install
```

#### Configure API Base URL

The frontend is configured to connect to the backend at `http://127.0.0.1:8000`. If your backend runs on a different URL, update it in `frontend/src/main.js`:

```javascript
axios.defaults.baseURL = "http://127.0.0.1:8000";
```

## Running the Application

### Start the Backend Server

```bash
cd backend
pipenv shell
python app.py
```

The backend server will start on `http://127.0.0.1:8000`

### Start the Frontend Development Server

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`
