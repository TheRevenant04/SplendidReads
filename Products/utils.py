from django.db.models import F
from Products.filters import Filters
from Products.models import AvgProductRatings, Product, ProductReviews, ProductSales

def bestsellers_filter(products):
    """
    A function that filters products according to number of copies sold in descending order.

    Attributes
    ----------
    products : list
        Products to be filtered.

    Returns
    -------
    Filtered products.
    """
    filtered_products = products.select_related('productsales').order_by('-productsales__copies_sold')
    return filtered_products

def compute_avg_rating(product, rating):
    """
    A function that computes the average rating of a product.

    Parameters
    ----------
    product : Product
        Represents a product.
    rating : int
        Represents a rating given by a user.

    Returns
    -------
    The average product rating of a product.
    """
    rating = float(rating)
    avg_product = get_reviewed_product(product)
    avg_product_ratings = avg_product.avg_rating
    no_of_ratings = avg_product.no_of_ratings
    avg_product_rating = avg_product_ratings + ((rating - avg_product_ratings) / (no_of_ratings + 1))
    return avg_product_rating

def genre_filter(genre):
    """
    A function that filters products according to genre.

    Attributes
    ----------
    genre : str
        Specifies product genre for product retrieval.

    Returns
    -------
    Filtered products.
    """
    filtered_products = Product.objects.filter(Genre=genre)
    return filtered_products

def get_all_products():
    """
    A function that retrieves all products.

    Returns
    -------
    All retrieved products.
    """
    products = Product.objects.select_related('avgproductratings')
    return products

def get_all_product_reviews(product):
    """
    A function that retrieves all products reviews of a product.

    Returns
    -------
    All retrieved product reviews.
    """
    product_reviews = ProductReviews.objects.filter(product=product)
    return product_reviews

def get_best_sellers(limit):
    """
    A function that retrieves some of the best selling products.

    Parameters
    ----------
    limit : int
        The maximum number of products that can be retrieved.

    Returns
    -------
        The best selling products.
    """
    all_bestsellers = Product.objects.select_related('productsales').order_by('-productsales__copies_sold')
    bestsellers = all_bestsellers[:limit]
    return bestsellers

def get_product(SKU):
    """
    A function that retrieves a product.
    It uses product SKU for retrieval.

    Attributes
    ----------
    SKU : str
        The stock keeping unit of a product.

    Returns
    -------
    A retrieved product if it exists or None.
    """
    try:
        product = Product.objects.get(SKU=SKU)
        return product
    except:
        return None

def get_product_reviews(product, limit):
    """
    A function that retrieves some product reviews of a product.

    Parameters
    ----------
    product : str
        Represents a product.
    limit : int
        Represents an integer limit.

    Returns
    -------
    Some retrieved product reviews.
    """
    product_reviews = ProductReviews.objects.filter(product=product)[:limit]
    return product_reviews

def get_product_sale_details(product):
    """
    A function that retrieves a product's sale details.

    Parameters
    ----------
    product : Product
        Represents a product.

    Returns
    -------
    Product sale details if they exist, otherwise None.
    """
    try:
        product_sale = ProductSales.objects.get(product=product)
        return product_sale
    except:
        return None

def get_reviewed_product(product):
    """
    A function that retrieves a reviewed product.

    Parameters
    ----------
    product : Product
        Represents products.

    Returns
    -------
    The reviews of a product.
    """
    try:
        avg_ratings = AvgProductRatings.objects.get(product=product)
        return avg_ratings
    except:
        return None

def get_top_rated(limit):
    """
    A function that retrieves products with highest ratings.

    Parameters
    ----------
    limit : int
        Represents the number of products to be retrieved.

    Returns
    -------
    Top rated products.
    """
    all_top_rated_products = Product.objects.select_related('avgproductratings').order_by('-avgproductratings__avg_rating')
    top_rated_products = all_top_rated_products[:limit]
    return top_rated_products

def high_to_low_filter(products):
    """
    A function that filters products in descending order of price.

    Attributes
    ----------
    products : list
        Products to be filtered.

    Returns
    -------
    Filtered products.
    """
    filtered_products = products.order_by('-Price')
    return filtered_products

