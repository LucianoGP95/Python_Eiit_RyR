Goals
- OOP implementation.
- Objetive structure:
    my_tkinter_app/
    │
    ├── main.py               # Main application entry point
    │
    ├── assets/               # Folder for static assets (icons, images, etc.)
    │   └── icon.ico          # Application icon
    │   └── image.png         # Other images
    │
    ├── views/                # Folder for GUI views/screens
    │   └── __init__.py       # Initialization script for the views package
    │   └── main_view.py      # Main application view/screen
    │   └── settings_view.py  # Settings view/screen
    │
    ├── controllers/          # Folder for GUI controllers/logic
    │   └── __init__.py       # Initialization script for the controllers package
    │   └── main_controller.py # Controller for the main view
    │   └── settings_controller.py # Controller for the settings view
    │
    ├── models/               # Folder for data models
    │   └── __init__.py       # Initialization script for the models package
    │   └── user.py           # Example data model (if needed)
    │
    ├── utils/                # Folder for utility functions and modules
    │   └── __init__.py       # Initialization script for the utils package
    │   └── helpers.py        # Utility functions
    │
    ├── db/                   # Folder for database-related code
    │   └── __init__.py       # Initialization script for the db package
    │   └── database.py       # Database connection and operations
    │
    └── requirements.txt      # List of Python dependencies
