from Products.models import Product
from Ebooks.models import Ebook
import csv
with open('static/csv/final_ebooks.csv',encoding="utf-8") as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for row in reader:
        product = Product(SKU=row[0],Title=row[1],Author=row[2],Genre=row[3],Price=row[4],Image_URL=row[5])
        ebook = Ebook(product=product)
        try:
            product.save()
            ebook.save()
        except:
            pass
