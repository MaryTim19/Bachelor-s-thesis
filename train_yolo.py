from ultralytics import YOLO
import os
import shutil

dataset_path = 'C:/Users/Mary/OneDrive/Робочий стіл/dataset'
# === Завантаження моделі YOLOv8s для класифікації ===
model = YOLO('yolov8s-cls.pt')

#model.train(
  #  data=dataset_path,
   # epochs=11,
    #imgsz=224,
    #project='training_logs',
    #name='wedding_dress_cls',
    #pretrained=True,
    #val=True,
    #batch=32,
   # device='cpu'  # 'cpu' або 0 для GPU
#)

# === Збереження найкращої моделі в папку models/ ===
output_path = 'training_logs/wedding_dress_cls3/weights/best.pt'
destination = 'models/best.pt'
os.makedirs('models', exist_ok=True)
shutil.copy(output_path, destination)

print(f"\n✅ Навчання завершено. Модель збережено як {destination}")
