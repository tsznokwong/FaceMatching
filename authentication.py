_user_id = ""

def isLoggedIn():
  return _user_id != ""

def login(user_id):
  global _user_id
  _user_id = user_id

def logout():
  global _user_id
  _user_id = ""

def get_user_id():
  return _user_id