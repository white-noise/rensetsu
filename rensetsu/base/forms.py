from django.forms import ModelForm
from .models import KanjiComment

class KanjiCommentForm(ModelForm):

	class Meta:
		model = KanjiComment
		fields = ('comment',)
