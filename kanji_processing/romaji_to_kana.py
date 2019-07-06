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

	'n': '',
}

# for regex matching, ideally we want syllables
# basic combos like 'ra', 'mi', etc, with one kana
# then things like 'oo', 'ryu', etc.
# edge cases like 'n', etc.

sample_text = ['kawabata', 'teika', 'reiken', 'ryuuzi', 'zyooo', 'eikan', 'soozi']

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

		decomposition = decomposition + second_division

	print("\n\ttotal decomposition: %s\n"%decomposition)

