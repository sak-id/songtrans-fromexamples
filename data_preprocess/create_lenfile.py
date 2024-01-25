# create len file acording to src and tgt file (val/test datasets)
# for calculate length accuracy in add_metrics_to_results.py
# conda activate lyric_ja2 (python3.9)

# English Syllable Counter is from Singable-Translation

import os
import json
import spacy
import nltk
import cmudict

DATASET_TYPE = "test" # "val" or "test"

DATASET_FILE = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/{}.jsonl".format(DATASET_TYPE)
OUTPUT_FILE = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/constraints/"

def main():
    print("DATASET_FILE:", DATASET_FILE)
    # read val/test dataset
    with open(DATASET_FILE, "r") as f:
        jsonl_data = [json.loads(line) for line in f.readlines()]
    source_texts = [data['translation']['en'] for data in jsonl_data] # en
    reference_texts = [data['translation']['ja'] for data in jsonl_data] # ja
    print("reference_texts:", reference_texts[0:3])

    # count syllables in english:
    en_lens = SyllableCounter.count_syllable_sentence_batch(source_texts)
    print("en_lens:", en_lens[0:3])
    print("len(en_lens):", len(en_lens))

    # count syllables in japanese:
    ja_lens = SyllableCounterJA.count_syllable_sentence_batch(reference_texts)
    print("ja_lens:", ja_lens[0:3])
    print("len(ja_lens):", len(ja_lens))

    breakpoint()
    if not os.path.exists(OUTPUT_FILE):
        os.makedirs(OUTPUT_FILE)
    # write to file
    with open(os.path.join(OUTPUT_FILE, DATASET_TYPE + "_len.source"), "w") as f:
        for i in en_lens:
            f.write(str(i) + "\n")
    with open(os.path.join(OUTPUT_FILE, DATASET_TYPE + "_len.target"), "w") as f:
        for i in ja_lens:
            f.write(str(i) + "\n")
    pass

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