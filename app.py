from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
from tensorflow.keras.models import load_model
from flask_cors import CORS
import secrets

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
CORS(app)  # Cho phép CORS cho tất cả các route

app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


# Model and upload folder paths
model_path = "./vgg16_disease_classifier.h5"
UPLOAD_FOLDER = "./static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model
try:
    model = load_model(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Set model to None if loading fails

# Disease classes and treatments
classes = [
    'Bệnh Bạc Lá', 'Bệnh Cháy Lá', 'Bệnh Đốm Đen', 'Bệnh Đốm Lá',
    'Bệnh Phấn Trắng', 'Bệnh Tảo', 'Bệnh Thán Thư', 'Bệnh Thối Lá', 'Lá Bình Thường'
]

treatments = {
    'Bệnh Bạc Lá': "Phun thuốc trừ nấm chứa đồng và đảm bảo thoát nước tốt.",
    'Bệnh Cháy Lá': "Sử dụng thuốc trừ nấm phù hợp và loại bỏ lá bị nhiễm.",
    'Bệnh Đốm Đen': "Áp dụng hỗn hợp dầu neem và baking soda.",
    'Bệnh Đốm Lá': "Sử dụng thuốc trừ nấm đặc hiệu cho bệnh đốm lá.",
    'Bệnh Phấn Trắng': "Phun thuốc chống nấm có chứa lưu huỳnh hoặc đồng và cải thiện thông gió.",
    'Bệnh Tảo': "Sử dụng thuốc trừ nấm chuyên dụng và loại bỏ các bộ phận bị nhiễm bệnh.",
    'Bệnh Thán Thư': "Phun thuốc trừ nấm có chứa đồng và cải thiện điều kiện canh tác.",
    'Bệnh Thối Lá': "Sử dụng thuốc trừ nấm chuyên dụng và cải thiện thoát nước.",
    'Lá Bình Thường': "Không cần điều trị, tiếp tục chăm sóc bình thường."
}
data_products = [
    {'pro_id': 11 ,'pro_name': 'Phun thuốc trừ nấm chứa đồng và đảm bảo thoát nước tốt.', 'pro_price': 5000},
    {'pro_id': 10 ,'pro_name': 'Sử dụng thuốc trừ nấm phù hợp và loại bỏ lá bị nhiễm.', 'pro_price': 6000},
    {'pro_id': 19 ,'pro_name': 'Áp dụng hỗn hợp dầu neem và baking soda.', 'pro_price': 5500},
    {'pro_id': 18 ,'pro_name': 'Sử dụng thuốc trừ nấm đặc hiệu cho bệnh đốm lá.', 'pro_price': 7000},
    {'pro_id': 16 ,'pro_name': 'Phun thuốc chống nấm có chứa lưu huỳnh hoặc đồng và cải thiện thông gió.', 'pro_price': 6500},
    {'pro_id': 15 ,'pro_name': 'Sử dụng thuốc trừ nấm chuyên dụng và loại bỏ các bộ phận bị nhiễm bệnh.', 'pro_price': 7500},
    {'pro_id': 14 ,'pro_name': 'Phun thuốc trừ nấm có chứa đồng và cải thiện điều kiện canh tác.', 'pro_price': 6800},
    {'pro_id': 13 ,'pro_name': 'Sử dụng thuốc trừ nấm chuyên dụng và cải thiện thoát nước.', 'pro_price': 7000},
    {'pro_id': 12 ,'pro_name': 'Không cần điều trị, tiếp tục chăm sóc bình thường.', 'pro_price': 0}
]

# Image processing function
def process_image(file_path):
    img = load_img(file_path, target_size=(224, 224))
    img = img_to_array(img) / 255.0
    return np.expand_dims(img, axis=0)

# Prediction function
def predict_disease(file_path):
    if model is None:
        return None, None, "Mô hình không được tải. Vui lòng kiểm tra."
    
    # Process image
    img_array = process_image(file_path)
    
    # Predict
    predictions = model.predict(img_array)
    predicted_class = classes[np.argmax(predictions)]
    confidence = np.max(predictions)
    
    # Get treatment recommendation
    recommended_treatment = treatments.get(predicted_class, "Không có phương pháp điều trị cho bệnh này.")
    
    return predicted_class, confidence, recommended_treatment

# Route for main page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('index.html', error='Không có tệp nào được chọn.')

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Predict disease
        predicted_class, confidence, treatment = predict_disease(file_path)

        # Delete file after prediction
        os.remove(file_path)

        return render_template('index.html', filename=filename, predicted_class=predicted_class, confidence=confidence, treatment=treatment)

    return render_template('index.html')

# Route for health check page
@app.route('/health_check', methods=['GET', 'POST'])
def health_check():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return render_template('health_check.html', error='Không có tệp nào được chọn.')

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Predict disease
        predicted_class, confidence, treatment = predict_disease(file_path)

        # Kiểm tra nếu treatment có trong data_products không
        matching_product = next((product for product in data_products if product['pro_name'] == treatment), None)
        print("check matching_product", matching_product)
        # Nếu không tìm thấy sản phẩm trong data_products
        if matching_product is None:
            print("Product not found in data_products.")
            return render_template('health_check.html', filename=filename, predicted_class=predicted_class, confidence=confidence, treatment=treatment, error="Không tìm thấy thuốc cho bệnh này.")
        pro_id = matching_product['pro_id']
        pro_name = matching_product['pro_name']
        pro_price = matching_product['pro_price']
        cart = session.get('cart', [])
        found = False
        for item in cart:
            if item['name'] == pro_name:
                item['quantity'] += 1 
                found = True
                break
        
        if not found:  
            cart.append({
                'name': pro_name,
                'price': pro_price,
                'quantity': 1
            })
        
        session['cart'] = cart  # Cập nhật lại giỏ hàng trong session
        print("Giỏ hàng hiện tại:", cart)  
        #session.pop('cart', None)
        return render_template('health_check.html', filename=filename, predicted_class=predicted_class, confidence=confidence, treatment=treatment)

    return render_template('health_check.html')



@app.route('/sell_medicine')
def sell_medicine():
    return render_template('sell_medicine.html')


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product_name = request.form.get('product_name')
    price_value = float(request.form.get('price_value'))
    
    cart = session.get('cart', [])
    
    for item in cart:
        if item['name'] == product_name:
            item['quantity'] += 1
            break
    else:
        cart.append({
            'id': product_id,
            'name': product_name,
            'price': price_value,
            'quantity': 1
        })
    # Cập nhật lại session
    session['cart'] = cart
    print(">>> check cart:", cart)  
    flash('Sản phẩm đã được thêm vào giỏ hàng!', 'success')
    return redirect(url_for('cart'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    # Giả sử giỏ hàng được lưu trong session
    cart = session.get('cart', [])
    if request.method == 'POST':  # Khi người dùng nhấn thanh toán
        # Xử lý thanh toán (giả lập thanh toán thành công)
        session['cart'] = []  # Làm trống giỏ hàng
        flash('Thanh toán thành công!', 'success')  # Hiển thị thông báo thành công
        return redirect(url_for('cart'))  # Reload trang giỏ hàng

    # Tính tổng giá trị giỏ hàng
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    
    # In ra để kiểm tra giá trị của total_price
    print("Total Price:", total_price)
    return render_template('cart.html', cart=cart, total_price=total_price)



# Route để cập nhật giỏ hàng
@app.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form.get('quantity'))
    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = quantity
            break

    session['cart'] = cart
    # Tính toán lại tổng giá
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    
    # Trả về dữ liệu dưới dạng JSON
    return jsonify(success=True, total_price=total_price)

# Route để xóa sản phẩm khỏi giỏ
@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    if 'cart' in session:
        data = request.get_json()
        product_name = data.get('productName')

        # Lọc bỏ sản phẩm khỏi session['cart']
        session['cart'] = [item for item in session['cart'] if item['name'] != product_name]

        return jsonify({"message": "Product removed from session['cart']."}), 200
    else:
        return jsonify({"message": "Cart is empty."}), 400


@app.route('/payment', methods=['POST'])
def payment():
    # Giả sử bạn xử lý thanh toán ở đây
    # Xóa giỏ hàng trong session sau khi thanh toán thành công
    session['cart'] = []  # Giỏ hàng được làm trống
    flash('Thanh toán thành công!', 'success')  # Hiển thị thông báo thành công
    return redirect(url_for('cart'))  # Reload trang giỏ hàng


# Chạy ứng dụng Flask
if __name__ == '__main__':
    app.run(debug=True)
