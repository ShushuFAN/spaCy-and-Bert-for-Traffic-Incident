import pandas as pd

def all_predicate(golden_dict,predict_result):
    correct_sum, predict_sum, recall_sum = 0.0, 0.0, 0.0
    assert len(golden_dict) == len(predict_result)
    for i in range(0,len(golden_dict)):
        golden_predicates=golden_dict[i].split(" ")
        predict_predicates=predict_result[i].split(" ")
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
    assert len(golden_dict) == len(predict_result)
    for i in range(0, len(golden_dict)):
        golden_predicates = golden_dict[i].split(" ")
        predict_predicates = predict_result[i].split(" ")
        for predicate in predict_predicates:
            if predicate_name in predicate:
                predict_sum+=1
                if predicate in golden_predicates:
                    correct_sum+=1
        for predicate in golden_predicates:
            if predicate_name in predicate:
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
    golden_data = open(golden_file, "r", encoding='utf-8').readlines()
    predict_data = open(predict_file, 'r', encoding='utf-8').readlines()
    golden_dict = [line.strip() for line in golden_data]
    predict_result = [line.strip() for line in predict_data]
    print("records", len(golden_dict))
    print("records", len(predict_result))
    df = pd.DataFrame(columns=["predicate","precision", "recall","f1"])
    df=df.append(all_predicate(golden_dict,predict_result),ignore_index=True)
    predicates=["Affect","Status","Lane","Direction","Near",
            "Between","Arrangement","Location"]
    for predicate in predicates:
        df=df.append(one_predicate(golden_dict,predict_result,predicate),ignore_index=True)
    print(df)
    return df

if __name__ == '__main__':
    golden_dict = "predicate_out.txt"
    predict_result = "predicate_predict.txt"
    df=calc_pr(golden_dict, predict_result)
    df.to_csv("eva_classification.csv", header=True)