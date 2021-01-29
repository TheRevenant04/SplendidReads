from Cart.utils import get_cart_product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.utils.decorators import method_decorator
from Ebooks.utils import get_customer_ebook, get_ebook, is_purchased
from Products.filters import Filters
from Products.forms import ProductFilter, RatingForm
from Products.models import AvgProductRatings, Product, ProductReviews
from Products.utils import genre_filter, get_all_products, get_all_product_reviews, get_product,get_product_reviews, get_top_rated, is_reviewed
from Products.utils import product_filter,set_avg_product_review, get_best_sellers, search_filter, search_filter_refine
import random

class AutoCompleteView(View):
    """
    A view that extends Django's default View.
    This view is used to render The search bar's autocomplete feature.

    Methods
    -------
    get(self, request, *args, **kwargs)
        Handles GET requests.
    """
    def get(self, request, *args, **kwargs):
        """
        Retrieves products based on search queries.

        Attributes
        ----------
        request : HttpRequest
            A request object.
        *args
            Unnamed variable arguments.
        **kwargs
            Named Variable arguments.

        Returns
        -------
        Returns retrieved products in Json format.
        """
        search_keyword = request.GET.get('term')
        limit = 5
        if search_keyword:
            search_products = search_filter_refine(search_filter(search_keyword, limit))
            search_results = list(search_products)
            return JsonResponse(search_results, safe=False)

class GenrePageView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render the genres page to a user.

    Attributes
    ----------
    template_name : str
        The html page for the user response.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """
    template_name = "Products/genres.html"

    def get_context_data(self,**kwargs):
        """
        Renders the genres on the genre page.

        Parameters
        ----------
        **kwargs
            Variable arguments.

        Returns
        -------
        Returns a dictionary representing the template context.
        """
        context = super(GenrePageView, self).get_context_data(**kwargs)
        genres = Product.objects.values_list('Genre').distinct()
        context['genres'] = genres
        return context

class HomePageView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render the home page to a user.

    Attributes
    ----------
    template_name : str
        The html page for the user response.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """
    template_name = "Products/home.html"

    def get_context_data(self,**kwargs):
        """
        Renders the home page with different products.

        Parameters
        ----------
        **kwargs
            Variable arguments.

        Returns
        -------
        Returns a dictionary representing the template context.
        """
        context = super(HomePageView, self).get_context_data(**kwargs)
        products = get_all_products()
        context['featured'] = random.sample(list(products), 12)
        context['bestsellers'] = get_best_sellers(6)
        context['latest'] = random.sample(list(products), 6)
        context['top_rated'] = get_top_rated(6)
        context['filter_tags'] = Filters().get_filter_model_value()
        return context

class ProductPageView(View):
    """
    A view that extends Django's default View class.
    This view is used to render a product's detail page to a user.

    Attributes
    ----------
    template_name : str
        The html page for the user response.
    form_class : RatingForm
        Represents the rating form class.

    Methods
    -------
    get(self, request, *args, **kwargs)
        Handles GET requests.
    post(self, request, *args, **kwargs)
        Handles POST requests.
    """
    template_name = "Products/product_page.html"
    form_class = RatingForm

    def get(self, request, *args, **kwargs):
        """
        Renders a product's details.

        Parameters
        ----------
        request : HttpRequest
            A request object.
        *args
            Unnamed variable arguments.
        **kwargs
            Named Variable arguments.

        Returns
        -------
        Returns a response with the product page.
        """
        context = kwargs
        limit=5
        product = Product.objects.get(pk=context['pk'])
        filtered_products = genre_filter(product.Genre)
        similar_products = random.sample(list(filtered_products), 6)
        product_reviews = get_product_reviews(product, limit)
        context['product'] = product
        context['similar_products'] = similar_products
        context['product_reviews'] = product_reviews
        context['five_stars'] = range(1,6)
        existing_cart_product = None
        user_ebook = None
        if self.request.user.is_authenticated:
            ebook = get_ebook(product)
            user_ebook = get_customer_ebook(self.request.user, ebook)
            existing_cart_product = get_cart_product(self.request.user, product)
            if is_purchased(self.request.user, ebook):
                if not is_reviewed(self.request.user, product):
                    context['rating_form'] = RatingForm()
        if user_ebook is not None:
            context['user_ebook_exists'] = True
        elif existing_cart_product is None:
            context["add_to_cart"] = True
        else:
            context["add_to_cart"] = False
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handles product reviews posted by users.

        Parameters
        ----------
        request : HttpRequest
            A POST request with rating form details.
        *args
            Unnamed variable arguments.
        **kwargs
            Named Variable arguments.

        Returns
        -------
        Redirects to product page.
        """
        form = RatingForm(request.POST)
        context = kwargs
        if form.is_valid():
            book_review = form.save(commit=False)
            book_review.customer = self.request.user
            product = Product.objects.get(pk=context['pk'])
            book_review.product = product
            set_avg_product_review(self.request.user, product ,request.POST.get('rating'))
            form.save()
            return redirect('Products:product_page',pk=context['pk'])
        return redirect('Products:product_page',pk=context['pk'])

class ProductsView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render the product catalog page to a user.

    Attributes
    ----------
    template_name : str
        The html page for the user response.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """
    template_name = "Products/product_catalog.html"

    def get_context_data(self, **kwargs):
        """
        Renders products according to genre and the selected filter.

        Parameters
        ----------
        **kwargs
            Variable arguments.

        Returns
        -------
        Returns a dictionary representing the template context.
        """
        context = super(ProductsView, self).get_context_data(**kwargs)
        if self.request.GET.get('product_filter'):
            context['filter_string'] = self.request.GET.get('product_filter')
            context['filter'] = ProductFilter(self.request.GET)
            if len(context['genre']) > 0:
                filtered_products = product_filter(self.request.GET.get("product_filter"),genre=context['genre'])

        else:
            context['filter'] = ProductFilter()
            if len(context['genre']) > 0:
                filtered_products = genre_filter(context['genre'])

        paginator = Paginator(filtered_products, 30)
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)
        return context

