import pickle

mp_list = pickle.load(open("verified_test_discourse_model.p", "rb"))

for item in mp_list.mp_list:
    print(item)

