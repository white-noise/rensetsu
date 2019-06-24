## rensetsu 連接 (a kanji collection app)

### objective of this app
- language as collection
- focus on hyperlink, navigability within referential net
- reminded of what you don't know, reminded of you what you do know, with simple views

### immediate to do
- scrubbing kanji json
- AJAX for comments, kanji group toggling (note that AJAX and CSRF tokens don't mix, requiring a hack)
- css framework
- generic groups
- post-saves should be handled outside of the model file

### long term implementation
- simple themes, almost entirely text based. lightweight. light and dark mode.
- custom groups beyond the three provided
- groups can be used to quiz, results of quiz shown after, permiting reshuffling of groups
- accounts communicate via friendships, sharing of comments and groups?

### points of caution
- redirects from long lists, pagination
- make sure various textfields don't have null=True (redundant, see docs)
- groups are many to many, but should be kept private to a user
- always keep kanji in common, but do so helpfully

### what is displayed on a profile
- standard user data: name, username
- kanji found interesting (either memorable, strange, useful)
- kanji found particularly difficult and particularly easy
- custom groups (with ability to override the groups shown on one's home page)
- link to pre-made quizzes based around these groups
- link to discovery modes, which troll though example sentences
- something to identify a user (minimal, like an emoji, or glyph, or color, or something)

### what is displayed on the landing page
- the name of the app
- choice to go to profile
- chance to float through kanji

### what is displayed on a kanji's individual page
- glyph, short-form meaning, pronounciations
- alternate forms, kanji compounds
- a couple decent example sentences
- profile-specific notes and comments (dynamic, stacked below)

### what should be displayed in an inline kanji window
- both glyph and reading, meaning hidden based on settings
- some toggle buttons to select as interesting, difficult, known, or dropdown for custom groups

### any additional pages
- hiragana and katakana chart, static, with reference to reading. a fun project for javascript fanatics to make this look nice on any screen (grouped by consonant)
- kanji compounds will have to exist somewhere, probably for a given kanji in a many-to-many relationship (paging through this might be tough).