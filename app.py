import os
import random

from dotenv import load_dotenv
load_dotenv()

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
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from werkzeug.utils import secure_filename
from database import get_connection
from mail import mail, send_seller_status_email

from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.jinja_loader = ChoiceLoader([
    FileSystemLoader("templates"),
    FileSystemLoader("Admin"),
    FileSystemLoader("Seller")
])
import os

print("Root Path:", app.root_path)
print("Template Folder:", app.template_folder)
print("Admin Login Exists:",
      os.path.exists(
          os.path.join(app.root_path, "templates", "Admin", "admin_login.html")
      ))
print("Template folder:", app.template_folder)

# PRODUCT IMAGE UPLOAD CONFIGURATION
UPLOAD_FOLDER = os.path.join(
    app.static_folder,
    "uploads",
    "products"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}


def allowed_image(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_IMAGE_EXTENSIONS
    )

SHOP_LOGO_FOLDER = os.path.join(UPLOAD_FOLDER, "shop_logos")
GST_FOLDER = os.path.join(UPLOAD_FOLDER, "gst")
PAN_FOLDER = os.path.join(UPLOAD_FOLDER, "pan")
PRODUCT_FOLDER = os.path.join(UPLOAD_FOLDER, "products")

os.makedirs(SHOP_LOGO_FOLDER, exist_ok=True)
os.makedirs(GST_FOLDER, exist_ok=True)
os.makedirs(PAN_FOLDER, exist_ok=True)
os.makedirs(PRODUCT_FOLDER, exist_ok=True)
app.secret_key = os.getenv("SECRET_KEY")

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
mail.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/checkout")
def checkout():

    if "user_id" not in session:
        return redirect(url_for("login", next="/checkout"))

    return render_template(
        "checkout.html",
        user_id=session["user_id"],
        user_name=session.get("user_name")
    )


