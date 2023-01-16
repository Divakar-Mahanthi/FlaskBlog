from flask import Flask,render_template,request
import sqlite3

app=Flask(__name__)

#home/view all posts
@app.route('/')
def index():
    con=sqlite3.connect('posts.db')
    cur=con.cursor()
    data=cur.execute("select * from posts").fetchall()
    con.commit()
    cur.close()
    con.close()
    return render_template("index.html",data=data)

#create new post
@app.route('/create',methods=["GET","POST"])
def create():
    if request.method=="POST":
        title=request.form.get("title")
        content=request.form.get("content")
        con=sqlite3.connect('posts.db')
        cur=con.cursor()
        cur.execute("insert into posts(title,content) values(?,?)",(title,content))
        con.commit()
        cur.close()
        con.close()
    return render_template("create.html")

#view single post
@app.route('/<int:pid>')
def view_1(pid):
    con=sqlite3.connect('posts.db')
    cur=con.cursor()
    data=cur.execute("select title,content from posts where p_id=?",(pid,)).fetchone()
    con.commit()
    cur.close()
    con.close()
    return render_template("view_1.html",data=data)

#edit post
@app.route('/<int:pid>/edit',methods=["GET","POST"])
def edit(pid):
    con=sqlite3.connect('posts.db')
    cur=con.cursor()
    title=cur.execute("select title from posts where p_id=?",(pid,)).fetchone()
    con.commit()
    cur.close()
    con.close()
    if request.method=="POST":
        n_title=request.form.get("title")
        n_content=request.form.get("content")
        con=sqlite3.connect('posts.db')
        cur=con.cursor()
        cur.execute("update posts set title=?,content=? where p_id=?",(n_title,n_content,pid))
        con.commit()
        cur.close()
        con.close()
    data=[pid,title[0]]
    return render_template("edit.html",data=data)

#delete post
@app.route('/<int:pid>/delete')
def delete(pid):
    con=sqlite3.connect('posts.db')
    cur=con.cursor()
    title=cur.execute("select title from posts where p_id=?",(pid,)).fetchone()
    cur.execute("delete from posts where p_id=?",(pid,))
    con.commit()
    cur.close()
    con.close()
    return render_template("delete.html",data=title[0])
