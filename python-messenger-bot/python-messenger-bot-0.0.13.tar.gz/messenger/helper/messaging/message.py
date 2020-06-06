class Message:

    def __init__(self, **kwargs):
        self.text=''
        self.reply_to_mid=''
        
        return super().__init__(**kwargs)

    def json_to_message(self, json):
        self.text = json['text']
        if json.get('reply_to'):
            self.reply_to_mid=json['reply_to']['mid']