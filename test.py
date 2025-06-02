from ultralytics import YOLO

model = YOLO('yolov8s-cls.pt')  # Базова модель

model.train(
    data='C:/Users/Mary/OneDrive/Робочий стіл/dataset',  # твій шлях
    epochs=30,
    imgsz=224,
    batch=32,
    name='wedding_dress_cls',
    project='training_logs',
    val=True,
    device='cpu'  # або '0', якщо є GPU
)
