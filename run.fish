#!/usr/local/bin/fish
source ./backend/venv/bin/activate.fish
cd ./backend && flask --app main run &
cd ../frontend && npm run dev

