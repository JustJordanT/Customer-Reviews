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
    customer = db.Column(db.String(200), unique=True)
    storelocation = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, storelocation, rating, comments):
        self.customer = customer
        self.storelocation = storelocation
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        storelocation = request.form['storelocation']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer,storelocation,rating,comments)wsa
        if customer == '' or storelocation == '':
            return render_template('index.html', message='Please enter the required field')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, storelocation, rating, comments)
            db.session.add(data)
            db.session.commit()
            #send_mail(customer, storelocation, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='We are sorry but, you have already submitted feedback.')

if __name__ == '__main__':
    app.run()
