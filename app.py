from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from forms import LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///blog.db"
app.config["SQLALCHEMY_TRECK_MODIFICATIONS"]=False
db =SQLAlchemy(app)


class Article(db.Model):                           # создаем колонки таблицы базы данных
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    intro = db.Column(db.String(300),nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):                         #указіваем какое значение возвращаем с базы данных
        return "<Article %r>" % self.id


class Tasks(db.Model):                           # создаем колонки таблицы базы данных
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), nullable=False)
    text_task = db.Column(db.String(300),nullable=False)
    answer = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):                         #указіваем какое значение возвращаем с базы данных
        return "<Tasks %r>" % self.id


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True) # создаем колонки таблицы базы данных
    hireUsFormFirstName = db.Column(db.String(20), nullable=False)
    hireUsFormLasttName = db.Column(db.String(29), nullable=False)
    hireUsFormWorkEmail = db.Column(db.String(50), nullable=False)
    hireUsFormPhone = db.Column(db.String(20),nullable=False)
    hireUsFormDetails = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default= datetime.utcnow)

    def __repr__(self):                         #указіваем какое значение возвращаем с базы данных
        return "<Contact %r>" % self.id




@app.route("/")  # що відкриваеться
@app.route("/home")
@app.route("/home/new")
def index():
    return render_template("index.html")


@app.route("/form")
def form():
    return render_template("form.html")



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/user/<string:name>/<int:id>")
def user(name,id):
    return "Welcome: "+name+" - "+str(id)


@app.route("/<string:admin>/<string:login>/<int:id>")
def admin(admin,login,id):
    return "Welcome: " +admin+ " - "+login+"-" +str(id)



@app.route("/blog/news")
@app.route("/blog/<int:id>/news")
def news(id):
    return "All news for you: " +str(id)
#/admin-login/id»


@app.route("/posts")
def posts():
    articles=Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>/del")
def post_delete(id):
    article=Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/posts")

    except:
        return "При відаленні сталася помилка"









@app.route("/posts/<int:id>")
def post_detail(id):
    article=Article.query.get(id)
    return render_template("post_detail.html", article=article)





@app.route("/posts/<int:id>/update", methods=["POST","GET"])
def post_update(id):
    article=Article.query.get(id)
    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]

        try:

            db.session.commit()
            return redirect("/posts")

        except:
            return ("При редагуванні виникла помилка ")
    else:
        return render_template("post_update.html", article=article)




@app.route("/create-article", methods=["POST","GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Article(title =title, intro=intro, text=text )

        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/posts")

        except:
            return ("При додаванні виникла помилка ")
    else:
        return  render_template("create-article.html")


#_____________________________________________________________________________




@app.route("/create-test", methods=["POST","GET"])
def create_test():
    if request.method == "POST":
        task_name = request.form["task_name"]
        text_task = request.form["text_task"]
        answer = request.form["answer"]
        tasks= Tasks(task_name = task_name, text_task = text_task, answer = answer )


        try:
            db.session.add(tasks)
            db.session.commit()
            return redirect("/")

        except:
            return ("При додаванні виникла помилка ")
    else:
        return render_template("create-test.html")


@app.route("/tasks")
def pos_test():
    tasks = Tasks.query.order_by(Tasks.date.desc()).all()
    return render_template('tasks.html', tasks=tasks)


@app.route("/tasks/<int:id>")
def test_ditail(id):
    tasks = Tasks.query.get(id)

    return render_template('tasks_detail.html', task=tasks)





#_____________________________________________________________________________
"""
@app.route("/contact", methods=["POST","GET"])
def contact():
    if request.method == "POST":
        hireUsFormFirstName = request.form["hireUsFormFirstName"]
        hireUsFormLasttName = request.form["hireUsFormLasttName"]
        hireUsFormWorkEmail = request.form["hireUsFormWorkEmail"]
        hireUsFormPhone = request.form["hireUsFormPhone"]
        hireUsFormDetails = request.form["hireUsFormDetails"]

        contact= Contact(hireUsFormFirstName = hireUsFormFirstName, hireUsFormLasttName = hireUsFormLasttName, hireUsFormWorkEmail = hireUsFormWorkEmail, hireUsFormPhone=hireUsFormPhone, hireUsFormDetails=hireUsFormDetails)


        try:
            db.session.add(contact)
            db.session.commit()
            return redirect("/")

        except:
            return ("При додаванні виникла помилка ")
    else:
        return render_template("contact.html")


@app.route("/cont")
def cont_test():
    contact = Contact.query.order_by(Contact.date.desc()).all()
    return render_template('cont.html', contact=contact)


@app.route("/cont/<int:id>")
def cont_ditail(id):
    contact = Contact.query.get(id)

    return render_template('contact_detail.html', contac=contact)"""

#_____________________________________________________________________________




"""@app.route("/login",methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    return render_tamplate("login.html", menu =db.getMenu(), title = "Avtoriza",)"""
    # if request.method == "POST":
    #     user = dbase.getUserByEmail(request.form['email']
    #     if user and check_password_hash(user['psw'], request.form['psw']):
    #         userlogin = UserLogin().create(user)
    #         rm =True if request.form.get('remainme') else False
    #         Login_user(userlogin, remember=rm)
    #         return redirect(request.args.get("next") or url_for("profile"))
    #     flash("НЕ верная пара логин пароль", "error")
    #
    # return render_template("Login.html", menu=dbase.getMenu(), title="ABTopn3auna")




if __name__ == "__main__":
    app.run(debug=True)
