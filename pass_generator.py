import random
length = 8
gen_data = list('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
with open("passwords.txt", "w") as file:
    data_to_write = ''
    for i in range(67):
        passwd = ''
        random.shuffle(gen_data)
        passwd = ''.join([random.choice(gen_data) for x in range(length)])
        data_to_write = data_to_write + passwd + "\n"
    file.write(data_to_write)
