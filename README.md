## rensetsu 連接 (a kanji collection app)

### objective of this app
- making language into collection, curation, curiosity
- make use of what web-based format can provide in ease, connection
- what is important is the link, the sort, the group
- reminds you what you don't know, reminds you what you do, all with simple views, interface that eschews competition and games

### things to do
- goal is quick, easily navigable, intuitive connections. collection of information rather than a game, competition, or motivational fervor. it should remind you of what you need to learn, but beautifully, and calmly.
- individual accounts should hold reference to interesting, difficult, and mastered kanji, along with other personal data not yet determined.
- user should be able to comment for a given kanji, i.e. store plain text notes about its use, as well as example sentences, in clean, minimal boxes directly accessible with the kanji.
- simple themes, almost entirely text based. lightweight is emphasis. light and dark mode.
- on the backend, post-saves should be handled outside of the model file before deployment.

### what is displayed on a profile
- standard user data: name, username, password, email.
- kanji found intersting (either memorable, strange, useful)
- kanji found particularly difficult and particularly easy
- possible ability to create custom groups (with ability to override the above on one's home page)
- link to review, scroll through these groups
- something to identify a user (eventually people should be able to see other profiles). the goal is placid communication, not competition

### what is displayed on the landing page
- the name of the app, or a random kanji
- choice to go to profile

### what is displayed on a kanji's individual page
- glyph, short-form meaning, pronounciations
- alternate forms, kanji compounds
- can we scrape decent example sentences
- profile-specific notes and comments (dynamic, stacked below)

### what should be displayed on an inline kanji window
- possibility to display both glyph and reading, or for hidden meaning and reading
- english and japanese reading, or just japanese (a variety of toggles in a settings page)
- some buttons (disabled if not logged in) to select as interesting, difficult, known, or dropdown for custom groups.

### what if any methods can be used for review
- gentle quizes drawing from certain groups. results displayed at the end, with options to shift around group assignments.