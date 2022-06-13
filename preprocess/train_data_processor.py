import random

punc_list = ['，','。',',','.','!','?',':',';','、','！']

punc_dict = {
    "，":"COMMA",
    "。":"PERIOD",
    ",":"COMMA",
    ".":"PERIOD",
    "!":"PERIOD",
    "?":"QUESTION",
    ":":"COMMA",
    ";":"PERIOD",
    "、":"COMMA",
    "！":"PERIOD",
}

def get_label_data(line):
    label_list = []
    for char in line:
        if char not in punc_list:
            label_list.append(char+"	O\n")
        else:
            if len(label_list)==0:
                print("invalid sentence!!!!!!")
                return []
            label_list[-1] = last_char+"	"+punc_dict[char]+"\n"
        last_char = char
    return label_list

def get_label_file(file_name,lines):
    with open(file_name,'w') as w:
        for line in lines:
            label_data = get_label_data(line.strip())
            w.writelines(label_data)
            if len(label_data)!=0:
                w.write("\n")
    


with open("./trans.txt", "r") as r, open("./trans_raw.txt","w") as w:
    for line in r:
        items = line.split(" ")
        if len(items)==2:
            w.write(items[1].strip()+"\n")


with open("./trans_raw.txt", "r") as r:
    lines = r.readlines()
    random.shuffle(lines)
    all_data_lines = []
    train_lines = lines[:int(len(lines)*0.8)]
    valid_lines = lines[-int(len(lines)*0.2):-int(len(lines)*0.1)]
    test_lines = lines[-int(len(lines)*0.1):]

    get_label_file("./trans_train.txt",train_lines)
    get_label_file("./trans_dev.txt",valid_lines)
    get_label_file("./trans_test.txt",test_lines)




