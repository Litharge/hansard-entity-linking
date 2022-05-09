# todo: recall, precision, f score

from evaluation.statistics.binary_classification import get_false_negative, get_true_positive, get_false_positive

# recall = true positive / true positive + false negative
def get_recall_for_dictionary(ground_truth, to_check):
    return get_true_positive(ground_truth, to_check) \
           / (get_true_positive(ground_truth, to_check) + get_false_negative(ground_truth, to_check))

def get_precision_for_dictionary(ground_truth, to_check):
    return get_true_positive(ground_truth, to_check) \
        / (get_true_positive(ground_truth, to_check) + get_false_positive(ground_truth, to_check))

def get_f1_for_dictionary(ground_truth, to_check):
    precision = get_precision_for_dictionary(ground_truth, to_check)
    recall = get_recall_for_dictionary(ground_truth, to_check)
    return 2 * (precision * recall) / (precision + recall)