from flask import Flask, url_for, request, send_file

app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        return f"Method POST, value {user}"
    else:
        user = request.args.get("name")
        return f"Method GET, value {user}"
    

@app.errorhandler(404)
def page_not_found(error):
    return "No such page", 404

def main():
    app.run()

if __name__ == "__main__":
    main()