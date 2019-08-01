## rensetsu 連接 (a kanji collection app)

### objective of app
- language as collection
- navigability within referential net
- non competitive, reminder/review based study. some metric of progress
- question: how can this app gain a sense of what you know and do not know over time? have you come back. may be easier given discrete kanji set

### immediate to do
- settings page, and some attribute model belonging to each profile: light/dark mode, whether to include romanizations, review format
- when a question is answered, highlight also the correct answer
- keep ajax class changes consistent with look and custom padding
- make bottom navbar into a block element in the base template? not always used though
- some sort of simple display carousel for review questions (one at a time, but all in CSS). we can also include a 'current question' field in the model, which is saved after each submission, through this requires careful ordering of the questions.
- ajax library page indicating successful group addition, as well as filters to determine where kanji is already present
- still big issue of access through url searching to other people's personal objects
- post-saves should be handled outside of the model file
- scrub and format meaning and readings with short and verbose versions (store them in model itself)
- email verification and sign-up page for users (see the simple is better than complex page on the subject)
- history for easy back-paging (a la midori), recently searched, recently added
- svg kanji shape database incorporation (long term)
- indicate when group updates, when review is incomplete, etc
- ajax everything relating to adding and deleting objects, posting comments, etc, so that no need to move away from (1) kanji individual page, (2) kanji inline object, (3) profile: redundancy
- randomization for review answers should be handled by seed generation based on, say, the time of creation for the review, so that answers do not keep shuffling on refresh (not bad behavior, just a little strange). that, or change the random filter to be deterministic based on review identity. Or this can just be handled with some explicit calls during review creation that's passed into the model itself.
- iron out some ambiguous and probably superfluous POSTS
- null on- and kun-yomi should be handled: new field for 'pretty' data (with division between short and verbose versions)
- initialization and loose tracking of kanji recognition metric
- method for choosing key value pairs for review: pronounciation, meaning
- metric for how many times a kanji has been identified correctly, kept track of on a user by user basis
- final styling, choose consistent spacing, and cutting extraneous pages

### jukugo roma-kana processing
- organize into a series of passes, non-nested, handled by functions with names
- (1) initial generous syllable break, (2) obvious dipthong break, (3) small character break, (4) retroactive insertion of long vowels with option for user correction, (5) non-standard characters and invalid romanizations
- the reverse of this is slightly easier, with recognition of small characters and scrubbing for various non-visibles

### what is displayed on a profile
- standard user data: name, username
- quick user metrics, percentage of mastery for kanji set
- custom groups (able to reorder, change names, change content; eventually taken to search page where one can load up kanji to add in one session?)
- link to pre-made quizzes of these groups, plus other mixing quizzes of a couple varying styles
- some sort of discovery mode
- something to identify a user (minimal, like a glyph, or color, or something)

### what is displayed on the landing page
- the name of the app
- choice to go to profile
- kanji of the day sort of thing

### what is displayed on a kanji's individual page
- glyph, verbose meaning, pronunciations
- alternate forms, a few jukugo
- a couple of example sentences
- profile-specific comments (stacked below)

### what should be displayed in an inline kanji window
- non-verbose data
- inline toggle (+) to add to group, and (!) to mark as interesting or difficult

### any additional apps?
- hiragana and katakana visualization as a fun sub-project for javascript lovers