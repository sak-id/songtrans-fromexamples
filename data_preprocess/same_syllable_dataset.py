# Description: This file is used to create a dataset of words that have the same number of syllables
# For parallel data

import os
import json
import spacy
import nltk
import cmudict

INPUT_DIR = "/raid/ieda/trans_jaen_dataset/Data/source_data/data_parallel/"
OUTPUT_DIR = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel_samesyllable/"

def main():
    with open(os.path.join(INPUT_DIR, "shuffled_full.source"), "r") as f:
        source_texts = f.readlines()
    with open(os.path.join(INPUT_DIR, "shuffled_full.target"), "r") as f:
        target_texts = f.readlines()
    assert len(source_texts) == len(target_texts)
    print("len(source_texts):", len(source_texts))
    
    # count syllables in english:
    en_lens = SyllableCounter.count_syllable_sentence_batch(source_texts)
    print("en_lens:", en_lens[0:3])
    print("len(en_lens):", len(en_lens))
    # count syllables in japanese:
    ja_lens = SyllableCounterJA.count_syllable_sentence_batch(target_texts)
    print("ja_lens:", ja_lens[0:3])
    print("len(ja_lens):", len(ja_lens))

    en_dataset = [] # list of sentences with the same number of syllables
    ja_dataset = []
    for i in range(len(source_texts)):
        if en_lens[i] == ja_lens[i]:
            en_dataset.append(source_texts[i])
            ja_dataset.append(target_texts[i])
    print("len(en_dataset):", len(en_dataset))
    breakpoint()
    with open(os.path.join(OUTPUT_DIR, "full.jsonl"), "w") as f:
        for en_text,ja_text in zip(en_dataset,ja_dataset):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")

    len_source = len(en_dataset)
    len_target = len(ja_dataset)
    assert len_source == len_target
    train_source = en_dataset[:int(len_source*0.8)]
    train_target = ja_dataset[:int(len_target*0.8)]
    val_source = en_dataset[int(len_source*0.8):int(len_source*0.9)]
    val_target = ja_dataset[int(len_target*0.8):int(len_target*0.9)]
    test_source = en_dataset[int(len_source*0.9):]
    test_target = ja_dataset[int(len_target*0.9):]
    print(f"train: {len(train_source)} lines")
    print(f"val: {len(val_source)} lines")
    print(f"test: {len(test_source)} lines")
    breakpoint()
    with open(os.path.join(OUTPUT_DIR, "train.jsonl"), "w") as f:
        for en_text,ja_text in zip(train_source,train_target):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")
    with open(os.path.join(OUTPUT_DIR, "val.jsonl"), "w") as f:
        for en_text,ja_text in zip(val_source,val_target):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")
    with open(os.path.join(OUTPUT_DIR, "test.jsonl"), "w") as f:
        for en_text,ja_text in zip(test_source,test_target):
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