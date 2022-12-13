import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT symbol, SUM(shares) AS shares, price, SUM(price) as total_price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
    cash = float(cash_db[0]["cash"])
    stock_value = 0.0
    current_stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
    for row in current_stocks:
        stock = lookup(row["symbol"].upper())
        stock_value += row["shares"] * stock["price"]
    total = cash + stock_value
    return render_template("index.html", database = transactions_db, cash = cash, total = total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Please input valid stock")
        if not symbol:
            return apology("Please input valid symbol")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Symbol does not exist")
        if shares <= 0:
            return apology("Please buy at least 1 share")
        transaction_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        if user_cash < transaction_value:
            return apology("Insufficient funds")

        update_cash = user_cash - transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, stock["symbol"], shares, stock["price"], date)

        flash("Stock successfully purchased")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions = transactions_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please input valid symbol")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("Symbol does not exist")
        return render_template("quoted.html", name = stock["name"], price = stock["price"], symbol = stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please input username")
        if not password:
            return apology("Please input password")
        if not confirmation:
            return apology("Please input confirmation password")
        if password != confirmation:
            return apology("Passwords do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")

        session["user_id"] = new_user

        return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", user_id)
        return render_template("sell.html", symbols = [row["symbol"] for row in symbols_user])

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock = lookup(symbol.upper())
        if shares < 0:
            return apology("Please buy at least 1 share")

        transaction_value = shares * stock["price"]
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = :id", id=user_id)
        user_cash = user_cash_db[0]["cash"]

        user_shares = db.execute("SELECT SUM(shares) as shares FROM transactions WHERE user_id =? AND symbol = ? GROUP BY symbol", user_id, symbol)
        user_shares_real = user_shares[0]["shares"]
        if shares > user_shares_real:
            return apology("Insufficient shares.")

        update_cash = user_cash + transaction_value
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES (?, ?, ?, ?, ?)", user_id, stock["symbol"], (-1)*shares, (-1)*stock["price"], date)

        flash("Stock successfully sold")
        return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change password"""
    if request.method == "GET":
        return render_template("change_password.html")

    else:
        username = request.form.get("username")
        old_pass = request.form.get("password")
        new_pass = request.form.get("newpass")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Please input username")
        if not old_pass:
            return apology("Please input old password")
        if not new_pass:
            return apology("Please input new password")
        if not confirmation:
            return apology("Please confirm new password")
        if new_pass != confirmation:
            return apology("New passwords do not match")

        user_id = session["user_id"]

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old_pass):
            return apology("invalid username and/or password", 403)

        new_hash = generate_password_hash(new_pass)

        db.execute("UPDATE users SET hash = ? WHERE username = ?", new_hash, username)

        flash("Password updated")

        return redirect("/")