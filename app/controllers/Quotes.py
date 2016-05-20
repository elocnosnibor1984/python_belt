from system.core.controller import *
from time import strftime
import string, random, re
from system.core.model import Model
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class Quotes(Controller):
    def __init__(self, action):
        super(Quotes, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db
   
    def dashboard(self):
        user_id=session['user_id']
        alias=self.models['User'].get_alias(user_id)
        quotes=self.models['User'].get_quotes(user_id)
        favorites=self.models['User'].get_favorites(user_id)
        return self.load_view('dashboard.html', alias=alias, quotes=quotes, favorites=favorites)

    def show_user(self, user_id):
        user_id=user_id
        alias=self.models['User'].get_alias(user_id)
        quotes=self.models['User'].get_quotes_by_user(user_id)
        count=self.models['User'].get_count_quotes_by_user(user_id)
        return self.load_view('user.html', alias=alias, quotes=quotes, count=count)

    def add_quote(self):
        author=request.form['author']
        message=request.form['message']
        user_id=request.form['user_id']
        errors=0
        if len(author)<3:
            errors += 1
            flash('Author cannot be less than 3 characters')
        if len(message)<10:
            errors += 1
            flash('Message cannot be less than 10 characters')
        if errors > 1:
            return redirect("/dashboard")
        data={
            'message':message,
            'author':author,
            'user_id':user_id
        }
        add_quote=self.models['User'].add_quote_db(data)
        return redirect('/dashboard')

    def add_to_favorites(self):
        user_id=request.form['user_id']
        quote_id=request.form['quote_id']
        
        data={
            'user_id':user_id,
            'quote_id':quote_id
        }
        add_favorite=self.models['User'].add_favorite_db(data)
        return redirect('/dashboard')

    def remove_from_favorites(self):
        user_id=session['user_id']
        quote_id=request.form['quote_id']
        data={
            'user_id':user_id,
            'quote_id':quote_id
        }
        remove_favorite=self.models['User'].remove_favorite_db(data)
        return redirect('/dashboard')

    
