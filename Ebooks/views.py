from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from Ebooks.utils import get_customer_ebooks

@method_decorator(login_required, name='dispatch')
class MyEbooksView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render a user's ebooks.

    Attributes
    ----------
    template_name : str
        Represents the template that the view renders.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """
    template_name = "Ebooks/my_ebooks.html"

    def get_context_data(self, **kwargs):
        """
        Returns a dictionary representing the template context.
        Retrieves a user's ebook objects from the 'MyEbooks' model.

        Parameters
        ----------
        **kwargs
            Optional named arguments.
        """
        context = super(MyEbooksView, self).get_context_data(**kwargs)
        user_ebooks = get_customer_ebooks(self.request.user)
        if user_ebooks is not None:
            context['user_ebooks'] = user_ebooks
        else:
            context['message'] = "You currently do not have any ebooks."
        return context
