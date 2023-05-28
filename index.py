from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__, template_folder='template')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            mobilenumber = request.form["mobilenumber"]
            with sqlite3.connect("user.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT into Employees (name, email, mobilenumber) values (?,?,?)", (name, email, mobilenumber))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id):
    con = sqlite3.connect("user.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""SELECT * FROM Employees WHERE id = ?""", (id,))
    rows = cur.fetchall()
    return render_template("edit.html", rows=rows)


@app.route("/update", methods=["POST", "GET"])
def update():
    id = request.form["id"]
    name = request.form["name"]
    email = request.form["email"]
    mobilenumber = request.form["mobilenumber"]
    con = sqlite3.connect("user.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""UPDATE Employees SET name = ?, email = ?, mobilenumber = ? WHERE id = ? """,
                (name, email, mobilenumber, id))
    con.commit()
    return redirect("/view")


@app.route("/view")
def view():
    con = sqlite3.connect("user.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    print(id)
    con = sqlite3.connect("user.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("""DELETE FROM Employees WHERE id = ?""", (id,))
    con.commit()
    return redirect("/view")


if __name__ == "__main__":
    app.run(debug=True)
