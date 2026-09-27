# Lemmings — Python Project

A command-line Python simulation inspired by the classic **Lemmings** game, created as a Computer Science school project.

The project models a cave as a 2D grid and simulates lemmings moving through it. Lemmings fall when there is free space below them, move horizontally when supported, reverse direction when blocked, and leave the simulation when they reach the exit.

## What the project demonstrates

- Object-oriented programming with separate game, lemming, and cell responsibilities
- Parsing a text file into a 2D map
- Grid-based movement and collision logic
- State management for multiple moving entities
- Algorithmic problem solving
- Command-line interaction and game-loop logic

## How it works

The map is loaded from `grotte.txt`.

Terrain symbols:

- `#` — wall
- space — free cell
- `O` — exit
- `>` / `<` — lemming moving right or left

During the simulation:

- press `l` to add a lemming
- press **Enter** to advance one turn
- press `q` to quit and display the game statistics

## Run

Requirements:

- Python 3.10+ recommended
- No third-party packages required

Clone the repository and run:

```bash
python lemmings.py
```

## Project structure

- `lemmings.py` — cleaned, portable version of the simulation
- `grotte.txt` — sample cave map
- `Project NSI - Lemmings version final.py` — original final school-project version
- `Projet NSI - Lemmings.pdf` — original project documentation
- other Python files — earlier iterations and working drafts

## Notes

The repository intentionally keeps the original school-project files alongside the cleaned portfolio version so the development process remains visible.
