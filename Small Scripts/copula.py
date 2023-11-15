import re
import os

folder = r'C:\Users\Example\Downloads\Eleanor2'
os.chdir(folder)

for cex in os.listdir(folder):
    cex_path = os.path.join(folder, cex)
    with open(cex_path, 'rt', encoding='utf-8') as file:
        lines = file.readlines()
        fileName = "FILE: "
        for index, line in enumerate(lines):
            if line.startswith("From file"):
                fileName += line[line.index("<"):]
                with open(cex_path, 'w', encoding='utf-8') as new_file:
                    new_file.write(fileName)

            lineNo = re.search(r'line [0-9]*\.$', line)
            if (lineNo != None):
                lineToPrint = lineNo.group().replace('.', ':')
                lineToPrint += " "
                for nextLine in lines[index + 1::]:
                    if nextLine.startswith("%mor"):
                        break
                    lineToPrint += nextLine.replace('\t', ' ')
                    with open(cex_path, 'a', encoding='utf-8') as new_file:
                            new_file.write(lineToPrint.split('')[0].strip())
                            new_file.write('\n')

with open('merged_file.txt', 'at', encoding='utf-8') as merged_file:
    for cex in os.listdir(folder):
        cex_path = os.path.join(folder, cex)
        with open(cex_path, 'rt', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                merged_file.write(line)
            merged_file.write("\n\n")
        if cex_path != os.path.join(folder, 'merged_file.txt'):
            os.remove(cex_path)
