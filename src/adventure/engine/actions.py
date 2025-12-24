# src/aventura/engine/actions.py
from __future__ import annotations

from typing import Callable, Dict, List, Any


State = Dict[str, Any]
World = Dict[str, Any]

Action = Dict[str, Any]  # id, label, when, do


def take_item(state: State, world: World, item_id: str) -> None:
    room = state["room"]
    items_in_room: List[str] = world["rooms"][room]["items"]
    if item_id in items_in_room:
        items_in_room.remove(item_id)
        state["inventory"].append(item_id)
        print(f"\nHas cogido: {world['items'][item_id]['name']}\n")
    else:
        print("\nNo ves ese objeto aquí.\n")


def abrir_caja_fuerte(state: State, world: World) -> None:
    # Si el papel está aún en la sala, lo “encuentras” al interactuar
    if "papel_codigo" in world["rooms"]["archivo"]["items"]:
        world["rooms"]["archivo"]["items"].remove("papel_codigo")
        state["inventory"].append("papel_codigo")
        print("\nEncuentras un papel con un código: 314.\n")

    intento = input("Introduce el código (3 dígitos): ").strip()
    state["flags"]["intentos_caja"] += 1

    if intento == "314":
        state["flags"]["caja_abierta"] = True
        if "llave_final" not in state["inventory"]:
            state["inventory"].append("llave_final")
        print("\nLa caja se abre. Dentro hay una llave.\n")
    else:
        print("\nNo encaja. El dial hace un ‘clac’ desagradable.\n")
        if state["flags"]["intentos_caja"] >= 3:
            print("Suena una alarma. Fin del juego.\n")
            raise SystemExit(0)


def ganar() -> None:
    print("\nAbres la puerta. Aire frío. Libertad.\n¡Has ganado!\n")
    raise SystemExit(0)


def build_actions() -> List[Action]:
    # Nota: usamos lambdas; luego, si quieres, lo pasamos a funciones con nombre.
    return [
        {
            "id": "leer_nota",
            "label": "Leer la nota",
            "when": lambda s, w: (
                s["room"] == "despacho"
                and ("nota" in w["rooms"]["despacho"]["items"] or "nota" in s["inventory"])
            ),
            "do": lambda s, w: print("\n" + w["items"]["nota"]["desc"] + "\n"),
        },
        {
            "id": "coger_linterna",
            "label": "Coger la linterna",
            "when": lambda s, w: s["room"] == "despacho" and "linterna" in w["rooms"]["despacho"]["items"],
            "do": lambda s, w: take_item(s, w, "linterna"),
        },
        {
            "id": "coger_nota",
            "label": "Coger la nota",
            "when": lambda s, w: s["room"] == "despacho" and "nota" in w["rooms"]["despacho"]["items"],
            "do": lambda s, w: take_item(s, w, "nota"),
        },
        {
            "id": "poner_pilas",
            "label": "Poner pilas a la linterna",
            "when": lambda s, w: ("linterna" in s["inventory"])
            and ("pilas" in s["inventory"])
            and (not s["flags"]["linterna_funciona"]),
            "do": lambda s, w: (
                s["flags"].__setitem__("linterna_funciona", True),
                s["inventory"].remove("pilas"),
                print("\nLa linterna cobra vida.\n"),
            ),
        },
        {
            "id": "abrir_cajon",
            "label": "Abrir el cajón del escritorio",
            "when": lambda s, w: s["room"] == "despacho"
            and (s["flags"]["luz"] or s["flags"]["linterna_funciona"])
            and ("tarjeta" not in s["inventory"]),
            "do": lambda s, w: (
                s["inventory"].append("tarjeta"),
                print("\nEncuentras una tarjeta de acceso.\n"),
            ),
        },
        {
            "id": "coger_pilas",
            "label": "Coger las pilas",
            "when": lambda s, w: s["room"] == "sala_electrica" and "pilas" in w["rooms"]["sala_electrica"]["items"],
            "do": lambda s, w: take_item(s, w, "pilas"),
        },
        {
            "id": "encender_luz",
            "label": "Encender la luz del edificio",
            "when": lambda s, w: s["room"] == "sala_electrica" and (not s["flags"]["luz"]),
            "do": lambda s, w: (
                s["flags"].__setitem__("luz", True),
                print("\nLas luces se encienden con un zumbido.\n"),
            ),
        },
        {
            "id": "usar_tarjeta_archivo",
            "label": "Usar la tarjeta en el lector",
            "when": lambda s, w: s["room"] == "archivo_puerta"
            and s["flags"]["luz"]
            and ("tarjeta" in s["inventory"])
            and (not s["flags"]["archivo_abierto"]),
            "do": lambda s, w: (
                s["flags"].__setitem__("archivo_abierto", True),
                s.__setitem__("room", "archivo"),
                print("\n*BIP* La puerta se abre. Entras al Archivo.\n"),
            ),
        },
        {
            "id": "abrir_caja",
            "label": "Abrir la caja fuerte (código)",
            "when": lambda s, w: s["room"] == "archivo" and (not s["flags"]["caja_abierta"]),
            "do": lambda s, w: abrir_caja_fuerte(s, w),
        },
        {
            "id": "usar_llave_salida",
            "label": "Usar la llave en la puerta de salida",
            "when": lambda s, w: s["room"] == "salida" and ("llave_final" in s["inventory"]),
            "do": lambda s, w: ganar(),
        },
    ]
