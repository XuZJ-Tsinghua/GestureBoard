word_dict = dict()


def is_legal(word):
    for letter in word:
        if not ('a' <= letter <= 'z'):
            return False
    return True


def read_write(file1, file2):
    global word_dict
    with open(file1, "r", encoding='UTF-8') as f:
        lines = f.read().split("\n")[: -1]
    i = 0
    for line in lines:
        arr = line.split("	")
        word = arr[0]
        if not is_legal(word):
            continue
        if word in word_dict:
            continue
        freq = arr[3]
        word_dict[word] = freq
        i += 1
        if i >= 10000:
            break
    with open(file2, "w") as f:
        for word in word_dict:
            f.write(word + " " + word_dict[word] + "\n")


def main(file1, file2):
    read_write(file1, file2)


if __name__ == "__main__":
    main("ANC.txt", "Lexicon.txt")
