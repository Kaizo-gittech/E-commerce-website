import razorpay
import os
import random
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash,
    url_for,
    jsonify
)

from flask import url_for
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
import os
from werkzeug.utils import secure_filename
from database import mysql
from mail import mail, send_seller_status_email
import config

client = razorpay.Client(
    auth=(
        config.RAZORPAY_KEY_ID,
        config.RAZORPAY_KEY_SECRET
    )
)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder="admin",
    static_folder="static"
)

print("Template folder:", app.template_folder)

UPLOAD_FOLDER = "static/uploads"

SHOP_LOGO_FOLDER = os.path.join(UPLOAD_FOLDER, "shop_logos")
GST_FOLDER = os.path.join(UPLOAD_FOLDER, "gst")
PAN_FOLDER = os.path.join(UPLOAD_FOLDER, "pan")
PRODUCT_FOLDER = os.path.join(UPLOAD_FOLDER, "products")

os.makedirs(SHOP_LOGO_FOLDER, exist_ok=True)
os.makedirs(GST_FOLDER, exist_ok=True)
os.makedirs(PAN_FOLDER, exist_ok=True)
os.makedirs(PRODUCT_FOLDER, exist_ok=True)

app.secret_key = config.SECRET_KEY

app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB

# --- Mail config ---
app.config["MAIL_SERVER"] = config.MAIL_SERVER
app.config["MAIL_PORT"] = config.MAIL_PORT
app.config["MAIL_USE_TLS"] = config.MAIL_USE_TLS
app.config["MAIL_USERNAME"] = config.MAIL_USERNAME
app.config["MAIL_PASSWORD"] = config.MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = config.MAIL_DEFAULT_SENDER

mysql.init_app(app)
mail.init_app(app)


def save_upload(file_obj, folder, url_prefix):
    """Save an uploaded file if present and return its stored relative path, else None."""
    if file_obj and file_obj.filename:
        filename = secure_filename(file_obj.filename)
        file_obj.save(os.path.join(folder, filename))
        return url_prefix + filename
    return None


