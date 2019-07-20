## rensetsu 連接 (a kanji collection app)

### objective of app
- language as collection
- focus on navigability within referential net
- reminded of what you don't know, reminded of you what you do know, with simple views
- non competitive, but reminder/review based study. not quizzes but assessments with some edge of adaptability and some metric of progress
- question: how can this app gain a sense of what you know and do not know over time? duolingo, e.g., does not always address this well (with apparent over-repetition?). this project may be easier given discrete kanji/jukugo set.

### immediate to do
- post-saves should be handled outside of the model file
- new reading format for kanji, and kana for jukugo (needs careful scrub)
- email verification and sign-up for user accounts (latter before former)
- methods for recording progress and global searches
- figure out basic parsing of the stroke order database with pleasant small style (png, gif?)
- for the love of god write tests
- review model answers not always distinct?
- right now review model update when group updates is not reasonable (post-save hook?)
- make the format better looking and more mobile friendly
- AJAX everything relating to adding and deleting from groups, posting comments, etc
- include slugs and reverses with defaults for getting around menus and searches; see model apps for ideas on this
- iron out some ambiguous and probably superfluous POSTS

### jukugo processing to do
- organize into a series of passes, non-nested, handled by functions with names
- (1) initial generous syllable break, (2) obvious dipthong break, (3) small character break, (4) retroactive insertion of long vowels with option for user correction, (5) non-standard characters and invalid romanizations

### ideas for new review model
- associated with a given user (possible sharing later)
- time of creation
- review contains kanji-score objects
- kanji and associated level of recognition (an integer)
- when a group is created, it has to be associated with a user group, from which it will draw all of the constituent kanji and create the objects above
- when a review is happening, options to draw answers from quiz set, globally, and split between on- and kun-yomi, meaning, etc.
- kanji to reading/meaning, making sure answers are distinct?
- reading/meaning to kanji, once again making answers distinct.
- maybe someday allowing user input answers. But MC is almost as good with enough options, for this type of thing
- one session with ability to come back, updates each page, saved progress?
- when the user clicks to review a group, a new review object is created, or a previous review object is searched for (whereupon the user can begin where they left off). They're then taken to a page that always fetches this object. When the user answers a question, it is flagged as completed, and disabled. When they have answered all questions (all kanji), then the review is removed
- eventually each of these reviews will contribute to a m2m relationship between user and kanji, whereby the comprehension level of the kanji is tracked
- would be nice to eventually have a visualization of this network

### points of caution
- redirects from long lists, pagination (can be handled with slugs and GETs and default cases)
- or can quick reverse plus redirect if that fails
- format errors well and give all forms error display
- gaurantee user only sees their own content; okay to be redundant in this

### things to do with kanji database
- kana reading for jukugo
- jukugo should contain only joyo kanji (or eventually jinmeio extension)
- supplement definitions, separate on- and kun-yomi

### what is displayed on a profile
- standard user data: name, username
- custom groups (able to reorder, change names, change content; eventually taken to search page where one can load up kanji to add in one session?)
- link to pre-made quizzes of these groups, plus other mixing quizzes of a couple varying styles
- link to discovery modes, reference to example sentences
- something to identify a user (minimal, like a glyph, or color, or something)

### what is displayed on the landing page
- the name of the app
- choice to go to profile
- chance to 'float' through kanji; some pretentious javascript

### what is displayed on a kanji's individual page
- glyph, short-form meaning, pronunciations
- alternate forms, a few jukugo
- a couple of example sentences
- profile-specific comments (stacked below)
- nothing should really be collapsible

### what should be displayed in an inline kanji window
- both glyph and reading, meaning hidden based on settings? question on where settings are normally stored? cached? sent to database later?
- possible inline toggle to add to a group, or favorite, or something?
- question: should favorite and unknown markers be group specific? eh, no.
- bigger question: all of these requests seem to demand either repetitive views or AJAXy things.

### any additional apps?
- hiragana and katakana into as a fun sub-project for the javascript hankerers