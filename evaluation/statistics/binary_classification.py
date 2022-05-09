
def get_true_positive(ground_truth, to_check):
    true_pos = 0
    for key in to_check:
        for value in to_check[key]:
            if key in ground_truth and value in ground_truth[key]:
                true_pos += 1

    return true_pos

def get_false_negative(ground_truth, to_check):
    false_neg = 0
    for key in ground_truth:
        for value in ground_truth[key]:
            if key not in to_check or value not in to_check[key]:
                false_neg += 1

    return false_neg


def get_false_positive(ground_truth, to_check):
    false_pos = 0
    for key in to_check:
        for value in to_check[key]:
            if key not in ground_truth or value not in ground_truth[key]:
                false_pos += 1

    return false_pos