# register seller route
@app.route("/seller/register", methods=["GET", "POST"])
def seller_register():

    if request.method == "POST":

        shop_name = request.form.get("shop_name", "").strip()
        owner_name = request.form.get("owner_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        gst_no = request.form.get("gst_no", "").strip()
        pan_no = request.form.get("pan_no", "").strip()
        address = request.form.get("address", "").strip()
        city = request.form.get("city", "").strip()
        state = request.form.get("state", "").strip()
        pincode = request.form.get("pincode", "").strip()
        category = request.form.get("category", "").strip()

        # Basic required-field check so we fail with a friendly flash
        # instead of a raw KeyError/500 if something is missing.
        required = {
            "Shop Name": shop_name,
            "Owner Name": owner_name,
            "Email": email,
            "Phone": phone,
            "GST No": gst_no,
            "PAN No": pan_no,
            "Address": address,
            "City": city,
            "State": state,
            "Pincode": pincode,
            "Category": category,
        }
        missing = [label for label, val in required.items() if not val]
        if missing:
            flash(f"Please fill in: {', '.join(missing)}.", "danger")
            return redirect("/seller/register")

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect("/seller/register")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return redirect("/seller/register")

        shop_logo = request.files.get("shop_logo")
        gst_certificate = request.files.get("gst_certificate")
        pan_document = request.files.get("pan_document")

        product_image_1 = request.files.get("product_image_1")
        product_image_2 = request.files.get("product_image_2")
        product_image_3 = request.files.get("product_image_3")

        # Check if email or phone exists
        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT seller_id FROM sellers WHERE email=%s OR phone=%s",
            (email, phone)
        )

        existing = cur.fetchone()

        if existing:
            cur.close()
            flash("Email or Phone already exists!", "danger")
            return redirect("/seller/register")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Save uploaded files (all optional at the DB level, but you can
        # add required-file checks above if you want to enforce them).
        shop_logo_path = save_upload(shop_logo, SHOP_LOGO_FOLDER, "uploads/shop_logos/")
        gst_path = save_upload(gst_certificate, GST_FOLDER, "uploads/gst/")
        pan_path = save_upload(pan_document, PAN_FOLDER, "uploads/pan/")

        product1_path = save_upload(product_image_1, PRODUCT_FOLDER, "uploads/products/")
        product2_path = save_upload(product_image_2, PRODUCT_FOLDER, "uploads/products/")
        product3_path = save_upload(product_image_3, PRODUCT_FOLDER, "uploads/products/")

        cur.execute("""
            INSERT INTO sellers
            (
            shop_name,
            owner_name,
            email,
            phone,
            password,
            gst_no,
            pan_no,
            address,
            city,
            state,
            pincode,
            category,
            shop_logo,
            gst_certificate,
            pan_document,
            product_image_1,
            product_image_2,
            product_image_3,
            status
            )

            VALUES
            (
            %s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,
            %s
            )
            """,

            (
            shop_name,
            owner_name,
            email,
            phone,
            hashed_password,

            gst_no,
            pan_no,
            address,
            city,
            state,
            pincode,
            category,

            shop_logo_path,
            gst_path,
            pan_path,

            product1_path,
            product2_path,
            product3_path,

            "Pending"
            ))

        mysql.connection.commit()
        cur.close()

        flash(
            "Registration submitted successfully! Your account is under "
            "review. You'll receive an email once the admin approves it.",
            "success"
        )
        return redirect("/seller/login")

    return render_template("Seller/seller_login.html")


# seller login route
@app.route("/seller/login", methods=["GET", "POST"])
def seller_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("""
                    SELECT
                    seller_id,
                    shop_name,
                    owner_name,
                    password,
                    status
                    FROM sellers
                    WHERE email=%s
                    """, (email,))

        seller = cur.fetchone()
        cur.close()

        if seller:

            seller_id = seller[0]
            shop_name = seller[1]
            owner_name = seller[2]
            password_hash = seller[3]
            status = seller[4]

            if check_password_hash(password_hash, password):

                if status == "Approved":

                    session["seller_id"] = seller_id
                    session["shop_name"] = shop_name
                    session["owner_name"] = owner_name

                    flash("Login Successful!", "success")
                    return redirect("/seller/dashboard")

                elif status == "Pending":
                    flash(
                        "Your account is still waiting for admin approval. "
                        "We'll email you as soon as it's reviewed.",
                        "warning"
                    )

                elif status == "Rejected":
                    flash("Your account application was not approved.", "danger")

                elif status == "Suspended":
                    flash("Your account has been suspended.", "danger")

            else:
                flash("Wrong Password!", "danger")

        else:
            flash("Email not found!", "danger")

    return render_template("Seller/seller_login.html")


# admin login route
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        print("Email entered:", email)

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT admin_id, admin_name, email, password, role
            FROM admins
            WHERE email=%s
        """, (email,))

        admin = cur.fetchone()

        print("Database Result:", admin)

        cur.close()

        if admin:

            print("Stored Hash:", admin[3])

            print(
                "Password Match:",
                check_password_hash(admin[3], password)
            )

            if check_password_hash(admin[3], password):

                session["admin_id"] = admin[0]
                session["admin_name"] = admin[1]
                session["role"] = admin[4]

                print("LOGIN SUCCESS")

                return redirect("/admin/dashboard")

            else:
                print("PASSWORD INCORRECT")

        else:
            print("EMAIL NOT FOUND")

    return render_template("Admin/admin_login.html")


# dashboard protected

# 1. Sellers
@app.route("/seller/dashboard")
def seller_dashboard():

    if "seller_id" not in session:
        return redirect("/seller/login")

    return render_template("Seller/index.html")


# 2. Admin
@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect("/admin/login")

    cur = mysql.connection.cursor()
    print("=== NEW ADMIN DASHBOARD RUNNING ===")
    cur.execute("""
    SELECT
        seller_id,
        shop_name,
        owner_name,
        email,
        phone,
        status,
        shop_logo,
        gst_certificate,
        pan_document,
        product_image_1,
        product_image_2,
        product_image_3
    FROM sellers
    ORDER BY FIELD(status,'Pending','Approved','Rejected','Suspended'),
             seller_id DESC
""")

    sellers = cur.fetchall()

    print("Total sellers:", len(sellers))
    for seller in sellers:
        print(seller)

    cur.close()

    return render_template("Admin/index.html", sellers=sellers)
# admin approves/rejects/suspends a seller - this is what actually
# unlocks seller login, and triggers the notification email.
@app.route("/admin/seller/<int:seller_id>/status", methods=["POST"])
def update_seller_status(seller_id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    new_status = request.form.get("status")
    if new_status not in ("Approved", "Rejected", "Suspended", "Pending"):
        flash("Invalid status.", "danger")
        return redirect("/admin/dashboard")

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT shop_name, owner_name, email FROM sellers WHERE seller_id=%s",
        (seller_id,)
    )
    seller = cur.fetchone()

    if not seller:
        cur.close()
        flash("Seller not found.", "danger")
        return redirect("/admin/dashboard")

    cur.execute(
        "UPDATE sellers SET status=%s WHERE seller_id=%s",
        (new_status, seller_id)
    )
    mysql.connection.commit()
    cur.close()

    shop_name, owner_name, seller_email = seller

    # Email the seller so they know they can now log in (or why they can't).
    try:
        send_seller_status_email(shop_name, owner_name, seller_email, new_status)
    except Exception as e:
        # Don't block the admin action if email sending fails - just warn.
        flash(f"Status updated, but the notification email failed to send: {e}", "warning")
        return redirect("/admin/dashboard")

    flash(f"{shop_name} marked as {new_status}. Notification email sent.", "success")
    return redirect("/admin/dashboard")


# seller logout
@app.route("/seller/logout")
def seller_logout():
    session.pop("seller_id", None)
    session.pop("shop_name", None)
    session.pop("owner_name", None)
    return redirect("/seller/login")

#admin logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_name", None)
    session.pop("role", None)
    return redirect("/admin/login")


@app.route("/create-order", methods=["POST"])
def create_order():

    amount = 79900  # Test amount ₹799

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return jsonify({
        "order_id": order["id"],
        "amount": amount,
        "key": config.RAZORPAY_KEY_ID
    })


#payment route
@app.route("/payment-success", methods=["POST"])
def payment_success():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json()

    params = {
        "razorpay_order_id": data["razorpay_order_id"],
        "razorpay_payment_id": data["razorpay_payment_id"],
        "razorpay_signature": data["razorpay_signature"]
    }

    try:

        client.utility.verify_payment_signature(params)

        cursor = mysql.connection.cursor()

        cursor.execute("""
            INSERT INTO orders
            (
                user_id,
                razorpay_order_id,
                razorpay_payment_id,
                total_amount,
                status
            )
            VALUES(%s,%s,%s,%s,%s)
        """,
        (
            session["user_id"],
            data["razorpay_order_id"],
            data["razorpay_payment_id"],
            799,
            "Paid"
        ))

        mysql.connection.commit()
        cursor.close()

        return jsonify({"success": True})

    except Exception as e:

        print(e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

#confirmation route
@app.route("/confirmation")
def confirmation():

    return render_template("templates/confirmation.html")


@app.route("/api/products")
def api_products():

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.brand,
            p.description,
            p.price,
            p.stock,
            p.rating,
            p.total_reviews,
            p.badge,
            pt.category_name,
            pt.subcategory_name

        FROM products p

        JOIN product_types pt
            ON p.type_id = pt.id
    """)

    rows = cursor.fetchall()
    cursor.close()

    products = []

    for row in rows:

        # Convert category to folder name
        category = row[9].strip().lower()

        # Optional mapping if your DB names differ from folder names
        folder_map = {
            "cosmetics": "cosmetics",
            "jewellery": "jewellery",
            "footwear": "footwear",
            "bags": "bags",
            "perfume": "perfume"
        }

        folder_name = folder_map.get(category, "cosmetics")

        folder = os.path.join(
            app.static_folder,
            "uploads",
            folder_name
        )

        image_path = ""

        if os.path.exists(folder):

            images = [
                img for img in os.listdir(folder)
                if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
            ]

            if images:
                image_path = url_for(
                    "static",
                    filename=f"uploads/{folder_name}/{random.choice(images)}"
                )

        print("Category:", category)
        print("Folder:", folder)
        print("Image:", image_path)

        products.append({
            "product_id": row[0],
            "product_name": row[1],
            "brand": row[2],
            "description": row[3],
            "price": float(row[4]),
            "stock": row[5],
            "rating": float(row[6]),
            "total_reviews": row[7],
            "badge": row[8],
            "category_name": row[9],
            "catLabel": row[10],
            "image1": image_path
        })

    return jsonify(products)

