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
		json_data = open("toshokan/static/toshokan/json/complete_kanji.json").read()
		json_obj  = json.loads(json_data)

		print("populating...")
		print("")

		"""
		"id": "5",
        "kanji": "\u66d6",
        "strokes": "17",
        "grade": "7",
        "classification": "\u5f62\u58f0 Phonetic",
        "jlpt": "-",
        "radical_name": "Nichi, Nichihen",
        "joyo_reading": "\u30a2\u30a4",
        "number_on": "1",
        "on_in_joyo": "ai",
        "number_on_meaning": "2",
        "on_meaning": "dark; not clear",
        "kun_in_joyo": "-",
        "number_kun_meaning": "0",
        "kun_meaning": "-",
        "year_inclusion": "2010"
		"""

		# provisional value parse
		for elem in json_obj:
			id_num = elem["id"]
			kanji = elem["kanji"]
			strokes = elem["strokes"]
			grade = int(elem["grade"])
			classification = elem["classification"]
			jlpt = elem["jlpt"]
			radical_name = elem["radical_name"]
			reading = elem["joyo_reading"]
			number_on = elem["number_on"]
			on_in_joyo = elem["on_in_joyo"]
			number_on_meaning = elem["number_on_meaning"]
			on_meaning = elem["on_meaning"]
			kun_in_joyo = elem["kun_in_joyo"]
			number_kun_meaning = elem["number_kun_meaning"]
			kun_meaning = elem["kun_meaning"]
			year_inclusion = elem["year_inclusion"]

			# create kanji object and save to database
			kanji = Kanji(
				character=kanji, 
				strokes=strokes,
				grade=grade,
				jlpt=jlpt,
				on_meaning=on_meaning,
				kun_meaning=kun_meaning,
				reading=reading,
				)

			kanji.save()

			print(kanji)
			print("")

		print("populated " + str(len(json_obj)))

	def handle(self, *args, **options):
		self._populate()