"""
    Routes Configuration File

    Put Routing rules here
"""
from system.core.router import routes

routes['default_controller'] = 'Users'
routes['/logout'] = 'Users#logout'
routes['POST']['/registration'] = 'Users#registration'
routes['POST']['/login_user'] = 'Users#login_user'

routes['/dashboard'] = 'Quotes#dashboard'
routes['/show_user/<user_id>'] = 'Quotes#show_user'
routes['POST']['/add_quote'] = 'Quotes#add_quote'
routes['POST']['/add_to_favorites'] = 'Quotes#add_to_favorites'
routes['POST']['/remove_from_favorites'] = 'Quotes#remove_from_favorites'
