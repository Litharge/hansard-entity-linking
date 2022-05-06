import pickle

mp_list = pickle.load(open("2021-12-01.p", "rb"))

for item in mp_list.mp_list:
    print(item)

