import pickle

mp_list = pickle.load(open("../discourse_model_data/2020-06-15.p", "rb"))

for item in mp_list.mp_list:
    print(item)
