from models.comment import Comment

class Insta:
    def __init__(self,
                 user_id: int,
                 message_id: int,
                 likes: list[int] = [],
                 comments: list[Comment] = []):
        self.user_id:int = user_id
        self.message_id: int = message_id
        self.likes: list[int] = likes
        self.comments: list[Comment] = comments