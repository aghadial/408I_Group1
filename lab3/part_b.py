from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")
    results = model.predict(source=0, show=True, stream=True)

    for result in results:
        pass

if __name__ == "__main__":
    main()