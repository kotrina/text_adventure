# Adventure — Interactive Fiction Engine in Python

This project is a small **interactive fiction / text adventure engine** written in Python.

It is designed with one clear goal:

> **Make it easy to build your own text adventure by editing data, not engine code.**

The engine is UI-agnostic (console today, web tomorrow) and separates:
- game logic
- world content
- user interface

You can play the included sample adventure **or create your own** by defining rooms, items and rules.

---

## Features

- Classic text adventure / interactive fiction
- Data-driven world definition (rooms, items, exits)
- Inventory system
- Conditional actions (doors, puzzles, flags)
- Multiple endings
- Clean separation between engine and content
- Ready for future web interface (FastAPI / Flask)

---

## Project Structure

```

adventure/
├─ src/
│  └─ adventure/
│     ├─ main_console.py      # Console entry point
│     ├─ engine/              # Game engine (logic only)
│     │  ├─ core.py
│     │  └─ actions.py
│     ├─ content/             # Your game world lives here
│     │  └─ world.py
│     └─ ui/
│        └─ console.py        # Console interface

````

**Important idea:**  
- `engine/` never contains story content  
- `content/` never contains game logic  

This is what makes the engine reusable.

---

## Requirements

- Python **3.9+**
- No external dependencies

---

## ▶️ Running the game (console)

From the project root:

```bash
PYTHONPATH=src python3 -m adventure.main_console
````

You should see the first room description in the console.

---

## Core Concepts

### 1. World

The game world is defined in:

```
src/adventure/content/world.py
```

It contains two main structures:

```python
WORLD
INITIAL_STATE
```

---

### 2. Rooms

Each room defines:

* title
* description
* items inside
* exits to other rooms

Example:

```python
"despacho": {
    "title": "Despacho",
    "desc": "You are in your office. It's late.",
    "items": ["linterna", "nota"],
    "exits": {"pasillo": "pasillo"},
}
```

---

### 3. Items

Items are defined once and referenced by ID:

```python
"linterna": {
    "name": "Linterna",
    "desc": "An old flashlight. It might still work."
}
```

The **ID** is used internally.
The **name** is shown to the player.

---

### 4. Player State

The player state is a dictionary:

```python
{
    "room": "despacho",
    "inventory": [],
    "flags": {
        "luz": False,
        "archivo_abierto": False
    }
}
```

* `room` → current location
* `inventory` → items carried
* `flags` → anything that changes the world

Flags are the key to puzzles.

---

### 5. Actions

Actions are defined in:

```
src/adventure/engine/actions.py
```

Each action has:

* an ID
* a label shown to the player
* a condition (`when`)
* an effect (`do`)

Example:

```python
{
    "id": "encender_luz",
    "label": "Encender la luz",
    "when": lambda s, w: s["room"] == "sala_electrica",
    "do": lambda s, w: s["flags"].__setitem__("luz", True)
}
```

If the condition is true, the action appears in the menu.

---

## Creating Your Own Adventure

To create your own game:

1. **Copy `world.py`**
2. Redefine:

   * rooms
   * items
   * initial state
3. Adjust or add actions if needed
4. Run the game

You do **not** need to touch the engine unless you want new mechanics.

---

## Philosophy

This engine is intentionally:

* simple
* explicit
* readable

No magic parsers.
No free-text commands.
No hidden state.

Everything is:

> **data → state → consequence**

---

## Future Ideas

* Save / load games
* Web interface (FastAPI)
* Multiple worlds
* Localization
* Graphical assets per room

---



