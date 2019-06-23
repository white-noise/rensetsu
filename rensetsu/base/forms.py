from django.forms import ModelForm
from .models import KanjiComment

class KanjiCommentForm(ModelForm):

    class Meta:
        model = KanjiComment
        fields = ('comment',)

    # in general this will define the look of the form
    def __init__(self, *args, **kwargs): 
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = ''