@app.route("/account")
def account():

    if "user_id" not in session:
        return redirect(url_for("login", next="/account"))

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            profile_image,
            gender,
            address,
            landmark,
            pincode
        FROM users
        WHERE id = %s
    """, (session["user_id"],))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "account.html",
        user=user
    )

@app.route("/api/account/profile", methods=["POST"])
def update_profile():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json()

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()

    if not full_name or not email:
        return jsonify({
            "success": False,
            "message": "Name and email are required."
        }), 400

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE users
            SET full_name = %s,
                email = %s
            WHERE id = %s
        """, (
            full_name,
            email,
            session["user_id"]
        ))

        conn.commit()

        session["user_name"] = full_name

        return jsonify({
            "success": True,
            "message": "Profile updated successfully."
        })

    except Exception as e:

        conn.rollback()

        print("PROFILE UPDATE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cur.close()
        conn.close()

@app.route("/api/account/details", methods=["POST"])
def update_details():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json()

    phone = data.get("phone", "").strip()
    gender = data.get("gender", "").strip()

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE users
            SET phone = %s,
                gender = %s
            WHERE id = %s
        """, (
            phone,
            gender,
            session["user_id"]
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Details updated successfully."
        })

    except Exception as e:

        conn.rollback()

        print("DETAIL UPDATE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cur.close()
        conn.close()

@app.route("/api/account/address", methods=["POST"])
def update_address():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json()

    address = data.get("address", "").strip()
    landmark = data.get("landmark", "").strip()
    pincode = data.get("pincode", "").strip()

    if not address or not landmark or not pincode:
        return jsonify({
            "success": False,
            "message": "All address fields are required."
        }), 400

    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            UPDATE users
            SET address = %s,
                landmark = %s,
                pincode = %s
            WHERE id = %s
        """, (
            address,
            landmark,
            pincode,
            session["user_id"]
        ))

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Address updated successfully."
        })

    except Exception as e:

        conn.rollback()

        print("ADDRESS UPDATE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cur.close()
        conn.close()


@app.route("/confirmation")
def confirmation():

    if "user_id" not in session:
        return redirect(
            url_for("login", next="/confirmation")
        )

    order_ids = session.get("last_order_ids", [])

    if not order_ids:
        return render_template(
            "confirmation.html",
            orders=[],
            user_id=session["user_id"],
            user_name=session.get("user_name")
        )

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        placeholders = ",".join(
            ["%s"] * len(order_ids)
        )

        query = f"""
            SELECT
                o.order_id,
                o.product_id,
                o.quantity,
                o.product_price,
                o.total_amount,
                o.order_status,
                o.order_date,

                p.product_name,
                p.brand,

                (
                    SELECT pi.image_path
                    FROM product_images pi
                    WHERE pi.product_id = p.product_id
                    ORDER BY
                        pi.is_primary DESC,
                        pi.display_order ASC,
                        pi.image_id ASC
                    LIMIT 1
                ) AS image

            FROM orders o

            JOIN products p
                ON o.product_id = p.product_id

            WHERE o.customer_id = %s
            AND o.order_id IN ({placeholders})

            ORDER BY o.order_id ASC
        """

        cursor.execute(
            query,
            [session["user_id"]] + order_ids
        )

        orders = cursor.fetchall()

        for order in orders:

            order["product_price"] = float(
                order["product_price"] or 0
            )

            order["total_amount"] = float(
                order["total_amount"] or 0
            )

            if order["order_date"]:

                order["order_date"] = (
                    order["order_date"]
                    .strftime("%Y-%m-%d %H:%M:%S")
                )

        # Calculate complete checkout total
        grand_total = sum(
            order["total_amount"]
            for order in orders
        )

        return render_template(
            "confirmation.html",
            orders=orders,
            grand_total=grand_total,
            user_id=session["user_id"],
            user_name=session.get("user_name")
        )

    except Exception as e:

        print("CONFIRMATION ERROR:", e)

        return render_template(
            "confirmation.html",
            orders=[],
            grand_total=0,
            user_id=session["user_id"],
            user_name=session.get("user_name")
        )

    finally:

        cursor.close()
        conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():

    next_page = request.args.get("next", "")

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        # Get the page user originally wanted
        next_page = request.form.get("next", "")

        print("Email:", email)
        print("Next page:", next_page)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                full_name,
                password
            FROM users
            WHERE email=%s
        """, (email,))

        user = cur.fetchone()

        cur.close()
        conn.close()

        # =========================
        # CHECK LOGIN
        # =========================

        if user and check_password_hash(user[2], password):

            print("LOGIN SUCCESS")

            # Save user information in Flask session
            session["user_id"] = user[0]
            session["user_name"] = user[1]

            print("SESSION:", dict(session))

            # If user originally wanted /account
            if next_page and next_page.startswith("/"):
                return redirect(next_page)

            # Normal login
            return redirect(url_for("account"))

        else:
            flash("Incorrect email or password.", "danger")

    return render_template(
        "login.html",
        next_page=next_page
    )

@app.route("/shop")
def shop():

    category = request.args.get("cat")
    type_id = request.args.get("type_id")
    sort = request.args.get("sort")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        query = """
            SELECT
                p.product_id,
                p.product_name,
                p.brand,
                p.price,
                p.stock,
                p.rating,
                p.total_reviews,
                p.badge,
                p.status,
                p.seller_id,
                p.type_id,
                p.material,
                p.description,
                pt.category_id,
                pt.category_name,
                pt.subcategory_name,

                (
                    SELECT pi.image_path
                    FROM product_images pi
                    WHERE pi.product_id = p.product_id
                    ORDER BY
                        pi.is_primary DESC,
                        pi.display_order ASC,
                        pi.image_id ASC
                    LIMIT 1
                ) AS primary_image

            FROM products p

            LEFT JOIN product_types pt
                ON p.type_id = pt.id

            WHERE p.status = 'Approved'
        """

        params = []

        if type_id:

            query += """
                AND p.type_id = %s
            """

            params.append(int(type_id))

        elif category:

            category_map = {
                "cosmetics": 1,
                "jewellery": 2,
                "footwear": 3,
                "bags": 4,
                "perfumes": 5
            }

            category_id = category_map.get(
                category.lower()
            )

            if category_id:

                query += """
                    AND pt.category_id = %s
                """

                params.append(category_id)

        if sort == "new":

            query += """
                ORDER BY p.created_at DESC
            """

        elif sort == "best":

            query += """
                ORDER BY p.rating DESC,
                         p.total_reviews DESC
            """

        else:

            query += """
                ORDER BY p.product_id DESC
            """

        cursor.execute(
            query,
            params
        )

        products = cursor.fetchall()

        return render_template(
            "shop.html",
            products=products
        )

    finally:

        cursor.close()
        conn.close()

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

        print(email)

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
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT seller_id FROM sellers WHERE email=%s OR phone=%s",
            (email, phone)
        )

        existing = cur.fetchone()

        if existing:
            cur.close()
            conn.close()
            flash("Email or Phone already exists!", "danger")
            return redirect("/seller/register")

        # Hash password
        hashed_password = generate_password_hash(password)
        print(request.form)

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

        conn.commit()
        cur.close()
        conn.close()

        flash(
            "Registration submitted successfully! Your account is under "
            "review. You'll receive an email once the admin approves it.",
            "success"
        )
        return redirect("/seller/login")

    return render_template("seller_login.html")


# seller login route
@app.route("/seller/login", methods=["GET", "POST"])
def seller_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cur = conn.cursor()
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
        conn.close()

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

@app.route("/seller/dashboard")
def seller_dashboard():

    if "seller_id" not in session:
        return redirect(url_for("seller_login"))

    return render_template("Seller/seller_index.html")

@app.route("/seller/products")
def seller_products():

    # Seller must be logged in
    if "seller_id" not in session:
        return jsonify({
            "success": False,
            "message": "Seller login required"
        }), 401

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.brand,
                p.price,
                p.stock,
                p.status,

                p.seller_id,
                s.shop_name,

                o.order_id,
                o.customer_id,
                o.quantity,
                o.product_price,
                o.total_amount,
                o.order_status,
                o.order_date,

                u.full_name,
                u.email,
                u.phone

            FROM products p

            LEFT JOIN sellers s
                ON p.seller_id = s.seller_id

            LEFT JOIN orders o
                ON p.product_id = o.product_id
                AND o.seller_id = p.seller_id

            LEFT JOIN users u
                ON o.customer_id = u.id

            ORDER BY
                p.product_id DESC,
                o.order_date DESC
        """)

        rows = cursor.fetchall()

        products = {}

        for row in rows:

            product_id = row[0]

            # Create product only once
            if product_id not in products:
                products[product_id] = {
                    "id": row[0],
                    "name": row[1],
                    "brand": row[2],
                    "price": float(row[3]),
                    "stock": row[4],
                    "status": row[5],

                    "seller_id": row[6],
                    "shop_name": row[7],

                    "orders": []
                }

            # Add order information if product has an order
            if row[8] is not None:

                products[product_id]["orders"].append({

                    "order_id": row[8],
                    "customer_id": row[9],
                    "quantity": row[10],

                    "product_price": float(row[11]),
                    "total_amount": float(row[12]),

                    "order_status": row[13],

                    "order_date": (
                        row[14].strftime("%Y-%m-%d %H:%M:%S")
                        if row[14]
                        else None
                    ),

                    "customer": {
                        "id": row[9],
                        "name": row[15],
                        "email": row[16],
                        "phone": row[17]
                    }
                })

        return jsonify({
            "success": True,
            "products": list(products.values())
        })

    except Exception as e:

        print("SELLER PRODUCTS ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
# admin login route
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        print("Admin Email:", email)
        print("Admin Password:", password)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT admin_id, admin_name, email, password, role
            FROM admins
            WHERE email=%s
        """, (email,))

        admin = cur.fetchone()

        print("Database Result:", admin)
        print(admin)
        cur.close()
        conn.close()

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

@app.route("/register", methods=["POST"])
def user_register():

    print("===== REGISTER ROUTE CALLED =====")
    print(request.form.to_dict())
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    full_name = f"{first_name} {last_name}"

    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    gender = request.form.get("gender")
    address = request.form.get("address")
    landmark = request.form.get("landmark")
    pincode = request.form.get("pincode")

    print("Full Name:", full_name)
    print("Email:", email)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    existing = cur.fetchone()

    if existing:
        flash("Email already exists.", "danger")
        cur.close()
        conn.close()
        return redirect(url_for("login"))

    hashed_password = generate_password_hash(password)

    cur.execute("""
        INSERT INTO users
        (full_name, email, phone, password, gender, address, landmark, pincode)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        full_name,
        email,
        phone,
        hashed_password,
        gender,
        address,
        landmark,
        pincode
    ))

    conn.commit()

    cur.close()
    conn.close()

    flash("Account created successfully!", "success")
    return redirect(url_for("login"))

