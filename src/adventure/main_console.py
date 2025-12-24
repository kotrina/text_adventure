# src/aventura/main_console.py
from adventure.content.world import WORLD, INITIAL_STATE
from adventure.ui.console import start


def main() -> None:
    start(WORLD, INITIAL_STATE)


if __name__ == "__main__":
    main()
