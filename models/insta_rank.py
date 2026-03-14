from models.comment import Comment

class Insta_Rank:
    def __init__(self,
                 user_id: int,
                 message_id: int,
                 rank: int,
                 num_likes: int,
                 num_comments: int, ):
        self.user_id: int = user_id
        self.message_id: int = message_id
        self.rank: int = rank
        self.num_likes: int = num_likes
        self.num_comments: int = num_comments