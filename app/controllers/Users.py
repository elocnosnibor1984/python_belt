from system.core.controller import *
from time import strftime
import string, random, re
from system.core.model import Model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db
   
    def index(self):
        return self.load_view('index.html')

    def logout(self):
        session.clear()
        return redirect('/')

    def registration(self):
        errors = 0
        name=request.form['name']
        alias=request.form['alias']
        email=request.form['email']
        dob=request.form['dob']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        if len(name)<3:
            errors += 1
            flash("name must be longer than 2 characters")
        if len(email)<1:
            errors += 1
            flash("email cannot be blank")
        if len(alias)<1:
            errors += 1
            flash("email cannot be blank")
        if len(dob)<1:
            errors += 1
            flash("Date of Birth cannot be blank")
        if len(password)<8:
            errors += 1
            flash("password cannot be less than 8 characters")
        if password != confirm_password:
            errors += 1
            flash("passwords don't match!")
        if not EMAIL_REGEX.match(request.form['email']):
            errors += 1
            flash("Invalid Email Address!")
        if errors > 0:
            return redirect('/')
        user={
            'name': name,
            'alias': alias,
            'email': email,
            'dob': dob,
            'password': password
        }
        register=self.models['User'].register_user(user)
        session['user_id']=register
        # flash("You are registered")
        return redirect("/dashboard")

    def login_user(self):
        info={
            'email':request.form['email'],
            'password': request.form['password']
        }
        check_user=self.models['User'].login_user(info)
        if check_user:
            session['user_id']=check_user[0]['user_id']
            return redirect('/dashboard') 
        flash("email or password did not match our records")
        return redirect('/')
