import subprocess

from src.nlp_qrmine import Content
from src.nlp_qrmine import ReadData


def main():
    data = ReadData()
    interviews = data.content
    content = Content(interviews)

    words = content.common_nouns(10)
    output = []
    for word, f1 in words:
        for attribute, f2 in content.attributes(word, 3):
            for dimension, f3 in content.dimensions(attribute, 3):
                output.append((word, attribute, dimension))
                word = '...'
                attribute = '...'
    print("_________________________________________")
    print("QRMine(TM) Qualitative Research Miner. v" + get_git_revision_short_hash())
    print("\n")
    print("gtdict - Grounded Coding Dictionary\n")
    print("-----------------------------------------")
    print_table(output)
    print("-----------------------------------------")


def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print("| " + " | ".join("{:{}}".format(x, col_width[i])
                                for i, x in enumerate(line)) + " |")


def get_git_revision_hash():
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'])


def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip().decode("utf-8")
    #return subprocess.check_output(['git', 'log', '-1', '--format=%cd']).strip().decode("utf-8")[10:]


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
