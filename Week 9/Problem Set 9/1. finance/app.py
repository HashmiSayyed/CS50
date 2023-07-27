import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

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
    res = db.execute("SELECT * FROM users_data WHERE user_id = ?", session["user_id"])

    g_total = 0.0
    shares_data = []
    for item in res:
        lookup_res = lookup(item["symbol"])
        total = (lookup_res["price"] * int(item["nos"]))
        new_dic = {"symbol": lookup_res["symbol"], "name": lookup_res["name"], "shares": item["nos"], "price": usd(lookup_res["price"]), "total": usd(total)}
        shares_data.append(new_dic)
        g_total += total

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = float(cash[0]["cash"])
    g_total += cash
    data = {"shares_data": shares_data, "cash": usd(cash), "g_total": usd(g_total)}
    return render_template("index.html", data=data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol or not shares:
            return apology("symbol & number of shares is required")
        elif int(shares) < 1:
            return apology("please enter positive integer")

        res = lookup(symbol)

        if not res:
            return apology("symbol is not valid")

        total = int(shares) * res["price"]
        bal = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

        if total > bal[0]["cash"]:
            return apology("you don't have enough cash")
        else:
            new_bal = bal[0]["cash"] - total
            db.execute("INSERT INTO history (user_id, type, symbol, price, nos) VALUES (?, ?, ?, ?, ?)", session["user_id"], "buy", symbol, total, shares)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_bal, session["user_id"])
            lst = db.execute("SELECT * FROM users_data WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
            if len(lst) == 0:
                db.execute("INSERT INTO users_data (user_id, symbol, nos) VALUES (?, ?, ?)", session["user_id"], symbol, shares)
            else:
                old_nos = db.execute("SELECT nos FROM users_data WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
                new_nos = int(old_nos[0]["nos"]) + int(shares)
                db.execute("UPDATE users_data SET nos = ? WHERE user_id = ? AND symbol = ?", new_nos, session["user_id"], symbol)
            return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    res = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])

    data = []
    for item in res:
        lookup_res = lookup(item["symbol"])
        name = lookup_res["name"]
        total = float(item["price"]) * int(item["nos"])
        dic = {"type": item["type"], "symbol": item["symbol"], "name": name, "price": usd(item["price"]), "nos": item["nos"], "total": usd(total), "time": item["time"]}
        data.append(dic)

    return render_template("history.html", data=data)


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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol required.")

        res = lookup(symbol)
        if not res:
            return apology("Invalid Symbol.")

        dlrs = usd(res["price"])

        return render_template("quoted.html", data=dlrs)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        un = request.form.get("username")
        h = generate_password_hash(request.form.get("password"))
        list = db.execute("SELECT * FROM users WHERE username = ?", un)

        if not request.form.get("username") or len(list) != 0:
            return apology("Username not given or already exists.")

        if not request.form.get("password") or request.form.get("password") != request.form.get("confirmation"):
            return apology("Password not given or don't match with confirmation.")

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", un, h)

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("Symbol required")

        if int(shares) < 1:
            return apology("please enter positive integer")

        users_nos = db.execute("SELECT nos FROM users_data WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        users_nos = users_nos[0]["nos"]
        users_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        users_cash = users_cash[0]["cash"]

        if int(shares) > int(users_nos):
            return apology("You have less shares then you entered")
        else:
            lookup_res = lookup(symbol)
            val = float(lookup_res["price"]) * int(shares)
            new_cash = val + float(users_cash)
            new_nos = int(users_nos) - int(shares)

            db.execute("INSERT INTO history (user_id, type, symbol, price, nos) VALUES (?, ?, ?, ?, ?)", session["user_id"], "sell", symbol, val, shares)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

            if new_nos == 0:
                db.execute("DELETE FROM users_data WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
            else:
                db.execute("UPDATE users_data SET nos = ? WHERE user_id = ? AND symbol = ?", new_nos, session["user_id"], symbol)

            return redirect("/")

    else:
        smbls = db.execute("SELECT symbol FROM users_data WHERE user_id = ?", session["user_id"])
        return render_template("sell.html", smbls=smbls)