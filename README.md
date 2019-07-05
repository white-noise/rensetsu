## rensetsu 連接 (a kanji collection app)

### objective of app
- language as collection
- focus on hyperlink, navigability within referential net
- reminded of what you don't know, reminded of you what you do know, with simple views
- non competitive, but reminder/review based study. not quizzes but assessments with some edge of adaptability and some metric of progress
- question: how can this app gain a sense of what you know and do not know over time? duolingo, e.g., does not always address this well (with apparent over-repetition). this case may be easier given discrete kanji/jukugo set.

### immediate to do
- form validation (e.g., exceeded character length)
- AJAX for comments, kanji group toggling (note that AJAX and CSRF tokens don't mix, requiring a hack)
- post-saves should be handled outside of the model file
- simple user interaction (friends, short messages, sharing groups?)
- add frequency, separate readings, and additional parameters to kanji and jukugo
- create model for a kanji quiz based on a group, and method for displaying quiz results
- enable email verification and sign-up for user accounts (latter before former)
- rank jukugo based on frequency and list the most frequent with options for seeing all
- basic search for kanji (using either hashtag system, kanji only, with related jukugo)
- figure out basic parsing of the stroke order database with pleasant small style (png gif?)
- start keeping track of file sizes
- for the love of god write unit tests before adding any more views or bootstrap

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

### things to do with kanji database
- provide japanese reading for jukugo
- create reasonable database structure for jukugo objects
- determine if jukugo contain only joyo kanji
- supplement definitions, and separate on- and kun-yomi

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
