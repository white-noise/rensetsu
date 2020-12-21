import re
import json

char_dict = {
	'a': 'あ',
	'i': 'い',
	'u': 'う',
	'e': 'え',
	'o': 'お',

	'ka': 'か',
	'ki': 'き',
	'ku': 'く',
	'ke': 'け',
	'ko': 'こ',
	'ga': 'が',
	'gi': 'ぎ',
	'gu': 'ぐ',
	'ge': 'げ',
	'go': 'ご',

	'sa': 'さ',
	'si': 'し',
	'su': 'す',
	'se': 'せ',
	'so': 'そ',
	'za': 'ざ',
	'zi': 'じ',
	'zu': 'ず',
	'ze': 'ぜ',
	'zo': 'ぞ',

	'ma': 'ま',
	'mi': 'み',
	'mu': 'む',
	'me': 'め',
	'mo': 'も',

	'na': 'な',
	'ni': 'に',
	'nu': 'ぬ',
	'ne': 'ね',
	'no': 'の',

	'ra': 'ら',
	'ri': 'り',
	'ru': 'る',
	're': 'れ',
	'ro': 'ろ',

	'ha': 'は',
	'hi': 'ひ',
	'hu': 'ふ',
	'he': 'へ',
	'ho': 'ほ',
	'ba': 'ば',
	'bi': 'び',
	'bu': 'ぶ',
	'be': 'べ',
	'bo': 'ぼ',
	'pa': 'ぱ',
	'pi': 'ぴ',
	'pu': 'ぷ',
	'pe': 'ぺ',
	'po': 'ぽ',

	'ta': 'た',
	'ti': 'ち',
	'tu': 'つ',
	'te': 'て',
	'to': 'と',
	'da': 'だ',
	'di': 'ぢ',
	'du': 'づ',
	'de': 'で',
	'do': 'ど',

	'ya': 'や',
	'yu': 'ゆ',
	'yo': 'よ',

	'wa': 'わ',
	'wo': 'を',

	's_ya': 'ゃ',
	's_yu': 'ゅ',
	's_yo': 'ょ',
	's_tu': 'っ',

	'n': 'ん',
}

# with open('complete_jukugo.json') as file:
#   jukugo_data = json.load(file)

# print(len(jukugo_data))

# sample_jukugo = []
# for i in range(len(jukugo_data)):
# 	pronunciation = jukugo_data[i]['pronunciation']
# 	if (',' in pronunciation) or (pronunciation == "ERROR"):
# 		# right now only 'simote, heta' appears
# 		# print(jukugo_data[i]['pronunciation'])
# 		continue
# 	else:
# 		characters = jukugo_data[i]['jukugo']
# 		sample_jukugo.append((characters, pronunciation))

# print(sample_jukugo)

# sample_text = ['kawabata', 'teikan', 'reiken', 'ryuuzi', 'zyoo', 'soozi', 'oote', 'tairyoo', 'tyotto', 'tenki', 'hiai', 'ryoonai', 'airaku', 'aityaku', 'enzen']

# for replacing, e.g., 'ryo' with 'ri' 's_yo' 'o'
def small_character(syllable):

	return '%si s_%s'%(syllable.group(0)[0], syllable.group(0)[1:])

def repeat_consonant(syllable):

	return 's_tu %s'%(syllable.group(0)[1:])
	
def romaji_to_kana(romaji_jukugo):

	pronunciation = romaji_jukugo

	# break into obvious syllables; dipthongs and vowels unsplit
	re_pattern = '([kgmnrhbptdyszw]*[aiueo]+)'
	syllables = list(filter(None, re.split(re_pattern, pronunciation)))

	# print('%s split into %s'%(pronunciation, syllables))

	decomposition = []
	for elem in syllables:
		re_pattern = '([kgmnrhbptdyszw]*[aiueo])'
		second_division = list(filter(None, re.split(re_pattern, elem, maxsplit=1)))
		# print('\t%s split into %s'%(elem, second_division))

		# split all consecutive vowels apart
		for syllable in second_division:
			vowel_pattern = '((?<=[aeiou])[aeiou])'
			# note that we do not bound how often this split can happen
			vowel_division = list(filter(None, re.split(vowel_pattern, elem)))
			# print('\t%s vowel split into %s'%(elem, vowel_division))

		sub_decomposition = []
		for syllable in vowel_division:
			re_small_pattern = '([kgmnrhbptdyszw]y[aiueo])'
			third_division   = re.sub(re_small_pattern, small_character, syllable)
			third_division   = third_division.split(' ')
			# print('\t\tthird division: %s'%third_division)

			sub_decomposition = sub_decomposition + third_division

		decomposition = decomposition + sub_decomposition

	n_decomposition = []
	for elem in decomposition:
		n_pattern = '(^n)(?=[^aeiou])'
		n_division = list(filter(None, re.split(n_pattern, elem, maxsplit=1)))
		n_decomposition = n_decomposition + n_division
		# print('\t%s n split into %s'%(elem, n_division))

	final_decomposition = []
	for elem in n_decomposition:
		re_repeat_pattern = '([kgmnrhbptdyszw][kgmnrhbptdyszw][aiueo]*)'
		fourth_division = (re.sub(re_repeat_pattern, repeat_consonant, elem)).split(' ')
		final_decomposition = final_decomposition + fourth_division
		# print('\t\t\tfourth division: %s'%fourth_division)


	# here we need another pass for 'o' specifically and determining if it should be modified to an 'u'
	# rules for this are, if last character of preceeding syllable is an o, and if not first or second character
	position = 0
	clean_decomposition = []
	for elem in final_decomposition:
		if elem == 'o':
			if (position == 0):
				clean_decomposition = clean_decomposition + [elem]
			# if first and second symbol are 'o', do nothing, else if previous syllable ends in 'o', replace
			elif (final_decomposition[position - 1][-1] == 'o') and (not (position == 1 and (final_decomposition[position - 1] == 'o'))):
				clean_decomposition = clean_decomposition + ['u']
			else:
				clean_decomposition = clean_decomposition + [elem]
			position = position + 1
		else:
			clean_decomposition = clean_decomposition + [elem]
			position = position + 1

	# print("\tdecomp: %s\n"%clean_decomposition)

	translated_string = ''.join(map(lambda x: char_dict[x], clean_decomposition))

	# print("\t%s\n"%translated_string)

	return translated_string

# for index in range(10):
	
# 	kanji_compound = sample_jukugo[index][0]
# 	pronunciation = sample_jukugo[index][1]

# 	print("\n%s: %s\n"%(str(index), kanji_compound))
# 	print("\t%s\n"%pronunciation)

# 	print(romaji_to_kana(pronunciation))
