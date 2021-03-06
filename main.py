"""build-a-blog"""
from flask import Flask,request,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256))
    body = db.Column(db.Text())

    def __init__ (self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def inxex():
    return redirect('blog')

@app.route('/blog')
def blog():
    blog = Blog.query.all()
    blog_id = request.args.get('id')
    if blog_id:
        x = Blog.query.filter_by(id = blog_id).first()
        return render_template('blog.html', blog = x)
    return render_template('index.html', blog = blog)

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    error = ''
    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        error_1 = ""
        error_2 = ""
        if not title:
            error_1 = "Please add a title"
        if not post:
            error_2 = "Please add a post"
        if not title or not post:
            return render_template('submit.html', error_1 = error_1, error_2 = error_2)
        else:
            new_blog = Blog(title, post)
            db.session.add(new_blog)
            db.session.commit()
            blog_id = './blog?id='+str(new_blog.id)
            return redirect(blog_id)
    
    return render_template('submit.html', error = error)

if __name__ == '__main__':
    app.run()