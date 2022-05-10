import sys, os, csv
import argparse
import pandas as pd

def load_dataset(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf8') as f:
            data = pd.read_csv(f, sep=',', header=None)
            data = data.replace(r';', '', regex=True)
        return data
    else:
        return pd.DataFrame()

def save_tsv(obj, filepath):
    with open(filepath, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        for row in obj:
            tsv_writer.writerow(row)


def convert_dataset(data, dataset_hz, samples_every_x_second, length_in_seconds, length=15, data_class=1, from_second=0):
    sample_set = []

    take_sample_every_x_hz = samples_every_x_second * dataset_hz
    converted_dataset = []

    for num, i in enumerate(data.to_dict(orient='records')):
        if not (num % take_sample_every_x_hz) == 0:
            continue
        sample_set.extend([i[0], i[1], i[2]]) #, i[3], i[4], i[5]])
        print('current len:', len(sample_set))
        if len(sample_set) >= length:
            converted_dataset.append([data_class] + sample_set)
            print('sample set added to dataset with length;',len(sample_set), '+ class.')
            sample_set = []
    if converted_dataset:
        return converted_dataset
    return []


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

    converted_data = convert_dataset(d1, 200, 5, 100)
    converted_data.extend(convert_dataset(d2, 200, 5, 100))
    converted_data.extend(convert_dataset(d3, 200, 5, 100))
    converted_data.extend(convert_dataset(d4, 200, 5, 25))
    converted_data.extend(convert_dataset(d5, 200, 5, 25))

    converted_data.extend(convert_dataset(f1, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f2, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f3, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f4, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f5, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f6, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f7, 200, 5, 15, data_class=2, from_second=9))
    converted_data.extend(convert_dataset(f8, 200, 5, 15, data_class=2, from_second=9))

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


def sisfall_main(target_length=45, hz=200, take_sample_every_x_second=1):
    converted_data = []
    with open('sisfall_paths.txt', 'r') as fpp:
        path_list = fpp.read()
        path_list = path_list.split('\n')
    
    for path in path_list:
        subpaths = path.split('/')
        if len(subpaths) < 2:
            continue
        
        trail_tag = subpaths[4].split('_')[0]
        no_fall = trail_tag.startswith('D')
        trail_num = int(trail_tag[1] + trail_tag[2])
        
        ds_fp = load_dataset(path)
        if ds_fp.empty:
            continue
        print('NEW DATASET! no fall?:', no_fall)
        if no_fall and trail_num <= 4:
            converted_data.extend(convert_dataset(ds_fp, hz, take_sample_every_x_second, 100, target_length))
        elif no_fall:
            converted_data.extend(convert_dataset(ds_fp, hz, take_sample_every_x_second, 25, target_length))
        elif not no_fall:
            converted_data.extend(convert_dataset(ds_fp, hz, take_sample_every_x_second, 15, target_length, data_class=2))
        else:
            raise Exception('bro how the fuck')
        
        print('\nset length:',len(converted_data))
        

    for dp in converted_data:
        if len(dp) != target_length+1:
            print(len(dp), dp)
            assert len(dp) == target_length+1, 'Wrong datapoint length.'

    train_set = []
    test_set = []
    for enu, dp in enumerate(converted_data):
        if enu % 5 == 0:
            test_set.append(dp)
        else:
            train_set.append(dp)
    fname = f'sisfall_{str(1/take_sample_every_x_second)}hz'
    save_tsv(train_set, f'./{fname}_TRAIN.tsv')
    save_tsv(test_set, f'./{fname}_TEST.tsv')

    #save_tsv(converted_data, f'./{fname}.tsv')
    print('dataset saved')


if __name__ == "__main__":
    """for a,b,c in os.walk('../archives/SisFall_dataset'):
        for cc in c:
            if cc.endswith('.txt'):
                print(a + '/' + cc) 
    """
    sisfall_main()