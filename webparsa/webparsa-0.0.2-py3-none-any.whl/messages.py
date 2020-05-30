class ParsaInfoMessage:
    """An info message regarding the past element's execution
    """
    def __init__(self, text):
        self.text = text
    
    def __str__(self):
        return f"<Info:{self.text}>"

    def __repr__(self):
        return str(self)

NOT_FOUND = ParsaInfoMessage("Not Found")
MATCH_FAILED = ParsaInfoMessage("Match Failed")
