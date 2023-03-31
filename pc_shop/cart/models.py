from django.db import models
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Cart(models.Model):
    creation_date = models.DateTimeField(verbose_name='creation date')
    checked_out = models.BooleanField(default=False, verbose_name='checked out')

    class Meta:
        verbose_name = ('cart',)
        verbose_name_plural = ('carts',)
        ordering = ('-creation_date',)

    def __str__(self):
        return str(self.creation_date)


class ItemManager(models.Manager):
    def get(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        if 'product' in kwargs:
            kwargs['content_type'] = ContentType.objects.get_for_model(type(kwargs['product']))
            kwargs['object_id'] = kwargs['product'].pk
            del(kwargs['product'])
        return super(ItemManager, self).filter(*args, **kwargs)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity')
    unit_price = models.DecimalField(max_digits=18, decimal_places=2, verbose_name='unit price')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    objects = ItemManager()

    class Meta:
        verbose_name = ('item',)
        verbose_name_plural = ('items',)
        ordering = ('cart',)

    def __str__(self):
        return f"{self.quantity} units of {self.product.__class__.__name__}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price
    

    @property
    def product(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    @product.setter
    def product(self, product):
        self.content_type = ContentType.objects.get_for_model(type(product))
        self.object_id = product.pk