# load_model.py
import os
from tensorflow.keras.models import load_model

# Đường dẫn tới mô hình đã lưu
model_path = r'D:\DoAnChuyenNganh\vgg16_disease_classifier.h5'

# Tải mô hình đã lưu
if os.path.exists(model_path):
    model = load_model(model_path)
    print("Mô hình đã được tải từ:", model_path)
else:
    raise FileNotFoundError("Mô hình không tồn tại. Vui lòng kiểm tra đường dẫn.")
