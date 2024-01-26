# Description: This file is used to create a dataset of words that have the same number of syllables
# For parallel data

import os
import json
import spacy
import nltk
import cmudict

INPUT_DIR = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/"
OUTPUT_DIR = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel_samesyllable/"

def main():
    # read train and val jsonl files
    with open(os.path.join(INPUT_DIR, "train.jsonl"), "r") as f:
        train_jsonl = [json.loads(line) for line in f.readlines()]
    with open(os.path.join(INPUT_DIR, "val.jsonl"), "r") as f:
        val_jsonl = [json.loads(line) for line in f.readlines()]
    train_raw_source = [line["translation"]["en"] for line in train_jsonl]
    train_raw_target = [line["translation"]["ja"] for line in train_jsonl]
    val_raw_source = [line["translation"]["en"] for line in val_jsonl]
    val_raw_target = [line["translation"]["ja"] for line in val_jsonl]

    # count syllables in english:
    en_utils = SyllableCounter()
    train_en_syllables = en_utils.count_syllable_sentence_batch(train_raw_source)
    val_en_syllables = en_utils.count_syllable_sentence_batch(val_raw_source)
    print("train_en_syllables:", train_en_syllables[0:3])
    print("val_en_syllables:", val_en_syllables[0:3])
    # count syllables in japanese:
    ja_utils = SyllableCounterJA()
    train_ja_syllables = ja_utils.count_syllable_sentence_batch(train_raw_target)
    val_ja_syllables = ja_utils.count_syllable_sentence_batch(val_raw_target)
    print("train_ja_syllables:", train_ja_syllables[0:3])
    print("val_ja_syllables:", val_ja_syllables[0:3])

    train_source = []
    train_target = []

    # add sentences with the same number of syllables to train dataset
    for i in range(len(train_raw_source)):
        if train_en_syllables[i] == train_ja_syllables[i]:
            train_source.append(train_raw_source[i])
            train_target.append(train_raw_target[i])

    val_source = []
    val_target = []

    # add sentences with the same number of syllables to val dataset
    for i in range(len(val_raw_source)):
        if val_en_syllables[i] == val_ja_syllables[i]:
            val_source.append(val_raw_source[i])
            val_target.append(val_raw_target[i])
    
    print(f"train: {len(train_source)} lines")
    print(f"val: {len(val_source)} lines")
    assert len(train_source) == len(train_target)
    assert len(val_source) == len(val_target)
    breakpoint()
    with open(os.path.join(OUTPUT_DIR, "train.jsonl"), "w") as f:
        for en_text,ja_text in zip(train_source,train_target):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")
    with open(os.path.join(OUTPUT_DIR, "val.jsonl"), "w") as f:
        for en_text,ja_text in zip(val_source,val_target):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")


# For English
class SyllableCounter:
    d = cmudict.dict()
    # special_word = read_json(os.path.join(os.path.dirname(__file__), 'special_word_syllables.json'))
    with open(os.path.join(os.path.dirname(__file__), 'special_word_syllables.json'), 'r') as f:
        special_word = f.read()
        special_word = json.loads(special_word)
        

    error_word = set()

    @classmethod
    def count_syllable_word(cls, word):
        word = word.strip(" :!?\"")

        if len(word) == 0:
            return 0

        if word in ["'ll", "n't", "'d", ",", "'ve", "'m", "'re", "'s"]:
            return 0

        if len(word) > 2 and word[-2:] == "'s":
            word = word[:-2]
        if word in cls.special_word:
            return cls.special_word[word]
        word = word.lower()
        t = [len(list(y for y in x if y[-1].isdigit())) for x in cls.d[word]]

        if len(t) >= 1:
            ret = t[0]
        else:
            # print(word)
            ret = naive_syllable_count(word)

            # if test == True:
            #     cls.error_word.add(word)
            #     ret = 1
            # else:
            #     print('Exception:', word)
            #     raise Exception
        return ret  # 可能会有多种读音，暂时取第一个

    @classmethod
    def count_syllable_sentence(cls, sentence, test=False, return_list=False):
        try:
            # words = sentence.strip().split(' ')  # this will lead to word combined with punctuation
            # sentence = re.sub("'(\w)+", " ", sentence)
            # words = re.findall(r'\w+', sentence) # I've
            words = nltk.word_tokenize(sentence)
            # print(words)
            # words = [i if i not in cls.special_word else cls.special_word[i] for i in words]
            # print(words)
            # words = [i for i in words if re.search(r'[\w]', i) != None]
            # print(words)
            word_syllables = [cls.count_syllable_word(word.lower().strip()) for word in words]
            # print(word_syllables)

            if return_list == True:  # return results in a list of integers
                ret_t = word_syllables
                ret = []
                for i in ret_t:
                    if i != 0:
                        ret.append(i)
                if len(ret) == 0:
                    ret = [1]
                return ret
            else:
                ret = sum(word_syllables)
                if ret == 0:
                    print('Zero syllable sentence detected!', sentence)
                    ret = 1
                return ret
        except Exception as e:
            raise e
            import traceback
            traceback.print_exc()
            print('The exception sentence:')
            print(sentence)
            exit(10086)

    @classmethod
    def count_syllable_sentence_batch(cls, batch):
        syllables = [cls.count_syllable_sentence(i) for i in batch]
        return syllables

def naive_syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

# For Japanese
class SyllableCounterJA:
    nlp = spacy.load('ja_ginza')
    @classmethod
    def count_syllable_sentence(cls, sentence, test=False, return_list=False):
        small_word = ["ャ","ュ","ョ","ァ","ィ","ゥ","ェ","ォ"]
        try:
            doc = cls.nlp(sentence)
            word_syllables = []
            for token in doc:
                if token.pos_ == 'PUNCT':
                    continue
                num_syllables = 0
                # print(token.morph.get("Reading"))
                if token.morph.get("Reading") == []:
                    continue
                for ch in token.morph.get("Reading")[0]:
                    if not ch in small_word:
                        num_syllables += 1
                word_syllables.append(num_syllables)

            if return_list == True:  # return results in a list of integers
                ret_t = word_syllables
                ret = []
                for i in ret_t:
                    if i != 0:
                        ret.append(i)
                if len(ret) == 0:
                    ret = [1]
                return ret
            else:
                ret = sum(word_syllables)
                if ret == 0:
                    print('Zero syllable sentence detected!', sentence)
                    ret = 1
                return ret
        except Exception as e:
            print('The exception sentence:')
            print(sentence)
            raise e

    @classmethod
    def count_syllable_sentence_batch(cls, batch):
        syllables = [cls.count_syllable_sentence(i) for i in batch]
        return syllables

if __name__ == "__main__":
    main()