from django import forms
from django.forms import ModelForm
from Products.filters import Filters
from Products.models import ProductReviews

class ProductFilter(forms.Form):
    """
    A class that extends Django's default Form class.
    This class is used for creating a form used as a product filter.

    Attributes
    ----------
    FILTER_CHOICES : list
        A list of 2-tuples that contain the filter choice name in the model and user representation name.
    product_filter
        Represents the product filter.
    """

    FILTER_CHOICES = Filters().get_product_filters()
    product_filter = forms.ChoiceField(choices=FILTER_CHOICES,required=True)

    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(ProductFilter, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['product_filter'].widget.attrs.update({'class':'form-control','required':'True'})

class RatingForm(ModelForm):
    """
    A class that extends Django's ModelForm.
    It models the product rating form for users.

    Attributes
    ----------
    CHOICES : list
        A list of 2-tuples that contain the filter choice number in the model and user representation name.
    rating : str
        Collects the rating choice of a user.
    """
    CHOICES = [
        ('5','★'),
        ('4','★'),
        ('3','★'),
        ('2','★'),
        ('1','★'),
    ]
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())

    class Meta:
        """
        An inner class that specifies the meta data of the Model class.
        In this case the model's default field configurations have been Overrided.

        Attributes
        ----------
        model : ProductReviews
            Specifies the model related to the form.
        fields : list
            Contains the fields to be rendered in the form.
        """
        model = ProductReviews
        fields = ['rating','comment']

    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(RatingForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['comment'].widget.attrs.update({'class':'form-control', 'rows':'8','placeholder':'Add your comment here'})
