from userauths.models import User
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField

STATUS_CHOICES = (
    ('processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('pubished', 'Published')
)

RATING = (
    (1, '⭐'),
    (2, '⭐⭐'),
    (3, '⭐⭐⭐'),
    (4, '⭐⭐⭐⭐'),
    (5, '⭐⭐⭐⭐⭐'),
)


# This creates a folder for each users and stores whatever image they upload
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        # (self.image.url) is gonna replace '%s'
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Tags(models.Model):
    pass


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefgh12345')

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    cover_image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = RichTextUploadingField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, default='123 Main street')
    contact = models.CharField(max_length=100, default='+123 (456) 789')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        # (self.image.url) is gonna replace '%s'
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh12345')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor')

    title = models.CharField(max_length=100, default='Fresh Pear')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = RichTextUploadingField(null=True, blank=True, default='This is the product')
    
    price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default='2.99')
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    
    tags = TaggableManager(blank=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default='in_review')

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    
    #sku is a little short code that identifies each product
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet='1234567890')

    date = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(null=True, blank=True)

    specifications = RichTextUploadingField(null=True, blank=True)
    type = models.CharField(max_length=100, default='organic', null=True, blank=True)
    stock_count = models.CharField(max_length=100, default='10', null=True, blank=True)
    life = models.CharField(max_length=100, default='100 Days', null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False,  null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Products'

    def product_image(self):
        # (self.image.url) is gonna replace '%s'
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
    #To get the percentage discount for each product
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')


    def __str__(self):
        return f'{self.user}--{self.product}--{self.price}'
    
    def multiply_price(self):
        new_price =  self.price * int(self.quantity)
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to='product-images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='p_images')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'




########################################## Cart, Order, OrderItem and Address
########################################## Cart, Order, OrderItem and Address
########################################## Cart, Order, OrderItem and Address


class Cartorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=100, null=True,blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    
    
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    coupons = models.ManyToManyField('core.coupon', blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    saved = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')

    shipping_method = models.CharField(max_length=100, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website = models.CharField(max_length=100, null=True, blank=True)


    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    Product_status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='processing')

    sku = ShortUUIDField(blank=True, length=4, max_length=10, prefix='SKU',  alphabet='123456789')
    oid = ShortUUIDField(blank=True, length=4, max_length=10, alphabet='123456789')


    stripe_payment = models.CharField(max_length=1000, blank=True, null=True)


    class Meta:
        verbose_name_plural = 'Cart Order'

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Coupon'

    def __str__(self):
        return self.code

class CartOrderItems(models.Model):
    order = models.ForeignKey(Cartorder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')
    total = models.DecimalField(max_digits=12, decimal_places=2, default='0.00')

    class Meta:
        verbose_name_plural = 'Cart order items'

    def order_img(self):
        # (self.image.url) is gonna replace '%s'
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))
    
########################################## Product Review, Wishlists, Address
########################################## Product Review, Wishlists, Address
########################################## Product Review, Wishlists, Address
########################################## Product Review, Wishlists, Address


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return self.product.title 

    def get_rating(self):
        return self.rating
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'wishlists'

    def __str__(self):
        return self.product.title 

    def get_rating(self):
        return self.rating
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    
    class Meta:
        verbose_name_plural = 'Address'

