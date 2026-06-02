from src.app import Application
import sys


def main():
    scene_mode = "trees"
    if len(sys.argv) > 1:
        scene_mode = sys.argv[1].lower()

    try:
        app = Application(scene_mode=scene_mode)
    except ValueError:
        print("Invalid scene mode. Use: trees or clouds")
        return

    app.run()


if __name__ == "__main__":
    main()
