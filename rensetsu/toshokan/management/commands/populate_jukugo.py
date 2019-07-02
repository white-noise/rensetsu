from django.core.management.base import BaseCommand
from toshokan.models import Kanji, KanjiCompound
from django.utils import timezone

import json
import datetime

class Command(BaseCommand):
	args = ""
	help = "A script to populate joyo kanji containing jukugo from a json file."

	def _populate(self):

		# deletes previous library entries in the table, if uncommented
		# Kanji.objects.all().delete()

		# use path as according to manage.py
		json_data = open("toshokan/static/toshokan/json/complete_jukugo.json").read()
		json_obj  = json.loads(json_data)

		print("populating...")
		print("")

		count = 0
		invalid_count = 0
		problem_kanji = set()

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

		    # one of the problems is like \u6eba\u00a0
		    # which is the kanji we want followed by a non-breaking space
			
			jukugo         = list(elem["jukugo"])
			frequency      = elem["frequency"]
			pronunciation  = elem["pronunciation"]
			meaning        = elem["meaning"]
			kanji          = elem["kanji"]
			kanji_id       = elem["kanji_id"]

			kanji_list = list(Kanji.objects.filter(character=kanji))

			if len(kanji_list) == 0:
				print("%s contains the non-joyo kanji: %s"%(str(jukugo), kanji))
				invalid_count = invalid_count + 1
				problem_kanji.add(kanji)
			else:
				count = count + 1
				# print("%s contains %s"%(str(jukugo), str(kanji_list)))

			# check that jukugo hasn't been created before
			# check, for each kanji in jukugo, whether it is a db kanji
			# if yes then add the object with the through-model indicating position
			# if no then, for now, we disallow jukugo entirely (could have concurrent dictionary)
			# reading in romanji for now, but it probably can be parsed

		print("populated %d good jukugo and %d bad"%(count, invalid_count))
		print(list(problem_kanji))

	def handle(self, *args, **options):
	 	self._populate()