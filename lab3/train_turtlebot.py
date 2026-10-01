from pathlib import Path
from ultralytics import YOLO

def main():
    folder = Path(__file__).resolve().parent
    model = YOLO(str(folder / "runs/turtlebot-4/weights/best.pt"))

    results = model.predict(
        source=0,
        show=True,
        stream=True,
        conf=0.5
    )

    for result in results:
        pass

if __name__ == "__main__":
    main()