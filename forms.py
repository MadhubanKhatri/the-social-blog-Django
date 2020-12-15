from django import forms
from .models import *
from ckeditor.fields import RichTextField

class WritePostForm(forms.ModelForm):
	title = forms.CharField(label='Title',help_text='Title', widget=forms.TextInput(attrs={'placeholder': 'Title'}), required=True, max_length=100)
	content = RichTextField()
	# date = forms.DateField()

	class Meta:
		model = Post
		fields = ('title', 'content',)
    # class Meta:
    #     model = Post
    #     fields = ('',)
