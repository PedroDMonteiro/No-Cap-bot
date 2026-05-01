from cogs.insta.models.comment import Comment

class Insta:
    def __init__(self,
                 user_id: int,
                 message_id: int,
                 extension: str,
                 rank: int = None,
                 likes: list[int] = [],
                 comments: list[Comment] = []):
        self.user_id:int = user_id
        self.message_id: int = message_id
        self.extension: str = extension
        self.rank = rank
        self.likes: list[int] = likes
        self.comments: list[Comment] = comments

    
    def num_likes(self, ) -> int:
        return len(self.likes)
    
    def num_comments(self, ) -> int:
        return len(self.comments)
    
    def __eq__(self, other):
        if not isinstance(other, Insta):
            return NotImplemented
        
        return self.message_id == other.message_id
    
    def __lt__(self, other):
        if not isinstance(other, Insta):
            return NotImplemented
        
        if self.num_likes() == other.num_likes():
            return self.num_comments() < other.num_comments()
        
        return self.num_likes() < other.num_likes()