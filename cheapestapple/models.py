from django.db import models

class ReviewSite(models.Model):
    site_name = models.CharField(verbose_name = 'Review Site', max_length = 500)
    image = models.ImageField(verbose_name = 'eTailer Graphic', upload_to = 'img/', null = True, blank = True)
    url = models.URLField(verbose_name = 'Site URL')
    
    def __unicode__(self):
        return str(self.id) + "<-->" + self.site_name

class Review(models.Model):
    exclusive = models.BooleanField(verbose_name = 'Exclusive Review')
    score = models.IntegerField(verbose_name = 'Score (out of 10)')
    #if exclusive is true
    review = models.TextField(verbose_name = 'CheapestApple review', max_length = 5000, blank = True, null = True)
    #if its not exclusive
    site_name = models.ForeignKey(ReviewSite, verbose_name = 'Review Site', null = True, blank = True)
    link = models.URLField(verbose_name = 'Review Link', null = True, blank = True)
    product = models.ManyToManyField("Product", related_name = 'related_products_for_review', verbose_name = 'Product', null = True, blank = True)
    
    def __unicode__(self):
        return str(self.id) + "<-->" + self.site_name.site_name

class Store(models.Model):
    etailer = models.CharField(verbose_name = 'eTailer', max_length = 500)
    image = models.ImageField(verbose_name = 'eTailer Graphic', upload_to = 'img/', null = True, blank = True)
    url = models.URLField(verbose_name = 'Store URL')
    
    def __unicode__(self):
        return str(self.id) + "<-->" + self.etailer

class Price(models.Model):
    etailer = models.ForeignKey(Store, verbose_name = 'eTailer')
    product = models.ManyToManyField("Product", related_name = 'related_products', verbose_name = 'Product', null = True, blank = True)
    price = models.FloatField(verbose_name = 'Price')
    link = models.URLField(verbose_name = 'Prod Link')
    
    def __unicode__(self):
        return str(self.id) + "<-->" + str(self.price) + ' ' + self.etailer.etailer

class Product(models.Model):
    title = models.CharField(verbose_name = 'Product', max_length = 500)
    desc_line_1 = models.CharField(verbose_name = 'Description Line 1', max_length = 500)
    desc_line_2 = models.CharField(verbose_name = 'Description Line 2', max_length = 500)
    image = models.ImageField(verbose_name = 'Product Image', upload_to = 'img/', null = True, blank = True)
    prices = models.ManyToManyField(Price, verbose_name = 'Prices', related_name = 'related_prices', null = True, blank = True) 
    reviews = models.ManyToManyField(Review, verbose_name = 'Reviews', related_name = 'related_reviews', null = True, blank = True)
    
    def __unicode__(self):
        return str(self.id) + "<-->" + self.title + ' <--> ' + self.desc_line_1 + ' <--> ' + self.desc_line_2   

class Box(models.Model):
    # for all
    title = models.CharField(verbose_name = 'Box Title', max_length = 500)
    image = models.ImageField(verbose_name = 'Product Image', upload_to = 'img/', null = True, blank = True)
    parent = models.ForeignKey("self", related_name = 'related_parent', verbose_name = 'Box Parent', null = True, blank = True)
    message = models.CharField(verbose_name = 'Message', max_length= 500, null = True, blank = True)
    # type 1, tree
    child = models.ManyToManyField("self", related_name = 'related_child', verbose_name = 'Box Child', null = True, blank = True, symmetrical = False)
    # type 2, models
    is_product_box = models.BooleanField(verbose_name = 'Product Box', default = False)
    product_box = models.ManyToManyField(Product, verbose_name = 'Products', null = True, blank = True)
    
    def __unicode__(self):
        return self.title