# dashboard protected
@app.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    conn = get_connection()
    cur = conn.cursor()

    # SELLERS

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
        ORDER BY FIELD(
            status,
            'Pending',
            'Approved',
            'Rejected',
            'Suspended'
        ),
        seller_id DESC
    """)

    sellers = cur.fetchall()

    # PRODUCTS
    cur.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.brand,
            p.price,
            p.stock,
            p.rating,
            p.total_reviews,
            p.badge,
            p.status,
            p.seller_id,
            s.shop_name,
            pt.category_name,
            pt.subcategory_name,

            (
                SELECT pi.image_path
                FROM product_images pi
                WHERE pi.product_id = p.product_id
                ORDER BY
                    pi.is_primary DESC,
                    pi.display_order ASC,
                    pi.image_id ASC
                LIMIT 1
            ) AS primary_image

        FROM products p

        LEFT JOIN sellers s
            ON p.seller_id = s.seller_id

        LEFT JOIN product_types pt
            ON p.type_id = pt.id

        ORDER BY
            FIELD(
                p.status,
                'Pending',
                'Approved',
                'Rejected'
            ),
            p.product_id DESC
    """)

    
    products = cur.fetchall()
    print("ADMIN PRODUCTS:")
    for product in products:
        print(product)


    # CUSTOMERS
    cur.execute("""
        SELECT
            id,
            full_name,
            email,
            phone,
            created_at
        FROM users
        ORDER BY id DESC
    """)

    customers = cur.fetchall()


    # BASIC COUNTS
    total_sellers = len(sellers)
    total_products = len(products)
    total_customers = len(customers)


    # SELLER STATUS COUNTS
    pending_sellers = sum(
        1 for seller in sellers
        if seller[5] == "Pending"
    )

    approved_sellers = sum(
        1 for seller in sellers
        if seller[5] == "Approved"
    )

    suspended_sellers = sum(
        1 for seller in sellers
        if seller[5] == "Suspended"
    )

    # ORDERS
    cur.execute("""
        SELECT
            order_id,
            customer_id,
            seller_id,
            product_id,
            quantity,
            product_price,
            total_amount,
            commission_percent,
            commission_amount,
            seller_earning,
            order_status,
            order_date
        FROM orders
        ORDER BY order_date DESC
    """)

    orders = cur.fetchall()


    # ORDER STATISTICS
    total_orders = len(orders)

    total_revenue = sum(
        float(order[6] or 0)
        for order in orders
        if order[10] != "Cancelled"
    )

    pending_orders = sum(
        1 for order in orders
        if order[10] == "Pending"
    )

    cancelled_orders = sum(
    1 for order in orders
    if order[10] == "Cancelled"
    )

    # COUPONS
    cur.execute("""
        SELECT
            id,
            code,
            discount,
            expiry_date,
            active
        FROM coupons
        ORDER BY id DESC
    """)

    coupons = cur.fetchall()


    # COMMISSION
    total_commission = sum(
        float(order[8] or 0)
        for order in orders
    )


    cur.close()
    conn.close()


    return render_template(
        "Admin/admin_index.html",

        sellers=sellers,
        products=products,
        customers=customers,
        orders=orders,
        coupons=coupons,

        total_sellers=total_sellers,
        total_products=total_products,
        total_customers=total_customers,
        total_orders=total_orders,

        pending_sellers=pending_sellers,
        approved_sellers=approved_sellers,
        suspended_sellers=suspended_sellers,

        total_revenue=total_revenue,
        pending_orders=pending_orders,
        cancelled_orders=cancelled_orders,
        total_commission=total_commission
)

