from flask import Flask, render_template

app = Flask(__name__)

max_score = 100
vegetables = [
    {"name": "Zuccini", "score": 72},
    {"name": "Pepper", "score": 99},
    {"name": "Lettuce", "score": 100},
    {"name": "Cucumber", "score": 99},
    {"name": "Tomato", "score": 72},
]

@app.route("/")
def home():
    return render_template("base.html", title="Lettuce")


@app.route("/scoreboard")
def scoreboard():
    context = {
        "board_title": "Vegetables scoreboard",
        "vegetables": vegetables,
        "max_score": max_score,
        "title": "Lettuce"
    }
    return render_template("scoreboard.html", **context)

if __name__ == "__main__":
    app.run()
