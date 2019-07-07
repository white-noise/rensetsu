import re

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

# for regex matching, ideally we want syllables
# basic combos like 'ra', 'mi', etc, with one kana
# then things like 'oo', 'ryu', etc.
# edge cases like 'n', etc.

sample_text = ['kawabata', 'teikan', 'reiken', 'ryuuzi', 
				'zyoo', 'soozi', 'oote', 'tairyoo', 'tyotto']

# for replacing, e.g., 'ryo' with 'ri' 's_yo' 'o'
def small_character(syllable):

	return '%si s_%s'%(syllable.group(0)[0], syllable.group(0)[1:])

def repeat_consonant(syllable):

	return 's_tu %s'%(syllable.group(0)[1:])

for word in sample_text:
	
	# this breaks into obvious syllables
	re_pattern = '([kgmnrhbptdyszw]*[aiueo]+)'
	# leaving dipthongs and extended vowels unsplit
	syllables = list(filter(None, re.split(re_pattern, word)))

	print('%s split into %s'%(word, syllables))

	decomposition = []
	for elem in syllables:
		re_pattern = '([kgmnrhbptdyszw]*[aiueo])'
		second_division = list(filter(None, re.split(re_pattern, elem, maxsplit=1)))
		print('\t%s split into %s'%(elem, second_division))

		sub_decomposition = []
		for syllable in second_division:
			re_small_pattern = '([kgmnrhbptdyszw]y[aiueo])'
			third_division   = re.sub(re_small_pattern, small_character, syllable)
			third_division   = third_division.split(' ')
			print('\t\tthird division: %s'%third_division)

			sub_decomposition = sub_decomposition + third_division

		decomposition = decomposition + sub_decomposition

	final_decomposition = []
	for elem in decomposition:
		re_repeat_pattern = '([kgmnrhbptdyszw][kgmnrhbptdyszw][aiueo]*)'
		fourth_division = (re.sub(re_repeat_pattern, repeat_consonant, elem)).split(' ')
		final_decomposition = final_decomposition + fourth_division
		print('\t\t\tfourth division: %s'%fourth_division)


	# need to have one last pass looking for lone consonants for
	# small tu etc. words like 'zyotto'

	print("\n\ttotal decomposition: %s\n"%final_decomposition)

	translated_string = ''.join(map(lambda x: char_dict[x], final_decomposition))

	print("\n\ttranslates to: %s\n"%translated_string)

# for o versus u there should be some sort of check for a lone 'o' following
# either another 'o'-terminated block. 'u' is always 'u' but not the inverse.

# instead of recursive we can make this iterative, with different passes,
# each given their own function. that is saved for optimization
