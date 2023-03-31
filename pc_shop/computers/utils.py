from typing import Union
from django.contrib.auth.base_user import BaseUserManager
from re import findall as find_price

def get_category_name(instance, filename):
    return '/'.join([instance.category.name, filename])

def get_category(instance, filename):
    return '/'.join(['Категории', instance.name, filename])

def normalize_price(price: Union[str, list]):
    if type(price) == list:
        price = price[0]
    return "".join(find_price(r"([0-9 ]+)\s{1}₽", price)[0].split(" "))

class UserManager(BaseUserManager):

    def create_user(self, email, number_phone, password=None):
        if not email:
            raise ValueError("Почта обязательна")
        
        if not number_phone:
            raise ValueError("Номер телефона обязателен")

        user = self.model(
            email = self.normalize_email(email),
            number_phone = number_phone,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, number_phone, password=None):
        user = self.create_user(
            email, number_phone, password,  
        )
        user.is_admin = True
        user.save(using=self._db)

        return user