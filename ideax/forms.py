from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Idea, Criterion, Category, Dimension, Category_Dimension, Evaluation, Challenge, Use_Term, Category_Image
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget
from tinymce import TinyMCE
from martor.fields import MartorFormField
from martor.widgets import AdminMartorWidget


class IdeaForm(forms.ModelForm):
    
    oportunity = MartorFormField()
    solution = MartorFormField()
    target = MartorFormField()
    summary = MartorFormField()
    class Meta:
        model = Idea
        fields = ('title', 'summary', 'oportunity', 'solution', 'target', 'category', 'challenge' )
        labels = {'title': _('Title'), 'summary': _('Summary') , 'oportunity': _('Oportunity'), 'solution': _('Solution'), 'target': _('Target'),'category': _('Category'), 'challenge': _('Challenge')}



class IdeaFormUpdate(forms.ModelForm):

    class Meta:
        model = Idea
        fields = ('title', 'oportunity', 'solution', 'target')
        labels = {'title': _('Title'), 'oportunity': _('Oportunity'), 'solution': _('Solution'), 'target': _('Target'),  }

class CriterionForm(forms.ModelForm):

    class Meta:
        model = Criterion
        fields = ('description','peso')
        labels = {'peso': _('Weight'), 'description': _('Description'), }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ('title', 'description', )
        labels = {'title':_('Title'), 'description': _('Description') }
class CategoryImageForm(forms.ModelForm):

    class Meta:
        model = Category_Image
        fields = ('description', 'image', 'category')
        labels = {'description':_('Description'),'image':_('Image'),'category':_('Category')}

class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = ('title', 'image', 'summary', 'requester', 'description', 'active' , 'limit_date', 'featured', 'category',)
        labels = {'title':_('Title'),'image':_('Image'),'summary':_('Summary'),
                  'requester':_('Requester'),'description':_('Description'),'active':_('Active'),'limit_date':_('Limit Date'),'featured':_('Featured'),'category':_('Category')}
        widgets = {
            'limit_date' : forms.DateInput(attrs={'placeholder' : 'dd/mm/aaaa'}),
        }
class UseTermForm(forms.ModelForm):
    
    class Meta:
        model = Use_Term
        fields = ('creator', 'term', 'init_date', 'final_date')
        labels = {'creator':_('Creator'), 'term':_('Term'), 'init_date':_('Initial Date'), 'final_date':_('Final Date')}
        widgets = {
            'term' : TinyMCE(),
        }

class EvaluationForm(forms.Form):
    FORMAT_ID = 'category_dimension_%s'
    FORMAT_ID_NOTE = 'note_dimension_%s'

    def __init__(self, *args, **kwargs):
        dimensions = kwargs.pop('extra', None)
        initial_arguments = kwargs.pop('initial', None)
        super(EvaluationForm, self).__init__(*args, **kwargs)

        if initial_arguments:
            for i in initial_arguments:
                id_field = self.FORMAT_ID % initial_arguments[i].dimension.pk
                self.fields[id_field] = forms.ModelChoiceField(queryset=initial_arguments[i].dimension.category_dimension_set,
                                                                                                         label=initial_arguments[i].dimension.title,
                                                                                                         initial=initial_arguments[i].category_dimension.id,
                                                                                                         help_text=initial_arguments[i].dimension.description)

                id_field_note = self.FORMAT_ID_NOTE % initial_arguments[i].dimension.pk
                self.fields[id_field_note] = forms.CharField(initial=initial_arguments[i].note,
                                                             widget=forms.Textarea,
                                                             label='',
                                                             required=False)
        if dimensions:
            for dim in dimensions:
                self.fields[self.FORMAT_ID % dim.pk ] = forms.ModelChoiceField(queryset=dim.category_dimension_set,
                                                                               label=dim.title,
                                                                               help_text=dim.description)
                self.fields[self.FORMAT_ID_NOTE % dim.pk] = forms.CharField(widget=forms.Textarea,
                                                                            label='',
                                                                            required=False)
