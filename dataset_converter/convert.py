import sys, os, csv
import argparse
import pandas as pd

def load_dataset(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        data = pd.read_csv(f, sep=',', header=None)
        data = data.replace(r';', '', regex=True)
    return data


def save_tsv(obj, filepath):
    with open(filepath, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        for row in obj:
            tsv_writer.writerow(row)


def convert_dataset(data, dataset_hz, samples_every_x_second, length_in_seconds, data_class=1, from_second=0):
    
    take_sample_every_x_hz = samples_every_x_second * dataset_hz
    converted_dataset = []

    for num, i in enumerate(data.to_dict(orient='records')):
        if not (num/dataset_hz) > from_second:
            continue
        if not (num % take_sample_every_x_hz) == 1:
            continue
        converted_dataset.append([data_class, i[0], i[1], i[2], i[3], i[4], i[5]])
    
    return converted_dataset
        


def main():
    root = '../archives/SisFall_dataset/'
    d1 = load_dataset(root + 'SA01/D01_SA01_R01.txt')
    d2 = load_dataset(root + 'SA01/D02_SA01_R01.txt')
    d3 = load_dataset(root + 'SA01/D03_SA01_R01.txt')
    d4 = load_dataset(root + 'SA01/D04_SA01_R01.txt')
    d5 = load_dataset(root + 'SA01/D05_SA01_R01.txt')
    d6 = load_dataset(root + 'SA01/D06_SA01_R01.txt')


    f1 = load_dataset(root + 'SA01/F01_SA01_R01.txt')
    f2 = load_dataset(root + 'SA01/F02_SA01_R01.txt')
    f3 = load_dataset(root + 'SA01/F03_SA01_R01.txt')
    f4 = load_dataset(root + 'SA01/F04_SA01_R01.txt')
    f5 = load_dataset(root + 'SA01/F05_SA01_R01.txt')
    f6 = load_dataset(root + 'SA01/F06_SA01_R01.txt')
    f7 = load_dataset(root + 'SA01/F07_SA01_R01.txt')
    f8 = load_dataset(root + 'SA01/F08_SA01_R01.txt')

    converted_data = convert_dataset(d1, 200, 1, 100)
    converted_data.extend(convert_dataset(d2, 200, 1, 100))
    converted_data.extend(convert_dataset(d3, 200, 1, 100))
    converted_data.extend(convert_dataset(d4, 200, 1, 25))
    converted_data.extend(convert_dataset(d5, 200, 1, 25))

    converted_data.extend(convert_dataset(f1, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f2, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f3, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f4, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f5, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f6, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f7, 200, 0.5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f8, 200, 0.5, 15, data_class=2, from_second=9))

    train_set = []
    test_set = []
    for enu, dp in enumerate(converted_data):
        if enu % 5 == 0:
            test_set.append(dp)
        else:
            train_set.append(dp)
    save_tsv(train_set, './out_TRAIN.tsv')
    save_tsv(test_set, './out_TEST.tsv')

    #save_tsv(converted_data, './out.tsv')
    print('dataset saved')

if __name__ == "__main__":
    main()