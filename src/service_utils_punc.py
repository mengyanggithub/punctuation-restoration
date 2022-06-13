import re
import torch
from model import DeepPunctuation
from config import *

tokenizer = MODELS["bert-base-multilingual-uncased"][1].from_pretrained("bert-base-multilingual-uncased")
token_style = MODELS["bert-base-multilingual-uncased"][3]

deep_punctuation = DeepPunctuation("bert-base-multilingual-uncased", freeze_bert=True, lstm_dim=-1)

deep_punctuation.load_state_dict(torch.load("./out/weights.pt"))
deep_punctuation.eval()

def punc_restore(query):
    text = query
    text = re.sub(r"[,:\-–.!;?，。！]", '', text)
    words_original_case = [char for char in text.strip()]
    words = words_original_case

    word_pos = 0
    sequence_len = 64
    result = ""
    decode_idx = 0
    punctuation_map = {0: '', 1: '，', 2: '。', 3: '?'}

    while word_pos < len(words):
        x = [TOKEN_IDX[token_style]['START_SEQ']]
        y_mask = [1]

        while len(x) < sequence_len and word_pos < len(words):
            tokens = tokenizer.tokenize(words[word_pos])
            if len(tokens) + len(x) >= sequence_len:
                break
            else:
                for i in range(len(tokens) - 1):
                    x.append(tokenizer.convert_tokens_to_ids(tokens[i]))
                    y_mask.append(0)
                x.append(tokenizer.convert_tokens_to_ids(tokens[-1]))
                y_mask.append(1)
                word_pos += 1
        x.append(TOKEN_IDX[token_style]['END_SEQ'])
        y_mask.append(0)
        if len(x) < sequence_len:
            x = x + [TOKEN_IDX[token_style]['PAD'] for _ in range(sequence_len - len(x))]
            y_mask = y_mask + [0 for _ in range(sequence_len - len(y_mask))]
        attn_mask = [1 if token != TOKEN_IDX[token_style]['PAD'] else 0 for token in x]

        x = torch.tensor(x).reshape(1,-1)
        y_mask = torch.tensor(y_mask)
        attn_mask = torch.tensor(attn_mask).reshape(1,-1)
    
    with torch.no_grad():
        y_predict = deep_punctuation(x, attn_mask)
        y_predict = y_predict.view(-1, y_predict.shape[2])
        y_predict = torch.argmax(y_predict, dim=1).view(-1)

    for i in range(1,y_mask.shape[0]):
        if y_mask[i] == 1:
            result += words_original_case[decode_idx] + punctuation_map[y_predict[i].item()]
        decode_idx += 1
    
    return result