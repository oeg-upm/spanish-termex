import csv
import numpy as np
import os
import time


def read_term_list_file(filepath):
    lst = []
    with open(filepath, "r", encoding='utf-8') as f:
        for line in f:
            k = line.replace("\n", '').replace("  ", " ").replace("  ", " ")
            k = k.strip()
            lst.append(k.lower())
    return lst


def f1(a, b):
    return a * b * 2 / (a + b)


def mean_f_p_r(actual, predicted, best=10, pr_plot=False):
    list_f1 = []
    list_p = []
    list_r = []
    for r in range(len(actual)):
        y_actual = actual[r]
        y_predicted = predicted[r][:best]
        y_score = 0
        for p, prediction in enumerate(y_predicted):
            if prediction in y_actual and prediction not in y_predicted[:p]:
                y_score += 1
        if not y_predicted:
            y_p = 0
            y_r = 0
        else:
            y_p = y_score / len(y_predicted)
            y_r = y_score / len(y_actual)
        if y_p != 0 and y_r != 0:
            y_f1 = 2 * (y_p * y_r / (y_p + y_r))
        else:
            y_f1 = 0
        list_f1.append(y_f1)
        list_p.append(y_p)
        list_r.append(y_r)
    if pr_plot:
        return list_f1, list_p, list_r
    else:
        return np.mean(list_f1), np.mean(list_p), np.mean(list_r)


def get_file_ids(text_path):
    # get files name
    files = os.listdir(text_path)
    for i, file in enumerate(files):
        files[i] = file[:-4]
    return files

def evaluate_results(keypath, respath ,f1_top):
    

    keys_path = keypath
    res_path = respath + 'res' + str(f1_top) + '/'
    predicted = []
    actual = []

    keyfiles = os.listdir(keys_path)
    resfiles = os.listdir(res_path)
    if len(keyfiles) != len(resfiles):
        print('FATAL ERROR')
        return

    print('Files to process:', len(keyfiles))

    for keyf in keyfiles:
        key_single = read_term_list_file(keys_path+keyf)
        key_single = list(set(key_single))
        actual.append(key_single)

        pred_single = read_term_list_file(res_path+keyf)
        pred_single = list(set(pred_single))
        predicted.append(pred_single)

    mean_f1, mean_p, mean_r = mean_f_p_r(actual, predicted, f1_top)
    straight_f1 = f1(mean_p, mean_r)
    print('Precission, recall, f1, mean_f1')
    print(mean_p, mean_r, straight_f1, mean_f1)
    print(mean_p*100, mean_r*100, straight_f1*100)
