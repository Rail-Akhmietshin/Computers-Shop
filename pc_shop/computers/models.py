import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .utils import UserManager
from django.urls import reverse
from django.utils.text import slugify
from .utils import get_category_name, get_category

from .tasks import send_verification_email
from django.db.models import signals

def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_confirmation:
        send_verification_email.delay(instance.id)

    
class Specification(models.Model):
    ''' Подробные характеристики товара'''

    parameters = models.JSONField("Подробные характеристики")

    def save(self, *args, **kwargs) -> None:
        super(Specification, self).save(*args, **kwargs)
        

class MainSpecification(models.Model):
    ''' Основные характеристики товаров одной категории '''

    main_specification_name = models.CharField(max_length = 100)
    specification_name = models.CharField(max_length = 100)
    filter_name = models.CharField(max_length = 100, null=True)
    feature = models.BooleanField(default=False)
    category = models.ForeignKey("Category", null = True, on_delete = models.SET_NULL)

class Category(models.Model):
    ''' Категории комплектующих для ПК'''

    name = models.CharField(max_length = 50)
    plural_name = models.CharField(max_length = 50)
    photo = models.ImageField(upload_to = get_category)
    slug = models.SlugField()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.cat_slug = slugify(self.name)
        return super(Product, self).__init__(*args, **kwargs)


class Product(models.Model):
    ''' Комплектующие '''

    name = models.CharField(max_length = 150)
    price = models.PositiveIntegerField()
    photo = models.ImageField(max_length = 255, upload_to = get_category_name)
    slug = models.SlugField(max_length=255)
    availability = models.BooleanField(default = True)
    category = models.ForeignKey("Category", on_delete = models.PROTECT)
    details = models.OneToOneField("Specification", on_delete = models.CASCADE)


    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
         return reverse('product', kwargs = {'post_slug' : self.slug})
    
    class Meta:
        ordering = ['name']


class User(AbstractBaseUser):
    ''' Пользователь '''

    number_phone = models.CharField(max_length = 13, db_index=True, unique=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    
    verification_uuid = models.UUIDField(default=uuid.uuid4, verbose_name="Уникальный ключ")

    is_active = models.BooleanField(default=True)
    is_confirmation = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'     
    REQUIRED_FIELDS = ['number_phone']

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
        ordering = ['is_admin', 'number_phone']

    

    def __str__(self) -> str:
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    



signals.post_save.connect(user_post_save, sender=User)
