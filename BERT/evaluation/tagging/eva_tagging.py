import pandas as pd
import json

def load_result(predict_filename):
    result_dict = {}
    with open(predict_filename, encoding='utf-8') as gf:
        for line in gf:
            json_info = json.loads(line)
            sent = json_info['text']
            spo_list = json_info['spo_list']
            # spo_result = []
            # for item in spo_list:
            #     o = del_bookname(item['object'].lower())
            #     s = del_bookname(item['subject'].lower())
            #     spo_result.append((s, item['predicate'], o))
            # spo_result = set(spo_result)
            result_dict[sent] = spo_list
    return result_dict


def all_predicate(golden_dict,predict_result):
    correct_sum, predict_sum, recall_sum = 0.0, 0.0, 0.0
    for sent in golden_dict:
        golden_predicates=golden_dict[sent]
        predict_predicates = predict_result.get(sent, set())
        # predict_predicates=predict_result[sent]
        recall_sum+=len(golden_predicates)
        predict_sum+=len(predict_predicates)
        TP=[predicate for predicate in predict_predicates if predicate in golden_predicates]
        correct_sum+=len(TP)
    print('correct predicate num = ', correct_sum)
    print('submitted predicate num = ', predict_sum)
    print('golden predicate num = ', recall_sum)
    precision = correct_sum / predict_sum if predict_sum > 0 else 0.0
    recall = correct_sum / recall_sum if recall_sum > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) \
        if precision + recall > 0 else 0.0
    precision = round(precision, 4)
    recall = round(recall, 4)
    f1 = round(f1, 4)
    ret_info={"predicate":"all","precision":precision,"recall":recall,"f1":f1}
    return ret_info



def one_predicate(golden_dict,predict_result,predicate_name):
    correct_sum, predict_sum, recall_sum = 0.0, 0.0, 0.0
    for sent in golden_dict:
        golden_predicates = golden_dict[sent]
        predict_predicates = predict_result.get(sent, set())
        # predict_predicates = predict_result[sent]
        for predicate in predict_predicates:
            # print(predicate)
            if predicate["predicate"]==predicate_name:
                predict_sum+=1
                if predicate in golden_predicates:
                    correct_sum+=1
        for predicate in golden_predicates:
            if predicate["predicate"] == predicate_name:
                recall_sum+=1
    print('correct label num = ', correct_sum)
    print('submitted label num = ', predict_sum)
    print('golden label num = ', recall_sum)
    precision = correct_sum / predict_sum if predict_sum > 0 else 0.0
    recall = correct_sum / recall_sum if recall_sum > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) \
        if precision + recall > 0 else 0.0
    precision = round(precision, 4)
    recall = round(recall, 4)
    f1 = round(f1, 4)
    ret_info = {"predicate": predicate_name, "precision": precision, "recall": recall, "f1": f1}
    return ret_info
def calc_pr(golden_file, predict_file):
    golden_dict= load_result(golden_file)
    predict_result = load_result(predict_file)
    assert len(golden_dict) == len(predict_result)
    # print("records", len(golden_dict))
    # print("records", len(predict_result))
    df = pd.DataFrame(columns=["predicate","precision", "recall","f1"])
    df=df.append(all_predicate(golden_dict,predict_result),ignore_index=True)
    predicates=["Affect","Status","Lane","Direction","Near",
            "Between","Arrangement","Location"]
    for predicate in predicates:
        df=df.append(one_predicate(golden_dict,predict_result,predicate),ignore_index=True)
    print(df)
    return df

if __name__ == '__main__':
    golden_file = "dev_data.json"
    predict_file = "keep_empty_spo_list_subject_predicate_object_predict_output.json"
    df=calc_pr(golden_file, predict_file)
    df.to_csv("eva_tagging.csv",header=True)