import csv
import re
import json
import romaji_to_kana

with open('kana_jukugo.json', "w") as write_file:
    with open('raw_jukugo.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        bad_count  = 0
        json_data  = []

        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:                
                # id,"Comp. Word",Frequency,"Grammatical Feature",Pronunciation,"English Translation",Position,Kanji,KanjiID

                romaji_jukugo = row[4]
                bad_jukugo_flag = False
                if (',' in romaji_jukugo) or (romaji_jukugo == 'ERROR'):
                    # right now only 'simote, heta', and "ERROR" appears
                    # print(jukugo_data[i]['pronunciation'])
                    print(f'Bad jukugo: {romaji_jukugo} at line {line_count}')
                    bad_jukugo_flag = True
                    bad_count += 1
                else:
                    jukugo_transliteration = romaji_to_kana.romaji_to_kana(romaji_jukugo)
                    bad_jukugo_flag = False

                if not bad_jukugo_flag:

                    new_row = {
                        "id" : row[0],
                        "jukugo" : row[1],
                        "frequency" : row[2],
                        "grammar" : row[3],
                        "pronunciation" : jukugo_transliteration,
                        "meaning" : row[5],
                        "position" : row[6],
                        "kanji" : row[7],
                        "kanji_id" : row[8],
                    }

                    json_data.append(new_row)

                line_count += 1


        json.dump(json_data, write_file, indent=4)
        
        print(f'Processed {line_count} good lines and {bad_count} bad lines.')

