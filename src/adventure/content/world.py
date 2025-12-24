# src/aventura/content/world.py

WORLD = {
    "start_room": "despacho",
    "rooms": {
        "despacho": {
            "title": "Despacho",
            "desc": "Estás en tu despacho. Es tarde. En la mesa hay una linterna vieja y una nota doblada.",
            "items": ["linterna", "nota"],
            "exits": {"pasillo": "pasillo"},
        },
        "pasillo": {
            "title": "Pasillo",
            "desc": "Un pasillo largo con dos puertas: 'Archivo' y 'Sala eléctrica'. Al fondo, la salida.",
            "items": [],
            "exits": {
                "despacho": "despacho",
                "archivo_puerta": "archivo_puerta",
                "sala_electrica": "sala_electrica",
                "salida": "salida",
            },
        },
        "archivo_puerta": {
            "title": "Archivo (puerta)",
            "desc": "Puerta con lector de tarjeta. Está apagado.",
            "items": [],
            "exits": {"pasillo": "pasillo"},
        },
        "sala_electrica": {
            "title": "Sala eléctrica",
            "desc": "Un cuarto con un cuadro eléctrico y varias cajas polvorientas.",
            "items": ["pilas"],
            "exits": {"pasillo": "pasillo"},
        },
        "archivo": {
            "title": "Archivo (interior)",
            "desc": "Estanterías, polvo, y una caja fuerte pequeña con dial.",
            "items": ["papel_codigo"],
            "exits": {"pasillo": "pasillo"},
        },
        "salida": {
            "title": "Salida",
            "desc": "Una puerta de salida con cerradura. Si tienes la llave, te vas. Si no, te quedas con la noche.",
            "items": [],
            "exits": {"pasillo": "pasillo"},
        },
    },
    "items": {
        "linterna": {"name": "Linterna", "desc": "Una linterna vieja. No sabes si funciona."},
        "nota": {"name": "Nota", "desc": "“Si vas al Archivo, primero enciende la luz. La tarjeta no funciona a oscuras.”"},
        "pilas": {"name": "Pilas", "desc": "Un par de pilas AA. Parecen nuevas."},
        "tarjeta": {"name": "Tarjeta", "desc": "Tarjeta de acceso del edificio. Huele a burocracia."},
        "papel_codigo": {"name": "Papel con código", "desc": "Un papel doblado: “314”. También pone: “círculos, círculos…”"},
        "llave_final": {"name": "Llave", "desc": "Una llave metálica. Tiene pinta de abrir la salida."},
    },
}

INITIAL_STATE = {
    "room": WORLD["start_room"],
    "inventory": [],
    "flags": {
        "luz": False,
        "linterna_funciona": False,
        "archivo_abierto": False,
        "caja_abierta": False,
        "intentos_caja": 0,
    },
}