class ProductSearchView(View):
    """
    A view that extends Django's default View class.
    This view is used to render the product catalog page to a user with products that match a user's search.

    Attributes
    ----------
    template_name : str
        The html page for the user response.

    Methods
    -------
    get(self, request, *args, **kwargs)
        Handles GET requests.
    post(self, request, *args, **kwargs)
        Handles POST requests.
    """
    template_name = 'Products/product_catalog.html'

    def get(self, request, *args, **kwargs):
        """
        Renders a list of products That match a search term.

        Parameters
        ----------
        request : HttpRequest
            A request object.
        *args
            Unnamed variable arguments.
        **kwargs
            Named Variable arguments.

        Returns
        -------
        Returns a response with products.
        """
        context = {}
        search_keyword = self.request.GET.get('search_keyword')
        search_results = None
        if search_keyword:
            search_results = search_filter(search_keyword)
        paginator = Paginator(search_results, 30)
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)
        context['search_keyword'] = search_keyword
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Processes search terms posted by users and retrieves products related to the term.

        Parameters
        ----------
        request : HttpRequest
            A POST request with rating form details.
        *args
            Unnamed variable arguments.
        **kwargs
            Named Variable arguments.

        Returns
        -------
        Renders the product catalog page.
        """
        search_keyword = request.POST.get('search')
        context = {}
        search_results = search_filter(search_keyword)
        if search_results:
            paginator = Paginator(search_results, 30)
            page_number = request.GET.get('page')
            context['products'] = paginator.get_page(page_number)
            context['search_keyword'] = search_keyword
        else:
            message = "No Products Found."
            return render(request, self.template_name, {'message':message})
        return render(request, self.template_name, context)

class RatingsPageView(TemplateView):
    """
    A view that extends Django's default TemplateView class.
    This view is used to render a product's reviews page to a user.

    Attributes
    ----------
    template_name : str
        The html page for the user response.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """
    template_name = 'Products/all_product_reviews.html'

    def get_context_data(self, **kwargs):
        """
        Renders product reviews.

        Parameters
        ----------
        **kwargs
            Named variable arguments.

        Returns
        -------
        Returns a dictionary representing the template context.
        """
        context = super(RatingsPageView, self).get_context_data(**kwargs)
        product = get_product(SKU=context['pk'])
        context['product_reviews'] = get_all_product_reviews(product)
        context['five_stars'] = range(1,6)
        return context

class ViewAllView(TemplateView):
    """
    A view that extends Django's default TemplateView class.
    This view is used to render the product catalog page to a user with products that match a particular category.

    Attributes
    ----------
    template_name : str
        The html page for the user response.

    Methods
    -------
    get_context_data(self, **kwargs)
        Handles GET requests.
    """

    template_name = 'Products/product_catalog.html'

    def get_context_data(self, **kwargs):
        """
        Retrieves products based on a particular category.

        Parameters
        ----------
        **kwargs
            Named variable arguments.

        Returns
        -------
        Returns a dictionary representing the template context.
        """
        context = super(ViewAllView, self).get_context_data(**kwargs)

        context['filter_string'] = context['product_filter']
        filtered_products = product_filter(context["product_filter"])
        paginator = Paginator(filtered_products, 30)
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)
        return context
