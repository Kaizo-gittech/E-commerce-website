CREATE TABLE IF NOT EXISTS sellers (
    seller_id   INT AUTO_INCREMENT PRIMARY KEY,
    shop_name   VARCHAR(150) NOT NULL,
    owner_name  VARCHAR(150) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    phone       VARCHAR(20)  NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    gst_no      VARCHAR(50),
    pan_no      VARCHAR(50),
    address     VARCHAR(255),
    city        VARCHAR(100),
    state       VARCHAR(100),
    pincode     VARCHAR(10),
    category    VARCHAR(100),
    status      ENUM('Pending', 'Approved', 'Rejected', 'Suspended') NOT NULL DEFAULT 'Pending',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admins (
    admin_id    INT AUTO_INCREMENT PRIMARY KEY,
    admin_name  VARCHAR(150) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(50) DEFAULT 'admin'
);

ALTER TABLE sellers
ADD COLUMN shop_logo VARCHAR(255) NULL,
ADD COLUMN gst_certificate VARCHAR(255) NULL,
ADD COLUMN pan_document VARCHAR(255) NULL,
ADD COLUMN product_image_1 VARCHAR(255) NULL,
ADD COLUMN product_image_2 VARCHAR(255) NULL,
ADD COLUMN product_image_3 VARCHAR(255) NULL;


CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    razorpay_order_id VARCHAR(100) NOT NULL,
    razorpay_payment_id VARCHAR(100) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'Paid',
    shipping_status VARCHAR(30) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    seller_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,

    FOREIGN KEY(order_id)
    REFERENCES orders(id),

    FOREIGN KEY(product_id)
    REFERENCES products(product_id),

    FOREIGN KEY(seller_id)
    REFERENCES sellers(seller_id)
);

CREATE TABLE orders(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    razorpay_order_id VARCHAR(100) NOT NULL,
    razorpay_payment_id VARCHAR(100) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'Paid',
    shipping_status VARCHAR(30) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
    REFERENCES users(user_id)
);

ALTER TABLE orders
ADD COLUMN shipping_address TEXT,
ADD COLUMN phone VARCHAR(20);