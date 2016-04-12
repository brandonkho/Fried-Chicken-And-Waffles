from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User
import requests

@app.route('/')
def main_page():
    
    return render_template("main_page.html")

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




@app.route('/order', methods=['GET', 'POST'])
def order():
  return render_template('order.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    name = request.form['name']
    address = request.form['address']
    phone = request.form['phone']
    city = request.form['city']
    state = request.form['state']
    item = request.form['food']
    quantity = request.form['quantity']

    postmates_key = 'ad79b419-cdc3-4972-8746-0c6985f846c1'

    postmates_url = 'https://api.postmates.com/v1/customers/'

    customer_id = 'cus_KkkOxMyDgB7F7F'

    dropoff_address = '2727 Haste St.'
    dropoff_phone = '909-732-8252'
    dropoff_city = 'Berkeley'
    dropoff_state = 'CA'
    dropoff_name = 'The White House'
    '''
    dropoff_string = '?dropoff_name=' + dropoff_name + '?dropoff_address=' + dropoff_address +dropoff_city + dropoff_state 
    delivery_url = postmates_url + 'customer_id' + '/deliveries' + '?pickup_name=' + name + '?pickup_address=' + address + city + state /
    + dropoff_string + '?manifest=' item + postmates_key
    '''
    delivery_url = postmates_url + customer_id + '/deliveries'
    
    data = {'pickup_name': name, 'pickup_address': address+city+', '+state, 'pickup_phone_number': phone,
    'dropoff_name': dropoff_name, 'dropoff_address': dropoff_address+dropoff_city+', '+dropoff_state, 'dropoff_phone_number': dropoff_phone, 'manifest':item}

    r = requests.post(delivery_url, data=data, auth=(postmates_key, ''))
    


    return render_template('order.html')