@app.route("/admin/order/<int:order_id>/status", methods=["POST"])
def admin_update_order_status(order_id):

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid order status"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE orders
            SET order_status = %s
            WHERE order_id = %s
        """, (
            status,
            order_id
        ))

        conn.commit()

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Order not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Order status updated successfully"
        })

    except Exception as e:

        conn.rollback()

        print("ORDER STATUS ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Database error"
        }), 500

    finally:

        cursor.close()
        conn.close()

@app.route(
    "/admin/product/<int:product_id>/approve",
    methods=["POST"]
)
def approve_product(product_id):

    if "admin_id" not in session:

        return jsonify({
            "success": False,
            "message": "Admin login required"
        }), 401


    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE products
            SET status = 'Approved'
            WHERE product_id = %s
            AND status = 'Pending'
        """, (product_id,))

        if cursor.rowcount == 0:

            conn.rollback()

            return jsonify({
                "success": False,
                "message": (
                    "Product not found or "
                    "already processed"
                )
            }), 400


        conn.commit()


        return jsonify({
            "success": True,
            "message": "Product approved successfully"
        })


    except Exception as e:

        conn.rollback()

        print(
            "APPROVE PRODUCT ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": "Failed to approve product"
        }), 500


    finally:

        cursor.close()
        conn.close()

