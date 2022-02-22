import sys, json
import numpy as np
import keras

MODEL_PATH = './best_model.hdf5'
TARGET_LENGTH = 6

model = keras.models.load_model(MODEL_PATH)
print('model loaded')
    

class NoArgumentException(Exception):
    def __init__(self, m='When using a CLI processing tool it is often a good idea to actually give it something to process.\nFormat: [int, int, int, ...]'):
        self.m = m
        super().__init__(self.m)

def arg_str_to_int_list(arg_str):
    astr = arg_str.split(',')
    num_arr = []

    # CLI validation
    assert type(astr) == type(list())
    for num in astr:
        num_arr.append(float(num))

    assert len(num_arr) == TARGET_LENGTH
    return num_arr

def get_input():
    args = sys.argv
    enter_while = False
    input_arr = None
    if not len(args) >= 2:
        raise(NoArgumentException)
    if args[1] == '-cli':
        enter_while = True
    else:
        input_arr = arg_str_to_int_list(args[1])

    return enter_while, input_arr


def array_to_prediction_obj(num_arr):
    npaar = np.array([num_arr])
    if len(npaar.shape) == 2:  # if univariate
        # add a dimension to make it multivariate with one dimension
        npaar = npaar.reshape((npaar.shape[0], npaar.shape[1], 1))
    #print(npaar[:, 0].shape)
    return npaar# [:, 0]


def single_predict(cli_input):
    predictable_arr = array_to_prediction_obj(cli_input)

    print('arr transformed', predictable_arr)

    prediction = model.predict(predictable_arr)

    
    response_dict = {
            'class1': json.dumps(prediction[0, 1].item()),
            'class2': json.dumps(prediction[0, 0].item())
            }
    print(json.dumps(response_dict))
    return json.dumps(response_dict)


def predict_cli():
    while True:
        try:
            cli_str = input('Type an array to input, the format is float,float,float...\n')
            cli_str = arg_str_to_int_list(cli_str)
            predictable_arr = array_to_prediction_obj(cli_str)
            prediction = model.predict(predictable_arr)
            response_dict = {
                    'class1': json.dumps(prediction[0, 1].item()),
                    'class2': json.dumps(prediction[0, 0].item())
                    }
            print(json.dumps(response_dict))
        except Exception as e:
            print(e)


def main():
    enter_cli, cli_input = get_input()
    if enter_cli:
        predict_cli()
    else:
        single_predict(cli_input)

    return 0
    

if __name__ == "__main__":
    try:
        main()
    #except 
    except Exception as e:
        print(e)

