# add TER, length, and BLEU scores to results file
# added_metrics.txt is the total results file
# added_generated_predictions.txt has four lines per prediction: the score, the source, the reference, and the prediction

# TERがpython3.11で動かないので、3.9(conda env: lyric_ja2)で実行している

import os
import pyter
import sacrebleu
import evaluate
import json
import spacy

cache_dir="/raid/ieda/dataset_cache"

# specify dataset/file files
DATASET_TYPE = "val" # "val" or "test"
MODEL_DIR = "mt5_bt_pre_finetuned"
CHECKPOINT=253380
SYLLABLE_TYPE = "target" # "target" or "source

OUTPUT_DIR = "/raid/ieda/examples_result/" + MODEL_DIR + "/result-" + str(CHECKPOINT)
DATASET_FILE = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/{}.jsonl".format(DATASET_TYPE)
CONSTRAINT_PATH = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/constraints/{}_len.{}".format(DATASET_TYPE, SYLLABLE_TYPE)

def main():
    print("DATASET_FILE:", DATASET_FILE)
    # read val/test dataset
    with open(DATASET_FILE, "r") as f:
        jsonl_data = [json.loads(line) for line in f.readlines()]
    source_texts = [data['translation']['en'] for data in jsonl_data] # en
    reference_texts = [data['translation']['ja'] for data in jsonl_data] # ja
    print("reference_texts:", reference_texts[0:3])

    # read model output file
    with open(os.path.join(OUTPUT_DIR, "generated_predictions.txt"), "r") as f:
        output_text = [line.strip() for line in f.readlines()]
    print("output_text:", output_text[0:3])

    result_scores = compute_scores(reference_texts, output_text, CONSTRAINT_PATH)
    generate_result_comparison_file(source_texts, output_text, reference_texts, result_scores)

def compute_scores(reference_texts, output_texts, constraint_path):
    """
    Compute metrics values for output text (given reference text).
    Reference text is optional.
    """
    output_lns = output_texts
    reference_lns = reference_texts
    if os.path.exists(constraint_path):
        constraint_lns = [x.rstrip() for x in open(constraint_path).readlines()]
        # constraint_stress_lns = [x.rstrip() for x in open(args.constraint_path.replace('.target', '_boundary.target')).readlines()]
    else:
        print('Constraint path not exist: {}'.format(constraint_path))
        constraint_lns = None
    if constraint_lns != None:
        assert len(output_lns) == len(reference_lns) == len(constraint_lns)

    # Compute scores
    scores: dict = calculate_sacrebleu(output_lns, reference_lns)

    # Read constraint target
    tgt_lens = [int(i) for i in constraint_lns]

    # Compute format accuracy
    print("start count_syllable_sentence_batch")
    out_lens = SyllableCounterJA.count_syllable_sentence_batch(output_lns)
    print("end count_syllable_sentence_batch")
    print("out_lens:", out_lens[0:3])

    len_acc, len_diff = calculate_acc(out=out_lens, tgt=tgt_lens)
    breakpoint()
    # 音韻数の正解率
    scores['length_accuracy {}'.format(SYLLABLE_TYPE)] = len_acc
    # 音韻数の平均誤差
    scores['length_difference {}'.format(SYLLABLE_TYPE)] = len_diff
    

    # Compute Translate Edit Rate (TER)
    ters = [pyter.ter(out, ref) for out, ref in zip(output_lns, reference_lns)]
    ter = sum(ters) / len(ters)
    scores['TER'] = ter

    # Save result
    with open(os.path.join(OUTPUT_DIR, "{}_metrics.txt".format(SYLLABLE_TYPE)), 'w', encoding='utf8') as f:
        f.write(json.dumps(scores, indent=4, ensure_ascii=False))

    # Metric for result comparison file
    bleus = calculate_sentence_bleu(output_lns, reference_lns)  # Sentence-level BLEU
    scores = {'bleu': ['{:.4f}'.format(i) for i in bleus]}
    ch_count = ['{} / {}'.format(i, j) for i, j in zip(out_lens, tgt_lens)]
    scores['len'] = ch_count

    return scores

def generate_result_comparison_file(srcs, outputs, refs, scores):
    '''
    Generate a result comparison file to compare the generation result with ground truth.
    scores is a dict that looks like:
        scores = {
            bleu: [bleu of all sentences],
            ter: [ter of all sentences],
        }
    '''

    # Construct file content
    ret = '----------------------------------------\n'
    ret += '{}\n'.format(SYLLABLE_TYPE)
    ret += '----------------------------------------\n'
    for i in range(len(outputs)):
        ret += 'Sentence {}'.format(i + 1)
        for k in scores:
            ret += ' | {}: {}'.format(k, scores[k][i])
        ret += '\n'
        src_s = srcs[i]
        ref_s = refs[i]
        out_s = outputs[i]
        ret += 'src: {}\n' \
               'ref: {}\n' \
               'out: {}\n' \
               '----------------------------------------\n'.format(src_s, ref_s, out_s)

    with open(os.path.join(OUTPUT_DIR, "{}_generated_predictions.txt".format(SYLLABLE_TYPE)), 'w') as f:
        f.write(ret)


def calculate_sacrebleu(out, ref, ja_tokenize=True):
    ref = [[i] for i in ref]
    metric = evaluate.load("sacrebleu",cache_dir=cache_dir)
    if ja_tokenize == True:
        result = metric.compute(predictions=out, references=ref, tokenize='ja-mecab')
    else:
        result = metric.compute(predictions=out, references=ref)
    ret = {'bleu': round(result['score'], 4)}
    return ret

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

def calculate_sentence_bleu(out, ref):
    out = [[i] for i in out]
    ref = [[[i]] for i in ref]
    ret = []
    metric = evaluate.load("sacrebleu",cache_dir=cache_dir)
    for i in range(len(out)):
        t = metric.compute(predictions=out[i], references=ref[i], tokenize='ja-mecab', use_effective_order=True)
        ret.append(t['score'])
    return ret


def calculate_acc(out, tgt):
    '''
    Calculate the ratio of same elements / average of difference in lengths
    '''
    assert len(out) == len(tgt)
    cnt_same = 0
    cnt_diff = 0
    for i in range(len(out)):
        if out[i] == tgt[i]:
            cnt_same += 1
        else:
            cnt_diff += abs(out[i] - tgt[i])
    return cnt_same / len(out), cnt_diff / len(out)

if __name__ == "__main__":
    main()