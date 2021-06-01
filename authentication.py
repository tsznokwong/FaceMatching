
class Authenticator():

  def __init__(self):
    self.user_id = ""

  def isLoggedIn(self):
    return self.user_id != ""

  def login(self, user_id):
    self.user_id = user_id

  def logout(self):
    self.user_id = ""

  def get_user_id(self):
    return self.user_id