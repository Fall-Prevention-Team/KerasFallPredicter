import sys, os
import argparse
import pandas as pd

def load_dataset(filepath):
    with open(filepath, 'r', encoding='utf8') as f:
        data = pd.read_csv(f, sep=',', header=None)
        data = data.replace(r';', '', regex=True)
    return data

def main():
    sample_rate = 100 # twice a second on a 100 second dataset
    
    data_class = 1 # 1 = no fall, 2 = fall

    dataset = load_dataset('../archives/SisFall_dataset/SA01/D01_SA01_R01.txt')
    print(dataset)
    converted_dataset = []
    datapoint = []
    for i in dataset.to_dict():
        if not (i % sample_rate) == 1:
            continue
        datapoint.append(data_class)
        datapoint.append(i[1])
    
    print(datapoint)

if __name__ == "__main__":
    main()