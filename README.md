# EDA-bot

EDA-Bot is a full-stack application that serves as a platform for exploring and analyzing data. It features a React frontend built with Vite and a Flask backend, providing an easy-to-use interface for users to interact with data.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Flask backend for handling API requests.
- Fetches data dynamically from the backend.
- Easy to set up and run.

## Technologies Used

- **Frontend**:

  - React
  - Vite
  - TypeScript
  - pnpm

- **Backend**:
  - Flask
  - Python
  - Flask-CORS

## Getting Started

To get started with this project, clone the repository and navigate into the project directory.

```bash
git clone https://github.com/yourusername/eda-bot.git
cd eda-bot
```

## Running the Application

1. **Frontend**:

   - Navigate to the `frontend` directory:
     ```bash
     cd frontend
     ```
   - Install dependencies:
     ```bash
     pnpm install
     ```
   - Start the frontend development server:
     ```bash
     pnpm run dev
     ```

2. **Backend**:
   - Open a new terminal window and navigate to the `backend` directory:
     ```bash
     cd backend
     ```
   - Create and activate a virtual environment (if not already done):
     ```bash
     python -m venv .venv
     # For Windows:
     .venv\Scripts\activate
     # For macOS/Linux:
     source .venv/bin/activate
     ```
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```
   - Run the backend server:
     ```bash
     python app.py
     ```

## Environment Variables

To manage environment variables, create a `.env` file in both the `frontend` and `backend` directories. This ensures that environment-specific configurations are set properly.
