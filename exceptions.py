 
class DuplicateUsernameError(Exception):
   
    def __init__(self, message, errors=None):
        super(DuplicateUsernameError, self).__init__(message)
        self.errors = errors


class SpecialCharError(Exception):
    
    def __init__(self, message=None):
        self.message = message
        self.special = ('#', '@', '&', '?', '!', '*', '$')
    def __str__(self):
        return f"Must contain special charachters: {self.special}"