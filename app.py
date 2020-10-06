from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jordan:admin@localhost/customer_reviews'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), unique=True)
    last_name = db.Column(db.String(200), unique=True)
    product = db.Column(db.String(200))
    store_location = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, first_name, last_name, product, store_location, rating, comments):
        self.first_name = first_name
        self.last_name = last_name
        self.product = product
        self.store_location = store_location
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        product = request.form['product']
        store_location = request.form['store_location']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer,storelocation,rating,comments)wsa
        if first_name == '' or last_name == '' or store_location == '' or product == '':
            return render_template('index.html', message='Please enter the required field')
        #if db.session.query(Feedback).filter(Feedback.first_name == first_name).count() == 0:
        data = Feedback(first_name, last_name, store_location, rating, comments)
        db.session.add(data)
        db.session.commit()
        send_mail(first_name, last_name, store_location, rating, comments)
        return render_template('success.html')
        #return render_template('index.html', message='We are sorry but, you have already submitted feedback.')

if __name__ == '__main__':
    app.run()