@app.route(
    "/admin/product/<int:product_id>/reject",
    methods=["POST"]
)
def reject_product(product_id):

    if "admin_id" not in session:

        return jsonify({
            "success": False,
            "message": "Admin login required"
        }), 401


    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE products
            SET status = 'Rejected'
            WHERE product_id = %s
            AND status = 'Pending'
        """, (product_id,))


        if cursor.rowcount == 0:

            conn.rollback()

            return jsonify({
                "success": False,
                "message": (
                    "Product not found or "
                    "already processed"
                )
            }), 400


        conn.commit()


        return jsonify({
            "success": True,
            "message": "Product rejected successfully"
        })


    except Exception as e:

        conn.rollback()

        print(
            "REJECT PRODUCT ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": "Failed to reject product"
        }), 500


    finally:

        cursor.close()
        conn.close()

@app.route("/admin/product/<int:product_id>/delete", methods=["POST"])
def admin_delete_product(product_id):

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            DELETE FROM products
            WHERE product_id = %s
        """, (product_id,))

        conn.commit()

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Product not found"
            }), 404

        return jsonify({
            "success": True,
            "message": "Product deleted successfully"
        })

    except Exception as e:

        conn.rollback()

        print("PRODUCT DELETE ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

@app.route("/admin/product/add", methods=["POST"])
def admin_add_product():

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    data = request.get_json(silent=True) or {}

    product_name = data.get("product_name", "").strip()
    brand = data.get("brand", "").strip()
    price = data.get("price", 0)
    stock = data.get("stock", 0)
    type_id = data.get("type_id")

    if not product_name:
        return jsonify({
            "success": False,
            "message": "Product name is required"
        }), 400

    if not brand:
        return jsonify({
            "success": False,
            "message": "Brand is required"
        }), 400

    if not type_id:
        return jsonify({
            "success": False,
            "message": "Product type is required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO products
            (
                type_id,
                product_name,
                brand,
                material,
                price,
                stock,
                rating,
                total_reviews
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                0.0,
                0
            )
        """, (
            type_id,
            product_name,
            brand,
            "Not Specified",
            price,
            stock
        ))

        conn.commit()

        product_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Product added successfully",
            "product_id": product_id
        })

    except Exception as e:

        conn.rollback()

        print("PRODUCT ADD ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

@app.route("/seller/product/add", methods=["POST"])
def seller_add_product():

    # ================= SELLER LOGIN CHECK =================

    if "seller_id" not in session:
        return jsonify({
            "success": False,
            "message": "Seller login required"
        }), 401


    # ================= GET FORM DATA =================

    product_name = request.form.get(
        "product_name",
        ""
    ).strip()

    brand = request.form.get(
        "brand",
        ""
    ).strip()

    material = request.form.get(
        "material",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    # Main category selected by seller
    category_id = request.form.get("type_id")

    price = request.form.get("price")

    stock = request.form.get("stock")


    # ================= VALIDATION =================

    if not product_name:
        return jsonify({
            "success": False,
            "message": "Product name is required"
        }), 400


    if not brand:
        return jsonify({
            "success": False,
            "message": "Brand is required"
        }), 400


    if not material:
        return jsonify({
            "success": False,
            "message": "Material is required"
        }), 400


    if not category_id:
        return jsonify({
            "success": False,
            "message": "Category is required"
        }), 400


    if price is None or price == "":
        return jsonify({
            "success": False,
            "message": "Price is required"
        }), 400


    if stock is None or stock == "":
        return jsonify({
            "success": False,
            "message": "Stock is required"
        }), 400


    # ================= CONVERT DATA =================

    try:

        price = float(price)

        stock = int(stock)

        category_id = int(category_id)

    except (ValueError, TypeError):

        return jsonify({
            "success": False,
            "message": "Invalid price, stock or category"
        }), 400

    category_map = {

        1: 101,   
        2: 201,   
        3: 301,   
        4: 401,   
        5: 501    

    }
    type_id = category_map.get(category_id)
    if not type_id:

        return jsonify({
            "success": False,
            "message": "Invalid category"
        }), 400

    if price <= 0:

        return jsonify({
            "success": False,
            "message": "Price must be greater than 0"
        }), 400


    if stock < 0:

        return jsonify({
            "success": False,
            "message": "Stock cannot be negative"
        }), 400

    images = request.files.getlist("product_images")



    if len(images) > 3:

        return jsonify({
            "success": False,
            "message": "You can upload maximum 3 images"
        }), 400


    allowed_extensions = {
        "jpg",
        "jpeg",
        "png",
        "webp"
    }

    for image in images:
        if not image or image.filename == "":
            continue


        extension = (
            image.filename
            .rsplit(".", 1)[-1]
            .lower()
        )

        if extension not in allowed_extensions:
            return jsonify({
                "success": False,
                "message": (
                    "Only JPG, JPEG, PNG and WEBP "
                    "images are allowed"
                )
            }), 400


    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO products
            (
                seller_id,
                type_id,
                product_name,
                brand,
                material,
                price,
                rating,
                total_reviews,
                badge,
                stock,
                description,
                status
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                0.0,
                0,
                NULL,
                %s,
                %s,
                'Pending'
            )
        """, (
            session["seller_id"],
            type_id,
            product_name,
            brand,
            material,
            price,
            stock,
            description
        ))

        print("PRODUCT INSERT EXECUTED")

        product_id = cursor.lastrowid

        print("NEW PRODUCT ID:", product_id)

        
        upload_folder = os.path.join(
            app.root_path,
            "static",
            "uploads",
            "products"
        )

        os.makedirs(

            upload_folder,

            exist_ok=True

        )

        image_number = 0
        for image in images:

            if not image or image.filename == "":
                continue

            image_number += 1

            original_name = secure_filename(
                image.filename
            )

            extension = (
                original_name
                .rsplit(".", 1)[-1]
                .lower()
            )

            filename = (
                f"product_{product_id}_"
                f"{image_number}.{extension}"
            )

            file_path = os.path.join(
                upload_folder,
                filename

            )

            image.save(file_path)

            image_path = (
                f"uploads/products/{filename}"
            )

            is_primary = (
                1 if image_number == 1 else 0
            )
            cursor.execute("""
                INSERT INTO product_images
                (
                    product_id,
                    image_path,
                    is_primary,
                    display_order
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s
                )
            """, (
                product_id,
                image_path,
                is_primary,
                image_number
            ))
        conn.commit()
        return jsonify({
            "success": True,
            "message": (
                "Product submitted for admin approval"
            ),
            "product_id": product_id
        })
    except Exception as e:

        conn.rollback()
        print(
            "SELLER PRODUCT ERROR:",
            e
        )
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
    
    finally:
        cursor.close()
        conn.close()

@app.route("/admin/product/<int:product_id>/approve", methods=["POST"])
def admin_approve_product(product_id):

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE products
            SET status = 'Approved'
            WHERE product_id = %s
            AND status = 'Pending'
        """, (product_id,))

        conn.commit()

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Product not found or already reviewed"
            }), 404

        return jsonify({
            "success": True,
            "message": "Product approved successfully"
        })

    except Exception as e:

        conn.rollback()

        print("APPROVE PRODUCT ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

@app.route("/admin/product/<int:product_id>/reject", methods=["POST"])
def admin_reject_product(product_id):

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE products
            SET status = 'Rejected'
            WHERE product_id = %s
            AND status = 'Pending'
        """, (product_id,))

        conn.commit()

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Product not found or already reviewed"
            }), 404

        return jsonify({
            "success": True,
            "message": "Product rejected"
        })

    except Exception as e:

        conn.rollback()

        print("REJECT PRODUCT ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

@app.route("/cart")
def cart():

    if "user_id" not in session:
        return redirect(url_for("login", next="/cart"))

    return render_template("cart.html")

# admin approves/rejects/suspends a seller - this is what actually
# unlocks seller login, and triggers the notification email.
@app.route("/admin/seller/<int:seller_id>/status", methods=["POST"])
def update_seller_status(seller_id):

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    new_status = request.form.get("status")

    allowed_statuses = [
        "Approved",
        "Rejected",
        "Suspended",
        "Pending"
    ]

    if new_status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid status"
        }), 400


    conn = get_connection()
    cur = conn.cursor()

    try:

        cur.execute("""
            SELECT
                shop_name,
                owner_name,
                email
            FROM sellers
            WHERE seller_id = %s
        """, (seller_id,))

        seller = cur.fetchone()

        if not seller:

            return jsonify({
                "success": False,
                "message": "Seller not found"
            }), 404


        cur.execute("""
            UPDATE sellers
            SET status = %s
            WHERE seller_id = %s
        """, (
            new_status,
            seller_id
        ))

        conn.commit()

        shop_name, owner_name, seller_email = seller


        try:

            send_seller_status_email(
                shop_name,
                owner_name,
                seller_email,
                new_status
            )

        except Exception as email_error:

            print(
                "SELLER EMAIL ERROR:",
                email_error
            )


        return jsonify({
            "success": True,
            "message":
                f"{shop_name} marked as {new_status}"
        })


    except Exception as e:

        conn.rollback()

        print(
            "SELLER STATUS ERROR:",
            e
        )

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


    finally:

        cur.close()
        conn.close()


