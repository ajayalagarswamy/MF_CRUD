from flask import Flask,render_template,request,url_for,redirect,flash,session
import requests
import sqlite3 as sql



list_1=[]
app=Flask(__name__)

app.secret_key="ajay"

url="https://api.mfapi.in/mf/"

@app.route('/')
def home():
    if "username" in session:
        conn = sql.connect("user.db")
        conn.row_factory = sql.Row
        cur = conn.cursor()
        cur.execute("select * from display where name=?",(session ["username"],))
        data = cur.fetchall()
        return render_template("index.html", datas=data)
    return redirect(url_for('login'))


@app.route('/index',methods=["POST","GET"])
def home1():
    if request.method=="POST":
        name=request.form.get("name")
        fund_house1=request.form.get("fund_house1")
        invested_amount=request.form.get("invested_amount")
        unit_held=request.form.get("unit_held")
        req=requests.get(url+fund_house1)
        data=req.json()
        fund_house1=data["meta"]["fund_house"]
        nav=data["data"][0]["nav"]
        current_value=float(nav)*int(invested_amount)
        growth=float(current_value)-int(unit_held)
        conn=sql.connect("user.db")
        cur = conn.cursor()
        cur.execute("insert into display(name,fund_house1,invested_amount,unit_held,nav,current_value,growth) values(?,?,?,?,?,?,?)",
        (name,fund_house1,invested_amount,unit_held,nav,current_value,growth))
        conn.commit()
        return redirect(url_for("home"))
    return render_template("index.html",datas=list_1)
            

# @app.route('/add_user',methods=["POST","GET"])
# def add_user():
#     if request.method=="POST":
#         name=request.form.get("name")
#         fund_house1=request.form.get("fund_house1")
#         invested_amount=request.form.get("invested_amount")
#         unit_held=request.form.get("unit_held")
#         req=requests.get(url+fund_house1)
#         data2=req.json()
#         fund_house1=data2["meta"]["fund_house"]
#         nav=data2["data"][0]["nav"]
#         current_value=float(nav)*int(invested_amount)
#         growth=float(current_value)-int(unit_held)
#         conn=sql.connect("user.db")
#         cur = conn.cursor()
#         cur.execute("insert into display(name,fund_house1,invested_amount,unit_held,nav,current_value,growth) values(?,?,?,?,?,?,?)",
#         (name,fund_house1,invested_amount,unit_held,nav,current_value,growth))
#         conn.commit()
#         flash("User Created","success")
#         return redirect(url_for("home"))
#     return render_template("add_user.html")

@app.route("/edit_user/<string:id>",methods=["POST","GET"])
def edit_user(id):
    if request.method=="POST":
        name=request.form.get("name")
        fund_house1=request.form.get("fund_house1")
        invested_amount=request.form.get("invested_amount")
        unit_held=request.form.get("unit_held")
        req=requests.get(url+fund_house1)
        data2=req.json()

        fund_house1=data2["meta"]["fund_house"]
        nav=data2["data"][0]["nav"]
        current_value=float(nav)*int(invested_amount)
        growth=float(current_value)-int(unit_held)
        conn=sql.connect("user.db")
        cur = conn.cursor()
        cur.execute("update display set name=?,fund_house1=?,invested_amount=?,unit_held=?,nav=?,current_value=?,growth=? where Id=?",
        (name,fund_house1,invested_amount,unit_held,nav,current_value,growth,id))
        conn.commit()
        # flash("User Updated","success")
        return redirect(url_for("home"))
    conn = sql.connect("user.db")
    conn.row_factory=sql.Row
    cur = conn.cursor()
    cur.execute("select * from display where Id=?",(id,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)

@app.route("/delete-user/<string:id>",methods=["GET"])
def delete_user(id):
    conn=sql.connect("user.db")
    cur= conn.cursor()
    cur.execute("delete from display where Id=?",(id,))
    conn.commit()
    flash("User Deleted","Warning")
    return redirect(url_for("home"))


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        name=request.form.get("name")
        password=request.form.get("password")
        conn=sql.connect("user.db")
        conn.row_factory=sql.Row
        cur=conn.cursor()
        cur.execute("Select * from signup where name=?",(name,))
        data=cur.fetchone()
        if data:
            if  str(data["name"])==name and str(data["password"])==password:
                session["username"]= data["name"]  
        return redirect(url_for("home"))
    flash("User Created","success")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("name",None)
    return redirect(url_for("login"))

@app.route("/signup",methods=["POST","GET"])
def signup():
   if request.method=="POST":
      name=request.form.get("name")
      password=request.form.get("password")
      conn=sql.connect("user.db")
      conn.row_factory=sql.Row
      cur=conn.cursor()
      cur.execute("insert into signup(name,password) values(?,?)",(name,password))
      conn.commit()
      return redirect(url_for('home'))
   return render_template("signup.html")



if __name__ == "__main__":
    app.run(debug=True)
