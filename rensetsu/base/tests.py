from django.test import TestCase

from .models import *
from toshokan.models import *

class UserProfileTestCase(TestCase):
	""" tests if user profile created on save of user object """
	def setUp(self):
		self.test_user = User.objects.create(
			username='zmr', 
			password='password', 
			email='text@website.com',
			first_name='Zane',
			last_name='Rossi')

		self.test_kanji = Kanji.objects.create(
			character='楽',
			alt_characters='',
			radical='',
			strokes=13,
			grade='1',
			meaning='happy',
			reading_jpn='らく',
			reading_eng='raku',
			)

	def test_post_save_user_profile_created(self):
		post_save_user = UserProfile.objects.filter(user__id=self.test_user.id).first()
		self.assertNotEqual(post_save_user, None)

	def test_post_save_user_profile_not_created(self):
		post_save_user = UserProfile.objects.filter(user__id=-1).first()
		self.assertEqual(post_save_user, None)

	def test_interesting_kanji_added(self):
		post_save_user = UserProfile.objects.filter(user__id=self.test_user.id).first()
		post_save_user.interesting_kanji.add(self.test_kanji)

		interesting_kanji = post_save_user.interesting_kanji.filter(id=self.test_kanji.id).first()

		self.assertEqual(self.test_kanji, interesting_kanji)
		
