from eve.auth import TokenAuth

from flask import current_app


class RolesAuth(TokenAuth):
    def check_auth(self, token,  allowed_roles, resource, method):
        accounts = current_app.data.driver.db['users']
        lookup = {'token': token}
        if allowed_roles:
            # Only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)
        return account