def is_reviewed(customer, product):
    """
    A function that checks whether a customer reviewed a product.

    Parameters
    ----------
    customer : User
        Represents the site's users.
    product : Product
        Represents a product.

    Returns
    -------
    True, if a customer reviewed a product, otherwise False.
    """
    try:
        product = ProductReviews.objects.get(customer=customer, product=product)
        return True
    except:
        return False

def latest_filter(products):
    """
    A function that filters products in descending order of product existence.

    Attributes
    ----------
    products : list
        Products to be filtered.

    Returns
    -------
    Filtered products.
    """
    return products

def low_to_high_filter(products):
    """
    A function that filters products in sorted order according to price.

    Attributes
    ----------
    products : list
        Products to be filtered.

    Returns
    -------
    Filtered products.
    """
    filtered_products = products.order_by('Price')
    return filtered_products

def product_filter(filter, **kwargs):
    """
    A function that filters products.

    Attributes
    ----------
    filter : str
        Represents the filter selected by the user.
    **kwargs
        Variable named arguments.

    Returns
    -------
    Filtered products.
    """
    filters_object = Filters()
    filters= filters_object.get_product_filters()

    if 'genre' in kwargs:
        genre = kwargs['genre']
        products = genre_filter(genre)
    elif 'items' in kwargs:
        items = kwargs['items']
        products = items
    else:
        products = get_all_products()
    if filter == filters[1][0]:
        return low_to_high_filter(products)
    elif filter == filters[2][0]:
        return high_to_low_filter(products)
    elif filter == filters[3][0]:
        return bestsellers_filter(products)
    elif filter == filters[4][0]:
        return latest_filter(products)
    elif filter == filters[5][0]:
        return top_rated_filter(products)
    else:
        return products

def search_filter(search_keyword, limit=None):
    """
    A function that retrieves products based on a search query.

    Parameters
    ----------
    search_keyword : str
        A search query to retrieve products.
    limit : int
        The maximum number of products to be retrieved. It is optional.

    Returns
    -------
    Products if the search query is matched, otherwise None.
    """
    if limit is None:
        search_products = Product.objects.filter(Title__icontains=search_keyword)
    else:
        search_products = Product.objects.filter(Title__icontains=search_keyword)[:5]
    return search_products

def search_filter_refine(search_products):
    """
    A function that retrieves particular fields of searched products.

    Parameters
    ----------
    search_products : Product
        A list of searched products.
    Returns
    -------
    Specific fields of Products.
    """
    try:
        refined_searched_products = search_products.values(label=F('Title'),value=F('SKU'))
        return refined_searched_products
    except:
        return None

def set_avg_product_review(customer, product, rating):
    """
    A function that updates the average product rating of a product.

    Parameters
    ----------
    customer : User
        Represents a site user.
    product : Product
        Represents a product.
    rating : int
        A rating provided by a user.
    """
    avg_product = get_reviewed_product(product)
    if avg_product is not None:
        avg_product.avg_rating = compute_avg_rating(product, rating)
        avg_product.no_of_ratings = avg_product.no_of_ratings + 1
        avg_product.save()
    else:
        avg_product = AvgProductRatings(product=product, no_of_ratings=1, avg_rating=rating)
        avg_product.save()

def set_product_sale_count(product):
    """
    A function that creates ProductSales objects or updates the sales count of a product.

    Parameters
    ----------
    product : Product
    """
    product_sale = get_product_sale_details(product)
    if product_sale is None:
        new_sale = ProductSales(product=product, copies_sold = 1)
        new_sale.save()
    else:
        product_sale.copies_sold =product_sale.copies_sold + 1
        product_sale.save()

def SKU_filter(SKU):
    """
    A function that retrieves products with a given SKU.

    Attributes
    ----------
    SKU : str
        Stock Keeping Unit.

    Returns
    -------
    Filtered product.
    """
    filtered_products = Product.objects.get(SKU=SKU)
    return filtered_products

def top_rated_filter(products):
    """
    A function that filters products in descending order of average product ratings.

    Attributes
    ----------
    products : list
        Products to be filtered.

    Returns
    -------
    Filtered products.
    """
    filtered_products = products.select_related('avgproductratings').order_by('-avgproductratings__avg_rating')
    return filtered_products
