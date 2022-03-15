import model_manager
import sys, json

"""
pasting this into the terminal somehow fixes the 'libcusolver.so.11' error.
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64/
"""

try_use_device = 'cpu'
if len(sys.argv) > 1:
    if sys.argv[1] == 'gpu':
        try_use_device = 'gpu'
    elif sys.argv[1] == 'pull':
        model_manager.retrieve_new_model()

model_manager.tf_init(try_use_device)
print(f"""
    ######################################
    ## Tensorflow is utilizing the {try_use_device}! ##
    ######################################
""")

print('Making prediction.')
arr = [27,-247,-71,302,169,-115,-40,-111,-49,287,-393,-329,-32,-149,-27,-375,558,131,0,-309,-28,-551,-491,179,-73,-324,-30,636,133,74,-64,-321,-169,10,-147,-101,10,-184,-159,243,-176,536,-50,-334,-103,-428,-165,-151,-36,-176,-54,159,-880,-469,-49,-126,-36,-391,-62,-5]

prediction = model_manager.predict_from_array(arr)

response_json = {
            'class1': json.dumps(prediction[0, 0].item()),
            'class2': json.dumps(prediction[0, 1].item())
            }
print('Prediction class(1):', response_json)