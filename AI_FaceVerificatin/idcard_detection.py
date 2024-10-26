from ultralytics import YOLO


model = YOLO("yolov8l.pt")

res = model("Frontend\output\idcard.jpg")
res[0].show()