@app.route("/shop")
def shop():
    print("SHOP TEMPLATE LOADED")
    return render_template("templates/shop.html")


#add to cart
@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401

    data = request.get_json()

    product_id = data["product_id"]
    quantity = data.get("quantity", 1)

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT id
        FROM cart
        WHERE user_id=%s AND product_id=%s
    """, (session["user_id"], product_id))

    item = cursor.fetchone()

    if item:

        cursor.execute("""
            UPDATE cart
            SET quantity = quantity + %s
            WHERE user_id=%s
            AND product_id=%s
        """, (quantity, session["user_id"], product_id))

    else:

        cursor.execute("""
            INSERT INTO cart
            (user_id, product_id, quantity)
            VALUES(%s,%s,%s)
        """, (session["user_id"], product_id, quantity))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"success": True})

#get cart items
@app.route("/api/cart")
def get_cart():

    if "user_id" not in session:
        return jsonify([])

    cursor = mysql.connection.cursor()

    cursor.execute("""
        SELECT

            c.id,
            c.quantity,

            p.product_id,
            p.name,
            p.price,

            COALESCE(pi.image_url,'no-image.jpg')

        FROM cart c

        JOIN products p
            ON c.product_id=p.product_id

        LEFT JOIN product_images pi
            ON p.product_id=pi.product_id
            AND pi.display_order=1

        WHERE c.user_id=%s
    """, (session["user_id"],))

    rows = cursor.fetchall()

    cursor.close()

    cart=[]

    for row in rows:

        cart.append({

            "cart_id":row[0],
            "quantity":row[1],

            "product_id":row[2],
            "name":row[3],
            "price":float(row[4]),
            "image":row[5]

        })

    return jsonify(cart)

#remove from cart
@app.route("/api/cart/remove/<int:cart_id>", methods=["DELETE"])
def remove_cart_item(cart_id):

    if "user_id" not in session:
        return jsonify({"success":False}),401

    cursor=mysql.connection.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE id=%s
        AND user_id=%s
    """,(cart_id,session["user_id"]))

    mysql.connection.commit()

    cursor.close()

    return jsonify({"success":True})

