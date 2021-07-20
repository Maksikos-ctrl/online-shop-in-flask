from flask import Flask, render_template, url_for, request, redirect 
from flask_sqlalchemy import SQLAlchemy
#import create_db
#from flaskext.mysql import MySQL пробуй.
#import pymysql 
import os
from cloudipsp import Api, Checkout # https://github.com/cloudipsp/python-sdk




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://max:maksikos973@umilitary.ml/max' # You can choose another BD, for example: sqllite(testBD), PostgresSQL etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # it says us that we can execute changes with BD
db = SQLAlchemy(app)


# BD - Tables - Notes
# Table:
# id    title   price  isActive
# 1     Some     100    True
# 2     Some2    200    False
# 3     Some3    300    True


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True) # если ми добавим primary_key=True, то значит что это поле будет проставлятьсо в автоматическом порядке
    title = db.Column(db.String(100), nullable=False) # nullable=False значит что это поле не может быть пустим
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True) # Значение по умолчанию
    #text = db.Column(db.Text, nullable=False)


    def __repr__(self): # Returns a string as a representation of the object.
        return self.title




@app.route('/')
@app.route('/homepage')
def homepage(): 
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)



@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/buy/<int:id>')
def buy_good(id):
    item = Item.query.get(id) 

    api = Api(merchant_id=1396424,   # create an object basing on API class 
            secret_key='test') # default id and secret_key.You can choose you own id and test from https://fondy.ua, after auth
    checkout = Checkout(api=api)
    data = {
        "currency": "UAH", # you can choose here your country currency
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create-good', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "На жаль при доданні статті сталася помилка....SAS"    # You can add here render_template on "404" page.
    else:    
        return render_template('create.html')    


if __name__ == "__main__":  # проверка чтобы наш файл имел только название main
    port = int(os.environ.get("PORT", 5000))  #хероку не разрешает порт напрямую, его нужно получить с аргументов командной строки
    app.run(host='0.0.0.0', debug=True, port=port)#на фолс поменяй потом