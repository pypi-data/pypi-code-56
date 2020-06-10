from transformers import AutoModelForQuestionAnswering, AutoTokenizer
from soco_mrc.cloud_bucket import CloudBucket
import os
import torch
import re
from soco_mrc import util
import logging
logging.getLogger("transformers.tokenization_utils").setLevel(logging.ERROR)

class MRCModel(object):
    RESOURCE_PATH = os.path.join.__name__

    def __init__(self, region, use_gpu=False, max_answer_length=64):
        if use_gpu and torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        self.region = region
        self.cloud_bucket = CloudBucket(region)
        self._models = dict()
        self.max_answer_length = max_answer_length

    def _load_model(self, model_id):
        # a naive check. if too big, just reset
        if len(self._models) > 20:
            self._models = dict()

        if model_id not in self._models:
            self.cloud_bucket.download_model('mrc-models', model_id)
            path = os.path.join('resources', model_id)
            model = AutoModelForQuestionAnswering.from_pretrained(path)
            tokenizer = AutoTokenizer.from_pretrained(path, use_fast=True)
            model.to(self.device)

            self._models[model_id] = (tokenizer, model)

        return self._models[model_id]

    def _normalize_text(self, text):
        return re.sub('\s+', ' ', text)

    def batch_predict(self, model_id, data, n_best_size=1):
        tokenizer, model = self._load_model(model_id)

        features = []
        for d in data:
            doc = self._normalize_text(d['doc'])
            q = self._normalize_text(d['q'])
            temp = tokenizer.encode_plus(q, doc, return_offsets_mapping=True)
            temp['doc'] = doc
            temp['q'] = q
            features.append(temp)

        results = []
        for batch in util.chunks(features, 10):
            max_len = max([len(f['input_ids']) for f in batch])
            for f in batch:
                f_len = len(f['input_ids'])
                f['length'] = f_len
                f['input_ids'] = f['input_ids'] + [0] * (max_len - f_len)
                f['token_type_ids'] = f['token_type_ids'] + [0] * (max_len - f_len)
                f['attention_mask'] = f['attention_mask'] + [0] * (max_len - f_len)

            input_ids = [f['input_ids'] for f in batch]
            token_type_ids = [f['token_type_ids'] for f in batch]
            attn_masks = [f['attention_mask'] for f in batch]

            with torch.no_grad():
                start_scores, end_scores = model(torch.tensor(input_ids).to(self.device),
                                                 token_type_ids=torch.tensor(token_type_ids).to(self.device),
                                                 attention_mask=torch.tensor(attn_masks).to(self.device))
                start_probs = torch.softmax(start_scores, dim=1)
                end_probs = torch.softmax(end_scores, dim=1)

            for b_id in range(len(batch)):
                all_tokens = tokenizer.convert_ids_to_tokens(input_ids[b_id])
                legal_length = batch[b_id]['length']
                b_start_score = start_scores[b_id][0:legal_length]
                b_end_score = end_scores[b_id][0:legal_length]
                token2char = batch[b_id]['offset_mapping']
                for t_id in range(legal_length):
                    if token2char[t_id] is None:
                        b_start_score[t_id] = -10e10
                        b_end_score[t_id] = -10e10

                _, top_start_id = torch.topk(b_start_score, 2, dim=0)
                _, top_end_id = torch.topk(b_end_score, 2, dim=0)

                s_prob = start_probs[b_id, top_start_id[0]].item()
                e_prob = end_probs[b_id, top_end_id[0]].item()
                s_logit = start_scores[b_id, top_start_id[0]].item()
                e_logit = end_scores[b_id, top_end_id[0]].item()

                prob = (s_prob + e_prob) / 2
                score = (s_logit + e_logit) / 2

                doc = batch[b_id]['doc']
                doc_offset = input_ids[b_id].index(102)

                res = all_tokens[top_start_id[0]:top_end_id[0] + 1]
                char_offset = token2char[doc_offset+1][0]

                if not res or res[0] == "[CLS]" or res[0] == '[SEP]':
                    # ans = helper.get_ans_span(all_tokens[top_start_id[1]:top_end_id[1] + 1])
                    prediction = {'missing_warning': True,
                                  'prob': prob,
                                  'start_end_prob': [s_prob, e_prob],
                                  'score': score,
                                  'start_end_score': [s_logit, e_logit],
                                  'value': "", 'answer_start': -1}
                else:
                    # ans = helper.get_ans_span(res)
                    start_map = token2char[top_start_id[0].item()]
                    end_map = token2char[top_end_id[0].item()]
                    span = [start_map[0] - char_offset, end_map[1] - char_offset]
                    ans = doc[span[0]: span[1]]

                    prediction = {'value': ans,
                                  'answer_start': span[0],
                                  'answer_span': span,
                                  'prob': prob,
                                  'start_end_prob': [s_prob, e_prob],
                                  'score': score,
                                  'start_end_score': [s_logit, e_logit],
                                  'tokens': res}

                results.append(prediction)

        return results

if __name__ == '__main__':
    use_gpu = False
    model = MRCModel('us', use_gpu=use_gpu)
    data = [
        {'q': 'Who is Jack?', 'doc': 'Jack is a programmer. He is tall.'},
        {'q': 'Who is tall?', 'doc': 'Jack is a programmer. He is tall.'},
        {'q': 'How to cook pasta?', 'doc': 'Jack is a programmer. He is tall.'}

    ]
    res = model.batch_predict('spanbert-large-squad2', data)
    print(res)

    data = [
        {'q': '张三是谁？', 'doc': '张三是一个铁匠。他很高。'},
        {'q': '谁很高？', 'doc': '张三是一个铁匠。他很高。'},
        {'q': '如何开飞机？', 'doc': '张三是一个铁匠。他很高。'}

    ]
    res = model.batch_predict('roberta-base-chinese-cmrc', data)
    print(res)
