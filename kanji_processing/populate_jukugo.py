# from django.core.management.base import BaseCommand
# from toshokan.models import Kanji, KanjiCompound
# from django.utils import timezone

import json
# import datetime

# class Command(BaseCommand):
# 	args = ""
# 	help = "A script to populate the joyo kanji from a json file."

# 	def _populate(self):

		# deletes previous library entries in the table, if uncommented
		# Kanji.objects.all().delete()

		# use path as according to manage.py
json_data = open("complete_jukugo.json").read()
json_obj  = json.loads(json_data)

print("populating...")
print("")

count = 0

# provisional value parse
for elem in json_obj:
	
	# sample jukugo with relevant fields
	# "id": "8278",
    # "jukugo": "\u4e9c\u925b",
    # "frequency": "364",
    # "grammar": "general noun",
    # "pronunciation": "aen",
    # "meaning": "zinc",
    # "position": "L",
    # "kanji": "\u4e9c",
    # "kanji_id": "1"
	
	jukugo         = list(elem["jukugo"])
	frequency      = elem["frequency"]
	pronunciation  = elem["pronunciation"]
	meaning        = elem["meaning"]
	kanji          = elem["kanji"]
	kanji_id       = elem["kanji_id"]

	print(jukugo)

	# check that jukugo hasn't been created before
	# check, for each kanji in jukugo, whether it is a db kanji
	# if yes then add the object with the through-model indicating position
	# if no then, for now, we disallow jukugo entirely (could have concurrent dictionary)
	# reading in romanji for now, but it probably can be parsed

	count = count + 1

print("populated %d"%(count))

	# def handle(self, *args, **options):
	# 	self._populate()