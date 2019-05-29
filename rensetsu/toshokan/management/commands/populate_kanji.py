from django.core.management.base import BaseCommand
from toshokan.models import Kanji
from django.utils import timezone

import json
import datetime

class Command(BaseCommand):
	args = ""
	help = "A script to populate the joyo kanji from a json file."

	def _populate(self):

		# deletes previous library entries in the table, if uncommented
		# Kanji.objects.all().delete()

		# use path as according to manage.py
		json_data = open("toshokan/static/toshokan/json/kanji.json").read()
		json_obj  = json.loads(json_data)

		print("populating...")
		print("")

		# provisional value parse
		for elem in json_obj:
			
			character      = elem["current"]
			alt_characters = elem["old"]
			radical        = elem["radical"]
			strokes        = int(elem["strokes"])
			grade          = elem["grade"]
			meaning        = elem["meaning"]
			reading_jpn    = ",".join(((elem["reading"])["jpn"]))
			reading_eng    = ",".join(((elem["reading"])["eng"]))

			# create kanji object and save to database
			kanji = Kanji(character=character,alt_characters=alt_characters,
				radical=radical,strokes=strokes,grade=grade,meaning=meaning,
				reading_jpn=reading_jpn,reading_eng=reading_eng)

			kanji.save()

			print(character)
			print("")

		print("populated " + str(len(json_obj)))

	def handle(self, *args, **options):
		self._populate()