from datetime import datetime
import re


def get_value_of_arg(text: str, start: int):
    ind = 0
    for i in range(start + 1, len(text)):
        if text[i] == " " or text[i] == "\n":
            return text[start: ind]


def parse_file(path_to_file):
    with open(path_to_file, "r") as log:
        for line in log:
            timestamp = ""
            params = {}
            tmp_line = line

            timestamp_match = re.match(timestamp_reg, line)
            if timestamp_match:
                tmp_line = tmp_line[timestamp_match.end():]
                print(timestamp_match.string[timestamp_match.start(): timestamp_match.end()])

            words = tmp_line.split(" ")
            word_ind = 0

            while word_ind < len(words):
                arg_match = re.fullmatch(argument_reg, words[word_ind])
                if arg_match:
                    params[arg_match.string] = words[word_ind + 1]
                    word_ind += 1
                else:
                    word_ind += 1

            for i in params.keys():
                print(f"{i}={params[i]}")
            # print(line[arg_match.start(), arg_match.end()])


timestamp_reg = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}'
argument_reg = '\D+:'

path_to_file = "/Users/andrejtarasov/Desktop/cinimex/BankruptLoadingModule_27/EFRSBGetList_INFO_TraceHTTPSuccAuth.log"



