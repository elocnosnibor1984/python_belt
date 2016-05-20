
from system.core.model import Model

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def register_user(self, user):
        password = user['password']
        password_hash=self.bcrypt.generate_password_hash(password)
        query="INSERT INTO users (name, alias, email, password, dob, created_at, updated_at) values (:name, :alias, :email, :password, :dob, NOW(), NOW())"
        data = {'name': user['name'], 'alias': user['alias'], 'email':user['email'], 'password':password_hash, 'dob':user['dob']}
        return self.db.query_db(query,data)

    def login_user(self, info):
        password=info['password']
        query="Select * from users where email=:email"
        data = {'email':info['email']}
        data_to_check=self.db.query_db(query,data)

        if data_to_check:
            check = self.bcrypt.check_password_hash(data_to_check[0]['password'], password)
            return data_to_check
        return False

    def get_alias(self, user_id):
        user_id=user_id
        query="Select alias from users where user_id=:user_id"
        data = {'user_id':user_id}
        return self.db.query_db(query,data)

    def get_quotes(self, user_id):
        user_id=user_id
        # query="Select * from quotes join users on quotes.user_id = users.user_id left join favorites on quotes.quote_id=favorites.quote_id where favorites.user_id != :user_id"
        query="select * from quotes join users on quotes.user_id=users.user_id where quote_id not in(Select favorites.quote_id from favorites left join users on favorites.user_id = users.user_id join quotes on quotes.quote_id=favorites.quote_id where favorites.user_id =:user_id)"
        data = {'user_id':user_id}
        return self.db.query_db(query,data)

    def get_quotes_by_user(self, user_id):
        user_id=user_id
        query="Select * from quotes join users on quotes.user_id = users.user_id where users.user_id=:user_id"
        data = {'user_id':user_id}
        return self.db.query_db(query,data)

    def get_count_quotes_by_user(self, user_id):
        user_id=user_id
        query="Select count(users.user_id) as num from quotes join users on quotes.user_id = users.user_id where users.user_id=:user_id"
        data = {'user_id':user_id}
        return self.db.query_db(query,data)

    def get_favorites(self, user_id):
        user_id=user_id
        query="Select * from favorites left join users on favorites.user_id = users.user_id join quotes on quotes.quote_id=favorites.quote_id where favorites.user_id =:user_id"
        data = {'user_id':user_id}
        return self.db.query_db(query,data)

    def add_quote_db(self, info):
        query="Insert into quotes (author, message, user_id, created_at, updated_at) Values (:author, :message, :user_id, NOW(), NOW())"
        data = {'author':info['author'], 'message':info['message'], 'user_id':info['user_id']}
        return self.db.query_db(query,data)

    def add_favorite_db(self, info):
        query="Insert into favorites (quote_id, user_id) Values (:quote_id, :user_id)"
        data = {'quote_id':info['quote_id'],'user_id':info['user_id']}
        return self.db.query_db(query,data)

    def remove_favorite_db(self, info):
        query="Delete from favorites where user_id=:user_id and quote_id=:quote_id"
        data = {'quote_id':info['quote_id'],'user_id':info['user_id']}
        return self.db.query_db(query,data)
