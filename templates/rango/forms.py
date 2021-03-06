from django import forms
from rango.models import Page, Category

class CategoryForm(form.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please the category name.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# An inline class to provide additional information on the form
	class Meta:
		# Provide an association between the ModelForm and a model
		model = Category

class PageForm(form.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Page

		# What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        fields = ('title', 'url', 'views')