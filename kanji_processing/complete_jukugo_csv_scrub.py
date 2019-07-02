import csv
import re
import json

with open('complete_jukugo.json', "w") as write_file:
    with open('raw_jukugo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        json_data  = []

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:                
                # id,"Comp. Word",Frequency,"Grammatical Feature",Pronunciation,"English Translation",Position,Kanji,KanjiID

                new_row = {
                    "id" : row[0],
                    "jukugo" : row[1],
                    "frequency" : row[2],
                    "grammar" : row[3],
                    "pronunciation" : row[4],
                    "meaning" : row[5],
                    "position" : row[6],
                    "kanji" : row[7],
                    "kanji_id" : row[8],
                }

                json_data.append(new_row)

                line_count += 1


        json.dump(json_data, write_file, indent=4)
        
        print(f'Processed {line_count} lines.')

