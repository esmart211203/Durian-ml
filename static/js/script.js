// Hiển thị ảnh khi người dùng chọn
function showImage(event) {
    var fileInput = event.target;
    var file = fileInput.files[0];
    var reader = new FileReader();

    // Khi file được đọc thành công, hiển thị ảnh
    reader.onload = function(e) {
        // Hiển thị ảnh đã chọn trong ô
        var image = document.getElementById('selected-image');
        image.src = e.target.result;
        image.style.display = 'block';  // Hiển thị ảnh

        // Ẩn thông báo ban đầu khi có ảnh
        document.getElementById('file-name').style.display = 'none';
        
        // Hiển thị nút "Tải ảnh khác"
        document.getElementById('new-image-button').style.display = 'block';
    };

    if (file) {
        reader.readAsDataURL(file);  // Đọc file dưới dạng URL
    }
}

// Xử lý khi nhấn nút "Tải Ảnh Khác"
function resetImage() {
    // Đặt lại ô chọn ảnh
    var fileInput = document.querySelector('.upload-input');
    fileInput.value = ''; // Xóa lựa chọn file

    // Ẩn ảnh đã chọn trong ô và hiển thị lại thông báo
    var image = document.getElementById('selected-image');
    image.src = '';
    image.style.display = 'none';
    document.getElementById('file-name').style.display = 'block';
    
    // Ẩn nút "Tải Ảnh Khác"
    document.getElementById('new-image-button').style.display = 'none';
}

// Lắng nghe sự kiện click vào các mục trong nav
const categoryLinks = document.querySelectorAll('.category-nav a');
const productCards = document.querySelectorAll('.product-card');

// Hàm ẩn/hiện sản phẩm theo danh mục
function filterProducts(category) {
    productCards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block'; // Hiển thị sản phẩm
        } else {
            card.style.display = 'none'; // Ẩn sản phẩm
        }
    });
}

// Xử lý khi click vào các mục trong danh mục
categoryLinks.forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault(); // Ngừng chuyển hướng mặc định
        const category = this.dataset.category;

        // Cập nhật lớp 'active' cho các link
        categoryLinks.forEach(link => link.classList.remove('active'));
        this.classList.add('active');

        // Lọc sản phẩm theo loại
        filterProducts(category);
    });
});


function addToCart(productName, productPrice, productQuantity) {
    fetch('/add_to_cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: productName,
            price: productPrice,
            quantity: productQuantity
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("HTTP error " + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(data.message);  // Hiển thị thông báo thành công từ server
        } else {
            alert("Có lỗi xảy ra: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Đã xảy ra lỗi khi thêm sản phẩm vào giỏ hàng.");
    });
}

// Kiểm tra xem có thông báo thanh toán thành công không và hiển thị
window.onload = function () {
    // Kiểm tra nếu có thông báo flash 'Thanh toán thành công'
    if (document.getElementById('payment-success')) {
        const successMessage = document.getElementById('payment-success');
        successMessage.style.display = 'block';  // Hiển thị thông báo
        setTimeout(function () {
            successMessage.style.display = 'none';  // Ẩn thông báo sau 3 giây
        }, 3000);
    }

    // Xử lý sự kiện submit form thanh toán
    const checkoutForm = document.getElementById('checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function (e) {
            // Ngăn không cho form submit mặc định
            e.preventDefault();

            // Gửi AJAX request hoặc chỉ đơn giản là thông báo thanh toán thành công
            setTimeout(function () {
                // Sau khi thanh toán thành công, hiển thị thông báo và reload trang
                window.location.reload();  // Tự động reload lại giỏ hàng
            }, 500);
        });
    }
}

function addToCart(productName, price) {
    // Get the current cart from localStorage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // Check if the product is already in the cart
    let productIndex = cart.findIndex(item => item.name === productName);

    if (productIndex !== -1) {
        // If the product is in the cart, increase its quantity
        cart[productIndex].quantity += 1;
    } else {
        // If the product is not in the cart, add it
        cart.push({
            name: productName,
            price: price,
            quantity: 1
        });
    }

    // Save the updated cart back to localStorage
    localStorage.setItem("cart", JSON.stringify(cart));

    // Show custom notification
    showNotification("Sản phẩm đã được thêm vào giỏ hàng!");
    
    // Update cart display (if you have a function for this)
    updateCart();
}

function showNotification(message) {
    const notification = document.getElementById("cart-notification");
    const cartMessage = document.getElementById("cart-message");
    
    // Set the message and show the notification
    cartMessage.innerText = message;
    notification.style.display = "block";
    
    // Optionally, hide the notification after a few seconds
    setTimeout(hideNotification, 3000); // hides after 3 seconds
}

function hideNotification() {
    document.getElementById("cart-notification").style.display = "none";
}


function updateCart() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let cartTableBody = document.querySelector(".cart-table tbody");

    // Xóa tất cả các dòng hiện tại trong bảng giỏ hàng
    cartTableBody.innerHTML = "";

    // Duyệt qua các sản phẩm trong giỏ và hiển thị chúng
    cart.forEach(function(item) {
        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.price}đ</td>
            <td><input type="number" class="quantity" value="${item.quantity}" min="1" max="10" data-product-name="${item.name}"></td>
            <td>${item.price * item.quantity}đ</td>
            <td><button class="remove-btn" data-product-name="${item.name}">Xóa</button></td>
        `;

        cartTableBody.appendChild(row);
    });
}

// Gọi hàm updateCart khi trang được tải hoặc khi giỏ hàng thay đổi
document.addEventListener("DOMContentLoaded", function() {
    updateCart();
});

// Xử lý thay đổi số lượng
document.addEventListener("change", function(event) {
    if (event.target.classList.contains("quantity")) {
        let productName = event.target.getAttribute("data-product-name");
        let newQuantity = event.target.value;

        // Lấy giỏ hàng và cập nhật số lượng
        let cart = JSON.parse(localStorage.getItem("cart")) || [];
        let productIndex = cart.findIndex(item => item.name === productName);

        if (productIndex !== -1) {
            cart[productIndex].quantity = newQuantity;
        }

        // Lưu lại giỏ hàng
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCart(); // Cập nhật lại giỏ hàng trên giao diện
    }
});

// Xử lý xóa sản phẩm
document.addEventListener("click", function(event) {
    if (event.target.classList.contains("remove-btn")) {
        let productName = event.target.getAttribute("data-product-name");
        let cart = JSON.parse(localStorage.getItem("cart")) || [];
        cart = cart.filter(item => item.name !== productName);
        localStorage.setItem("cart", JSON.stringify(cart));
        updateCart(); 
        fetch('/remove-from-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ productName: productName })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});



function updateCart() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let cartTableBody = document.querySelector(".cart-table tbody");
    let totalPrice = 0;

    // Xóa tất cả các dòng hiện tại trong bảng giỏ hàng
    cartTableBody.innerHTML = "";

    // Duyệt qua các sản phẩm trong giỏ và hiển thị chúng
    cart.forEach(function(item) {
        let row = document.createElement("tr");

        let totalItemPrice = item.price * item.quantity;
        totalPrice += totalItemPrice;

        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.price}đ</td>
            <td><input type="number" class="quantity" value="${item.quantity}" min="1" max="10" data-product-name="${item.name}"></td>
            <td>${totalItemPrice}đ</td>
            <td><button class="remove-btn" data-product-name="${item.name}">Xóa</button></td>
        `;

        cartTableBody.appendChild(row);
    });

    // Cập nhật tổng giá
    document.getElementById("total-price").innerText = totalPrice + "đ";
}

