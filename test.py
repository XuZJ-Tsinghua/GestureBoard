import generateTrace


lex = []
with open("Lexicon.txt",'r') as read_file:
    lineList = read_file.readlines()
    for line in lineList:
        wd = line.split(' ')[0]
        lex.append(wd)
for wd in lex[:10]:
    generateTrace.generateTrace(wd, 0.2, 0.05, 100, True)

