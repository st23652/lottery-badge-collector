from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

BADGES = {
    "win": "🏅",
}

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    badge = ""
    if "badges" not in session:
        session["badges"] = []

    if request.method == "POST":
        user_ticket = request.form.get("ticket", "")
        if len(user_ticket) != 6 or not user_ticket.isdigit():
            message = "Please enter a valid 6-digit ticket number."
        else:
            winning_number = ''.join(str(random.randint(0, 9)) for _ in range(6))
            if user_ticket == winning_number:
                message = f"Congrats! You won a badge! Winning number was {winning_number}."
                session["badges"].append(BADGES["win"])
                session.modified = True
            else:
                message = f"Sorry, no luck. Winning number was {winning_number}."

    return render_template("index.html", message=message, badges=session.get("badges", []))

if __name__ == "__main__":
    app.run(debug=True)
