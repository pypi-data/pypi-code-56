import json

from .constant import Constant
from messenger.helper import Utils
from messenger.helper.messaging import ButtonTemplate, Message, Postback, QuickReply, Receipt, Response#, GenericTemplate, ReceiptElement, ReceiptAdjustment
from messenger.helper.http import Post

class Bot:
    def __init__(self, page_access_token, **kwargs):
        self.post = Post(page_access_token)

    def unpack_messenger_json(self, json):
        utils = Utils()
        chat_id, chat_time, sender_psid, event = utils.messenger_to_var(json)

        return chat_id, chat_time, sender_psid, event

    def unpack_thread_context_json(self, json):
        utils = Utils()
        psid, signed_request, thread_type, tid = utils.thread_context_to_var(json)

        return psid, signed_request, thread_type, tid

    def upload_attachment_file(self, log, sender_psid, file):
        response = Response()
        response.recipient_psid = sender_psid
        message, filestream = response.upload_attachment_file(file)
        
        attachment_json = self.post.send_multipart(Constant.attachment_api, message, filestream)
        log.info('%s: %s' % ('upload_attachment_file', attachment_json))

        return attachment_json
    
    def send_attachment_asset(self, log, sender_psid, attachment_id):
        response = Response()
        response.recipient_psid = sender_psid
        response_text = response.send_attachment_asset(attachment_id)
        
        log.info('%s: %s' % ('send_attachment_asset', self.post.send(Constant.send_api, response_text)))

    def send_attachment_file(self, log, sender_psid, file):
        response = Response()
        response.recipient_psid = sender_psid
        response_text = response.send_attachment_file(file)
        
        log.info('%s: %s' % ('send_attachment_file', self.post.send(Constant.send_api, response_text)))

    def send_button_template(self, log, sender_psid, button_template):
        response = Response()
        response.recipient_psid = sender_psid
        response_text = response.send_button_template(button_template)
        
        log.info('%s: %s' % ('send_button_template', self.post.send(Constant.send_api, response_text)))
                
    def send_generic_template(self, log, sender_psid, generic_template):
        response = Response()
        response.recipient_psid = sender_psid
        response_text = response.send_generic_template(generic_template)
        
        log.info('%s: %s' % ('send_generic_template', self.post.send(Constant.send_api, response_text)))

    def send_message(self, log, sender_psid, text):
        response = Response()
        response.recipient_psid = sender_psid
        response.text = text
        response_text = response.send_message()
        
        resp = self.post.send(Constant.send_api, response_text)
        log.info('%s: %s' % ('send_message', resp))

        return json.loads(resp)

    def send_quick_reply(self, log, sender_psid, text, quick_reply):
        response = Response()
        response.recipient_psid = sender_psid        
        response.text = text
        response_text = response.send_quick_reply(quick_reply)
        
        log.info('%s: %s' % ('send_quick_reply', self.post.send(Constant.send_api, response_text)))
        
    def send_receipt(self, log, sender_psid, receipt):
        response = Response()     
        response.recipient_psid = sender_psid
        response_text = response.send_receipt(receipt)
        
        log.info('%s: %s' % ('send_receipt', self.post.send(Constant.send_api, response_text)))

    def send_sender_action(self, sender_psid, log, sender_action):
        response = Response()
        response.recipient_psid = sender_psid
        
        response_text = response.send_sender_action(sender_action)

        log.info('%s: %s' % ('send_sender_action', self.post.send(Constant.send_api, response_text)))