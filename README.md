# 🖱️ Gaming Mouse Catalog & Shape Arena

A full-stack web application designed for gamers and hardware enthusiasts to explore, filter, and visually compare gaming mice. The project features an automated data pipeline that syncs daily with external APIs to keep the catalog up to date.

## ✨ Features

* **Extensive Catalog**: Browse hundreds of gaming mice with detailed specifications (weight, dimensions, sensors).
* **Advanced Filtering & Sorting**: Filter mice by brand, sensor type, weight range, and length. Sort results dynamically.
* **⚔️ Shape Comparison Arena**: 
    * Visually compare multiple mice shapes using high-quality SVG overlays (Top & Side views).
    * Align mice by Front (fingertips), Center (sensor), or Back (palm) to see exactly how they differ.
* **🧠 Smart Search**: Tokenized search engine with keyboard navigation support for quickly finding and adding mice to the arena.
* **🤖 Automated Data Sync**: A background Python scheduler runs daily at 00:00 AM (Jerusalem Time) to scrape and update the SQLite database with the latest market data, ensuring a "single source of truth".

## 🛠️ Tech Stack

**Frontend:**
* Vue.js 3 (Composition API)
* Vite
* Vue Router
* Pure CSS (Responsive & Modern UI)

**Backend:**
* Python 3
* Flask & Flask-CORS (RESTful API)
* SQLite3 (Database with `Row` factory for dict-like cursor access)
* APScheduler (Automated background jobs)
* Requests (API Scraping)

## 📁 Project Structure

```text
├── backend/
│   ├── app.py           # Flask server entry point & API routes
│   ├── database.py      # SQLite connection & queries (Separation of Concerns)
│   ├── scraper.py       # API fetching & data processing logic
│   └── mice_catalog.db  # Auto-generated SQLite database
├── frontend/
│   ├── src/             # Vue 3 source code (Components, Views, Router)
│   ├── index.html       
│   └── package.json     
├── start_project.bat    # Windows automation script for running the entire stack
└── README.md

🚀 Getting Started
Prerequisites
Node.js (v16+)

Python (3.9+)

1. Installation
Clone the repository:

Bash
git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
cd YourRepoName
Setup Frontend:

Bash
cd frontend
npm install
cd ..
Setup Backend (Virtual Environment):

Bash
cd backend
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install Flask flask-cors requests APScheduler
cd ..
2. Running the Application (Windows)
For Windows users, simply double-click the start_project.bat file located in the root directory. This script will automatically:

Run the scraper inside the virtual environment to fetch the initial data.

Start the Flask backend server.

Start the Vue Vite development server.

Manual Run (Mac/Linux/Windows)
If you prefer running it manually:

Terminal 1 (Backend):

Bash
cd backend
# Make sure your venv is activated!
python scraper.py  # Run once to populate the database
python app.py      # Start the Flask server
Terminal 2 (Frontend):

Bash
cd frontend
npm run dev
Open your browser and navigate to http://localhost:5173/.

👨‍💻 Author
Created by Ori Nave.
