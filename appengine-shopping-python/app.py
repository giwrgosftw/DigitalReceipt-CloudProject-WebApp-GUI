from flask import Flask, render_template, flash, redirect, url_for, session, logging, request #import flask "enviroment here"
from wtforms import Form, IntegerField, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__) #create an instance of the flask class, name = a placeholder for the current module
app.config['SECRET_KEY'] = 'qwertyuiopasdfghjklzxcvbnmqwertyuiop'

@app.route('/')
def index():
    return render_template('home.html')

#User register
class RegisterForm(Form):
    firstName = StringField('First Name', [validators.Length(min=1)])
    lastName = StringField('Last Name', [validators.Length(min=1)])
    email = StringField('E-mail (e.g. someone@example.com)', [validators.email('Not valid e-mail value (e.g. someone@example.com)')])
    dateOfBirth = StringField('Date of birth (e.g. 12.03.1998)', [validators.Length(min=10,max=10)])
    placeOfBirth = StringField('Place of Birth', [validators.Length(min=1)])
    trailingDigits = IntegerField('Trailing digits of your card (e.g. last 4 figits, 3456)',[validators.NumberRange(min=1000,max=9999)])
    leadingDigits = IntegerField('Leading digits of your card (e.g first 4 digits, 5407)',[validators.NumberRange(min=1000,max=9999)])
    cardType = StringField('Card type', [validators.Length(min=1)])
    startDate = StringField('Start Date of your card (e.g. 08.2012)', [validators.Length(min=7,max=7)])
    expiryDate = StringField('Expiry Date of your card (e.g. 08.2015)', [validators.Length(min=7,max=7)])

#User dashboard
class DashboardForm(Form):
    firstName = StringField('First Name')
    lastName = StringField('Last Name')
    email = StringField('E-mail')
    dateOfBirth = StringField('Date of birth')
    placeOfBirth = StringField('Place of Birth')
    trailingDigits = IntegerField('Trailing digits')
    leadingDigits = IntegerField('Leading digits')
    cardType = StringField('Card type')
    startDate = StringField('Start Date')
    expiryDate = StringField('Expiry Date')

#User request
class SendReceiptForm(Form):
    trailingDigits = IntegerField('Trailing digits of your card (e.g. last 4 digits, 3456)', [validators.NumberRange(min=1000,max=9999)])
    leadingDigits = IntegerField('Leading digits of your card (e.g first 4 digits, 5407)', [validators.NumberRange(min=1000,max=9999)])
    cardType = StringField('Card type', [validators.Length(min=1)])
    expiryDate = StringField('Expiry Date of your card (e.g. 08.2015)', [validators.Length(min=7,max=7)])
    email = StringField('E-mail (e.g. someone@example.com)', [validators.email('Not valid e-mail value (e.g. someone@example.com)')])

#User register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        lastName = request.form['username']
        trailingDigits_candidate = request.form['password']
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#User logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#User request
@app.route('/sendReceipt', methods=['GET','POST'])
def sendReceipt():
    form = SendReceiptForm(request.form)
    if request.method == 'POST' and form.validate():
        flash('The receipt has been sent to your e-mail address', 'success')
        return redirect(url_for('sendReceipt'))
    return render_template('sendReceipt.html', form=form)

# User dashboard
@app.route('/dashboard',methods=['GET','POST'])
#@is_logged_in
def dashboard():
    form = DashboardForm(request.form)
    if request.method == 'POST':
        flash('The receipt has been sent to your e-mail address', 'success')
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html')


if __name__ == '__main__': #check if the script going to be executed
    app.run(debug=True) #start the application, debug-> no need to restart the server, just reload
