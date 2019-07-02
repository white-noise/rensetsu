import csv
import re
import json

with open('complete_kanji.json', "w") as write_file:
    with open('raw_kanji.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        json_data  = []

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:                
                # id,Kanji,Strokes,Grade,"Kanji Classification",JLPT-test,"Name of Radical","Reading within Joyo","Reading beyond Joyo","# of On","On within Joyo","Kanji ID in Nelson","# of Meanings of On","Translation of On","# of Kun within Joyo with inflections","# of Kun within Joyo without inflections","Kun within Joyo","# of Meanings of Kun","Translation of Kun","Year of Inclusion"

                new_row = {
                    "id" : row[0],
                    "kanji" : row[1],
                    "strokes" : row[2],
                    "grade" : row[3],
                    "classification" : row[4],
                    "jlpt" : row[5],
                    # "radical_name" : row[6],
                    "joyo_reading" : row[7],
                    # "beyond_joyo_reading" : row[8],
                    "number_on" : row[9],
                    "on_in_joyo" : row[10],
                    # "nelson_id" : row[11],
                    "number_on_meaning" : row[12],
                    "on_meaning" : row[13],
                    # "number_kun_inflection" : row[14],
                    # "number_kun_no_inflection" : row[15],
                    "kun_in_joyo" : row[16], 
                    "number_kun_meaning" : row[17],
                    "kun_meaning" : row[18],
                    "year_inclusion" : row[19],
                }

                json_data.append(new_row)

                line_count += 1


        json.dump(json_data, write_file, indent=4)
        
        print(f'Processed {line_count} lines.')