#Update Quantity
@app.route("/api/cart/update", methods=["POST"])
def update_cart():

    if "user_id" not in session:
        return jsonify({"success":False}),401

    data=request.get_json()

    cursor=mysql.connection.cursor()

    cursor.execute("""
        UPDATE cart
        SET quantity=%s
        WHERE id=%s
        AND user_id=%s
    """,
    (
        data["quantity"],
        data["cart_id"],
        session["user_id"]
    ))

    mysql.connection.commit()

    cursor.close()

    return jsonify({"success":True})


#add to wishlist
@app.route("/api/wishlist/add", methods=["POST"])
def add_to_wishlist():

    if "user_id" not in session:
        return jsonify({"success":False}),401

    data=request.get_json()

    product_id=data["product_id"]

    cursor=mysql.connection.cursor()

    cursor.execute("""
        SELECT id
        FROM wishlist
        WHERE user_id=%s
        AND product_id=%s
    """,(session["user_id"],product_id))

    exists=cursor.fetchone()

    if not exists:

        cursor.execute("""
            INSERT INTO wishlist(user_id,product_id)
            VALUES(%s,%s)
        """,(session["user_id"],product_id))

        mysql.connection.commit()

    cursor.close()

    return jsonify({"success":True})


#get wishlist items
@app.route("/api/wishlist")
def get_wishlist():

    if "user_id" not in session:
        return jsonify([])

    cursor=mysql.connection.cursor()

    cursor.execute("""

    SELECT

        w.id,

        p.product_id,
        p.name,
        p.price,

        COALESCE(pi.image_url,'no-image.jpg')

    FROM wishlist w

    JOIN products p
        ON w.product_id=p.product_id

    LEFT JOIN product_images pi
        ON p.product_id=pi.product_id
        AND pi.display_order=1

    WHERE w.user_id=%s

    """,(session["user_id"],))

    rows=cursor.fetchall()

    cursor.close()

    wishlist=[]

    for row in rows:

        wishlist.append({

            "wishlist_id":row[0],
            "product_id":row[1],
            "name":row[2],
            "price":float(row[3]),
            "image":row[4]

        })

    return jsonify(wishlist)


#remove from wishlist
@app.route("/api/wishlist/remove/<int:wishlist_id>",methods=["DELETE"])
def remove_wishlist(wishlist_id):

    if "user_id" not in session:
        return jsonify({"success":False}),401
    cursor=mysql.connection.cursor()
    cursor.execute("""
    DELETE FROM wishlist
    WHERE id=%s
    AND user_id=%s

    """,(wishlist_id,session["user_id"]))
    mysql.connection.commit()
    cursor.close()
    return jsonify({"success":True})

#admin approval
@app.route("/admin/approve_seller/<int:seller_id>")
def approve_seller(seller_id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    cur = mysql.connection.cursor()

    cur.execute(
        "UPDATE sellers SET status='Approved' WHERE seller_id=%s",
        (seller_id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect("/admin/dashboard")

#admin reject 
@app.route("/admin/reject_seller/<int:seller_id>")
def reject_seller(seller_id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    cur = mysql.connection.cursor()

    cur.execute(
        "UPDATE sellers SET status='Rejected' WHERE seller_id=%s",
        (seller_id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect("/admin/dashboard")
    

if __name__ == "__main__":
    app.run(debug=True)



