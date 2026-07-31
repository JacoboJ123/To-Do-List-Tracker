# To-Do List Tracker

A command-line to-do list and habit tracker built with Python and SQLite. Started as a simple in-memory to-do list and evolved into a persistent, database-backed app with streak tracking for recurring tasks.

## Features

- **Add tasks** with a title and an optional description
- **View tasks** — only shows fields that actually have a value (no clutter from empty descriptions)
- **Edit tasks** — update the title, the description, or both; leave a field blank to skip changing it
- **Delete tasks**
- **Mark tasks complete** — builds a daily streak:
  - First time completing a task → streak starts at 1
  - Completing again the next day → streak increases
  - Completing again the same day → no change (already counted)
  - Missing a day → streak resets to 1 on the next completion
- Optional due date (`enddate`) field for tracking when a task needs to be done by

## Tech Stack

- **Python 3** — core application logic
- **SQLite3** (via Python's built-in `sqlite3` module) — persistent local storage, no external database required

## Project Structure

```
To-Do-List-Tracker/
├── main.py          # CLI menu and all task operations (add, view, edit, delete, complete)
├── db_setup.py       # Creates the SQLite database and tasks table if they don't exist
├── tasks.db          # SQLite database file (created automatically on first run, not tracked in git)
└── .gitignore
```

## Database Schema

```sql
CREATE TABLE tasks(
    task_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    enddate NUMERIC,
    streak INTEGER DEFAULT 0,
    last_completed TEXT
);
```

## Getting Started

### Prerequisites
- Python 3.8 or higher

### Installation

1. Clone the repo:
   ```
   git clone https://github.com/JacoboJ123/To-Do-List-Tracker.git
   cd To-Do-List-Tracker
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1      # Windows PowerShell
   source .venv/bin/activate       # macOS/Linux
   ```

3. Run the app:
   ```
   python main.py
   ```

No external dependencies are required — everything runs on Python's standard library.

## Usage

Once running, you'll see a menu with options:

```
'A' to add a new task
'V' to view your current tasks
'E' to edit a task
'C' to mark a task complete
'D' to delete a task
'Q' to quit.
```

Follow the prompts to manage your tasks. The database file (`tasks.db`) is created automatically in the project folder the first time you run the app.

## What I Learned / Built

This project started as a simple in-memory Python script that saved tasks to a plain text file. I rebuilt it to use SQLite for real, persistent storage, which involved:

- Designing a relational schema from scratch (primary keys, nullable vs. required columns, sensible defaults)
- Writing parameterized SQL queries to prevent SQL injection
- Managing database connections safely with `try`/`except`/`finally`
- Implementing date-comparison logic in Python to track daily streaks
- Building a dynamic SQL `UPDATE` statement that only modifies the fields the user actually changed

## Future Improvements

- Display `enddate` in the task view and flag overdue tasks
- Add sorting/filtering (e.g., by streak length or due date)
- Add unit tests
- Create frontend in React