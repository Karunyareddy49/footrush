from flask import Flask, render_template, request, redirect, session, url_for
from products import products as product_list   # renamed
import os
app = Flask(__name__)
app.secret_key = "secret"


# ---------------- HOME ----------------
@app.route('/')
def index():
    search = request.args.get("search", "")
    category = request.args.get("category", "")

    filtered = product_list

    # ✅ FIXED formatting
    if search:
        filtered = [p for p in filtered if search.lower() in p["name"].lower()]

    if category:
        filtered = [p for p in filtered if p["category"] == category]

    cart_count = len(session.get("cart", []))

    return render_template("index.html", products=filtered, cart_count=cart_count)


# ---------------- ADD TO CART ----------------
@app.route('/add/<int:id>')
def add(id):
    cart = session.get("cart", [])

    cart.append(id)
    session["cart"] = cart

    return redirect(url_for('index'))


# ---------------- CART ----------------
@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    for pid in session.get("cart", []):
        for p in product_list:
            if p["id"] == pid:
                cart_items.append(p)
                total += p["price"]

    return render_template("cart.html", cart_items=cart_items, total=total)


# ---------------- REMOVE FROM CART ----------------
@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    session["cart"] = cart
    return redirect(url_for("cart"))


# ---------------- WISHLIST ----------------
@app.route('/wishlist/<int:id>')
def wishlist(id):
    wishlist = session.get("wishlist", [])

    wishlist.append(id)
    session["wishlist"] = wishlist

    return redirect(url_for('index'))


# ---------------- LOGIN ----------------
users = {}

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if users.get(user) == pwd:
            session["user"] = user
            return redirect(url_for('index'))
        else:
            return "Invalid credentials ❌"

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect(url_for("login"))

    return render_template("signup.html")


# ---------------- CHECKOUT ----------------
@app.route('/checkout')
def checkout():
    return render_template("checkout.html")


# ---------------- NAVIGATION PAGES ----------------
@app.route("/about")
def about():
    return render_template("about.html")


# ✅ FIXED (ONLY ONE PRODUCTS ROUTE)
@app.route("/products")
def products_page():
    return render_template("products.html", products=product_list)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/help")
def help_page():
    return render_template("help.html")


@app.route("/offers")
def offers():
    return render_template("offers.html")



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