# SELLER LOGOUT
@app.route("/seller/logout")
def seller_logout():

    session.pop("seller_id", None)
    session.pop("shop_name", None)
    session.pop("owner_name", None)

    flash("Seller logged out successfully!", "success")

    return redirect(url_for("seller_login"))

# ADMIN LOGOUT
@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_id", None)
    session.pop("admin_name", None)
    session.pop("role", None)

    session.modified = True

    response = redirect(url_for("admin_login"))

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

# user logout
@app.route("/logout")
def logout():

    session.pop("user_id", None)
    session.pop("user_name", None)

    flash("Logged out successfully!", "success")

    return redirect("/login")

@app.route("/delete-account", methods=["POST"])
def delete_account():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "message": "You are not logged in."
        }), 401

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )

        if cursor.rowcount == 0:
            conn.rollback()

            return jsonify({
                "success": False,
                "message": "User account not found."
            }), 404

        conn.commit()

        session.clear()

        return jsonify({
            "success": True,
            "message": "Account deleted successfully."
        })

    except Exception as e:

        if conn:
            conn.rollback()

        print("DELETE ACCOUNT ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Could not delete account."
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()
    


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
        "key": os.getenv("RAZORPAY_KEY_ID")
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

        conn = get_connection()
        cursor = conn.cursor()

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

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:

        print(e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

@app.route("/api/products")
def api_products():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT DATABASE() AS db")
        db = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) AS total FROM products")
        count = cursor.fetchone()

        print("DATABASE USED:", db["db"])
        print("PRODUCT COUNT:", count["total"])

        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                p.brand,
                p.price,
                p.stock,
                p.status,
                p.seller_id
            FROM products p
            ORDER BY p.product_id DESC
        """)

        rows = cursor.fetchall()

        products = []

        for p in rows:
            products.append({
                "product_id": p["product_id"],
                "product_name": p["product_name"],
                "brand": p["brand"],
                "price": float(p["price"] or 0),
                "stock": p["stock"],
                "status": p["status"],
                "seller_id": p["seller_id"]
            })

        print("TOTAL PRODUCTS FROM DATABASE:", len(products))

        return jsonify({
            "success": True,
            "products": products
        })

    except Exception as e:
        print("API PRODUCTS ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()
        
#add to cart
@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():

    if "user_id" not in session:
        return jsonify({"success": False, "message": "Login required"}), 401

    data = request.get_json()

    product_id = data["product_id"]
    quantity = data.get("quantity", 1)

    conn = get_connection()
    cursor = conn.cursor()

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

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})

#get cart items
@app.route("/api/cart")
def get_cart():

    if "user_id" not in session:
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            c.id,
            c.quantity,

            p.product_id,
            p.product_name,
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
    conn.close()

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
        return jsonify({"success": False}), 401

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM cart
        WHERE id=%s
        AND user_id=%s
    """, (cart_id, session["user_id"]))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": True})

