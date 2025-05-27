from uuid import uuid4 as uuid
class User:
    def __init__(self, id: uuid, name: str, surname: str,  email: str, password: str):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password

    def __repr__(self):
        return f"User(username={self.username}, email={self.email})"
    
    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email
        }