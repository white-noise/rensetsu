import csv
import re
import json

with open('kanji.json', "w") as write_file:
    with open('joyo_kanji.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        json_data  = []

        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                regex_split = re.split('(?<=[^a-z,ō\s])(?=[a-z,ō\s])', row[-1], flags=re.IGNORECASE, maxsplit=1)
                
                # need to check if this captures all whitespace
                eng_split = (regex_split[1]).split(", ")
                jpn_split = (regex_split[0]).split("、")

                # if (len(eng_split) != len(jpn_split)) or (len(eng_split) == 0):
                # print("")

                # for i in range(8):
                #     row[i] = (row[i]).replace(" ", "")
                #     print(row[i])

                # print(eng_split)
                # print(jpn_split)

                line_count += 1

                new_row = {
                    "index"   : row[0],
                    "current" : row[1],
                    "old"     : row[2],
                    "radical" : row[3],
                    "strokes" : row[4],
                    "grade"   : row[5],
                    "meaning" : row[7],
                    "reading" : 
                        {
                            'jpn' : jpn_split, 
                            'eng' : eng_split
                        },
                }

                json_data.append(new_row)

        json.dump(json_data, write_file, indent=4)
        
        print(f'Processed {line_count} lines.')