#Update Quantity
@app.route("/api/cart/update", methods=["POST"])
def update_cart():

    if "user_id" not in session:
        return jsonify({"success": False}), 401

    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE cart
        SET quantity=%s
        WHERE id=%s
        AND user_id=%s
    """, (
        data["quantity"],
        data["cart_id"],
        session["user_id"]
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": True})


#add to wishlist
@app.route("/api/wishlist/add", methods=["POST"])
def add_to_wishlist():

    if "user_id" not in session:
        return jsonify({"success":False}),401

    data=request.get_json()

    product_id=data["product_id"]
    conn = get_connection()
    cursor = conn.cursor()
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

        conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success":True})


#get wishlist items
@app.route("/api/wishlist")
def get_wishlist():

    if "user_id" not in session:
        return jsonify([])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT

        w.id,

        p.product_id,
        p.product_name,
        p.price,

        COALESCE(pi.image_path,'no-image.jpg')

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
    conn.close()

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

@app.route("/seller/order/<int:order_id>/status", methods=["POST"])
def seller_update_order_status(order_id):

    if "seller_id" not in session:
        return jsonify({
            "success": False,
            "message": "Seller login required"
        }), 401

    data = request.get_json(silent=True) or {}
    status = data.get("status")

    allowed_statuses = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if status not in allowed_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid order status"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE orders
            SET order_status = %s
            WHERE order_id = %s
            AND seller_id = %s
        """, (
            status,
            order_id,
            session["seller_id"]
        ))

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({
                "success": False,
                "message": "Order not found"
            }), 404

        return jsonify({
            "success": True
        })

    except Exception as e:

        conn.rollback()

        print("SELLER STATUS ERROR:", e)

        return jsonify({
            "success": False,
            "message": "Database error"
        }), 500

    finally:

        cursor.close()
        conn.close()

