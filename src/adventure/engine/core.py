# src/aventura/engine/core.py
from __future__ import annotations

import copy
from typing import Dict, Any, List, Tuple

from adventure.engine.actions import build_actions

State = Dict[str, Any]
World = Dict[str, Any]


def render_room(state: State, world: World) -> None:
    room = world["rooms"][state["room"]]
    print(f"\n== {room['title']} ==")
    print(room["desc"])

    if room["items"]:
        names = [world["items"][i]["name"] for i in room["items"]]
        print("Ves:", ", ".join(names))


def render_inventory(state: State, world: World) -> None:
    inv = state["inventory"]
    if not inv:
        print("\nInventario: (vacío)\n")
        return
    names = [world["items"][i]["name"] for i in inv]
    print("\nInventario:", ", ".join(names), "\n")


def available_actions(state: State, world: World):
    actions = build_actions()
    return [a for a in actions if a["when"](state, world)]


def navigation_options(state: State, world: World) -> List[Tuple[str, str]]:
    exits = world["rooms"][state["room"]]["exits"]
    return [(f"ir:{k}", f"Ir a {k.replace('_', ' ')}") for k in exits.keys()]


def move(state: State, world: World, exit_key: str) -> None:
    exits = world["rooms"][state["room"]]["exits"]
    if exit_key not in exits:
        print("\nNo puedes ir por ahí.\n")
        return

    # Pequeño “gating” narrativo: si vas al archivo interior, en realidad vas a la puerta (si no está abierto)
    dest = exits[exit_key]
    if dest == "archivo_puerta" and state["flags"]["archivo_abierto"]:
        state["room"] = "archivo"
        return

    state["room"] = dest


def run_console_game(world: World, initial_state: State) -> None:
    world = copy.deepcopy(world)
    state = copy.deepcopy(initial_state)

    while True:
        render_room(state, world)

        nav = navigation_options(state, world)
        acts = available_actions(state, world)

        menu: List[Tuple[str, str]] = []
        menu.append(("inventario", "Ver inventario"))
        menu.append(("mirar", "Mirar alrededor"))
        menu.extend(nav)
        menu.extend([(a["id"], a["label"]) for a in acts])

        print("\nOpciones:")
        for i, (_, label) in enumerate(menu, start=1):
            print(f"{i}. {label}")

        raw = input("\n> ").strip()
        if not raw.isdigit():
            print("\nElige un número.\n")
            continue

        idx = int(raw) - 1
        if idx < 0 or idx >= len(menu):
            print("\nOpción inválida.\n")
            continue

        action_id = menu[idx][0]

        if action_id == "inventario":
            render_inventory(state, world)
            continue

        if action_id == "mirar":
            # Re-render simple
            render_room(state, world)
            continue

        if action_id.startswith("ir:"):
            exit_key = action_id.split(":", 1)[1]
            move(state, world, exit_key)
            continue

        # Ejecutar acción del catálogo
        selected = next((a for a in acts if a["id"] == action_id), None)
        if selected is None:
            print("\nEsa acción no está disponible.\n")
            continue

        selected["do"](state, world)
