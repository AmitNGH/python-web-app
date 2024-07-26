from datetime import datetime


class User:
    def __init__(self, user_id, user_name, creation_date=False):
        self.user_id = user_id
        self.user_name = user_name
        if creation_date:
            self.creation_date = creation_date
        else:
            self.creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
