from django.core.management.base import BaseCommand
from toshokan.models import Kanji, KanjiCompound, KanjiCompoundElement
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

		    # the troubling 2010 revision kanji: ['叱', '剥', '頬', '填']
		    # 53f1 versus 20bdf
		    # 5265 versus 525d
		    # 9830 versus 982c
		    # 586b versus 5861
			
			jukugo_raw     = elem["jukugo"]
			jukugo         = list(elem["jukugo"])
			frequency      = int(elem["frequency"])
			pronunciation  = elem["pronunciation"]
			meaning        = elem["meaning"]
			kanji          = elem["kanji"]
			kanji_id       = elem["kanji_id"]

			len_jukugo = len(jukugo)
			valid_jukugo = False
			
			if len_jukugo != 2:
				continue
			else:
				valid_jukugo = True
				for elem in jukugo:
					if Kanji.objects.filter(character=elem).exists():
						continue
					else:
						valid_jukugo = False
						break

			if valid_jukugo:
				if KanjiCompound.objects.filter(characters=jukugo_raw).exists():
					continue
				else:

					kanji_compound = KanjiCompound(characters=jukugo_raw,
						meaning=meaning,
						reading_eng=pronunciation,
						frequency=frequency)
					kanji_compound.save()

					print("populated jukugo: %s"%(jukugo_raw))

					for index in range(len_jukugo):
						position = index
						component = jukugo[index]

						jukugo_element = KanjiCompoundElement(kanji_compound=kanji_compound,
							kanji=Kanji.objects.filter(character=component)[0:1].get(),
							position=position)
						jukugo_element.save()

					count = count + 1


			# check that jukugo hasn't been created before
			# check, for each kanji in jukugo, whether it is a db kanji
			# if yes then add the object with the through-model indicating position
			# if no then, for now, we disallow jukugo entirely (could have concurrent dictionary)
			# reading in romanji for now, but it probably can be parsed

		print("populated %d good jukugo"%(count))

	def handle(self, *args, **options):
	 	self._populate()