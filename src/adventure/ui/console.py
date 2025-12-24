# src/aventura/ui/console.py
from __future__ import annotations

from typing import Dict, Any

from adventure.engine.core import run_console_game

State = Dict[str, Any]
World = Dict[str, Any]


def start(world: World, initial_state: State) -> None:
    run_console_game(world, initial_state)