#remove from wishlist
@app.route("/api/wishlist/remove/<int:wishlist_id>",methods=["DELETE"])
def remove_wishlist(wishlist_id):

    if "user_id" not in session:
        return jsonify({"success":False}),401
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM wishlist
    WHERE id=%s
    AND user_id=%s

    """,(wishlist_id,session["user_id"]))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success":True})

#admin approval
@app.route("/admin/approve_seller/<int:seller_id>")
def approve_seller(seller_id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    "UPDATE sellers SET status='Approved' WHERE seller_id=%s",
    (seller_id,)
)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/admin/dashboard")

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found", 404

#admin reject 
@app.route("/admin/reject_seller/<int:seller_id>")
def reject_seller(seller_id):

    if "admin_id" not in session:
        return redirect("/admin/login")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE sellers SET status='Rejected' WHERE seller_id=%s",
        (seller_id,)
    )

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/admin/dashboard")

@app.route("/place-order", methods=["POST"])
def place_order():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    data = request.get_json(silent=True) or {}
    cart = data.get("cart", [])

    if not cart:
        return jsonify({
            "success": False,
            "message": "Your cart is empty."
        }), 400

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        user_id = session["user_id"]

        for item in cart:

            product_id = item.get("id") or item.get("product_id")
            quantity = int(item.get("qty", 1))
            price = float(item.get("price", 0))

            if not product_id:
                continue

            # Get seller from the actual product
            cursor.execute("""
                SELECT seller_id, price
                FROM products
                WHERE product_id = %s
            """, (product_id,))

            product = cursor.fetchone()

            if not product:
                raise Exception(
                    f"Product {product_id} was not found."
                )

            seller_id = product[0]

            # Use database price rather than trusting browser price
            price = float(product[1])

            total_amount = price * quantity

            # Temporary commission calculation
            commission_percent = 10
            commission_amount = (
                total_amount * commission_percent / 100
            )

            seller_earning = (
                total_amount - commission_amount
            )

            cursor.execute("""
                INSERT INTO orders
                (
                    customer_id,
                    seller_id,
                    product_id,
                    quantity,
                    product_price,
                    total_amount,
                    commission_percent,
                    commission_amount,
                    seller_earning,
                    order_status,
                    order_date
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, NOW()
                )
            """, (
                user_id,
                seller_id,
                product_id,
                quantity,
                price,
                total_amount,
                commission_percent,
                commission_amount,
                seller_earning,
                "Pending"
            ))

        conn.commit()

        print("ORDER CREATED SUCCESSFULLY")

        return jsonify({
            "success": True,
            "message": "Order placed successfully."
        })

    except Exception as e:

        if conn:
            conn.rollback()

        print("PLACE ORDER ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        if cursor:
            cursor.close()

        if conn:
            conn.close()

@app.route("/api/account/orders")
def account_orders():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Please login first."
        }), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:

        cursor.execute("""
            SELECT
                o.order_id,
                o.product_id,
                o.quantity,
                o.product_price,
                o.total_amount,
                o.order_status,
                o.order_date,

                p.product_name,
                p.brand,

                (
                    SELECT pi.image_path
                    FROM product_images pi
                    WHERE pi.product_id = p.product_id
                    ORDER BY
                        pi.is_primary DESC,
                        pi.display_order ASC,
                        pi.image_id ASC
                    LIMIT 1
                ) AS image

            FROM orders o

            JOIN products p
                ON o.product_id = p.product_id

            WHERE o.customer_id = %s

            ORDER BY o.order_date DESC
        """, (session["user_id"],))

        orders = cursor.fetchall()

        for order in orders:

            order["product_price"] = float(
                order["product_price"] or 0
            )

            order["total_amount"] = float(
                order["total_amount"] or 0
            )

            if order["order_date"]:
                order["order_date"] = (
                    order["order_date"]
                    .strftime("%Y-%m-%d %H:%M:%S")
                )

        return jsonify({
            "success": True,
            "orders": orders
        })

    except Exception as e:

        print("ACCOUNT ORDERS ERROR:", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)