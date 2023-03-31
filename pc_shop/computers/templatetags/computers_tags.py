from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Min, Max
from computers.models import *
import re
from datetime import datetime

register = template.Library()

@register.simple_tag
def get_categories_for_navbar():
    return Category.objects.all()

@register.simple_tag
@stringfilter
def price_formatting(price):
    return " ".join(re.findall(r"[\d]{1,3}", price[::-1]))[::-1]


@register.simple_tag
def normalize_date():
    from random import randint
    months = ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    day = datetime.now().day + randint(1, 5)
    month = months[datetime.now().month]
    return f"{day} {month}"



@register.simple_tag
def min_max_price(category_id: int):
    if category_id:
        return Product.objects.filter(category_id = category_id).aggregate(Min('price'), Max('price'))
    return Product.objects.none()



@register.simple_tag
def filter_names(category_id: int):
    return MainSpecification.objects.filter(category_id = category_id).exclude(filter_name=None).order_by("id")
    

@register.simple_tag
def subfilter_values(category_id, filters):
    
    parameters = Product.objects.filter(category_id = category_id).values('details__parameters')
    filters = filters.values_list('main_specification_name', 'specification_name', 'filter_name', 'feature')

    #print(filters)
    some_data = {}
    
    dlt = []

    i = 1450
    for data in parameters[2:]:
        
        new_data = data.get("details__parameters")

        if not new_data == 1:
            for main_key, key, filter_name, feature in filters:
                try:
                    value = new_data.get(main_key).get(f" {key} ").strip()
                except:
                    break
                if filter_name == 'Производитель':
                    value = re.search(r"([a-zA-Z]+)", value).group()

                if not some_data.get(filter_name):
                    some_data[filter_name] = set()

                if value.isdigit():
                    value = int(value)

                if feature and not type(value) == int:
                    new_value = re.findall(r"[0-9]+\.?[0-9]?\s{1}", value)[0].strip()
                    
                    if new_value.isdigit():
                        value = int(new_value)
                    else:
                        value = float(new_value)

                some_data[filter_name].add(value)
    
    for key, value in some_data.items():
        try:
            some_data[key] = sorted(list(value))
        except:
            some_data[key] = list(value)
    
    return some_data

@register.simple_tag
def checked_result(request_data, key1, key2):
    key = f"{key1}_{key2}"
    if key in request_data:
        return True
    return False

@register.simple_tag
def checked_feature(request_data, key, min_or_max: str):
    key = min_or_max + key
    
    if key in request_data:
        return request_data[key]
    return False
    

@register.simple_tag
def data_for_main_specifications(data: dict, category: int):
    main_specification_names = MainSpecification.objects.filter(category_id = category).values_list('main_specification_name', 'specification_name')
    
    result = []
    for key in main_specification_names:
        value = data.get(key[0]).get(f" {key[1]} ")
        if value == None:
            continue
        result.append(f"{key[1]}: {value}")
    return result


