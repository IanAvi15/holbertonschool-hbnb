#!/usr/bin/python3
"""Entry point for running the HBnB Flask application."""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
