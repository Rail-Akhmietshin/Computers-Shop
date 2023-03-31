import re
from typing import List, Union
from django.db.models import QuerySet
from .models import MainSpecification, Product

class Details:

    def __init__(self, request) -> None:
        self.user_filters = [[key, value] for key, value in request.GET.items() if value]

        self.category_name = self.user_filters.pop(0).pop()
        # print(self.category_name)

        self.parameters = Product.objects.filter(category__name = self.category_name).values('id', 'details__parameters')
        self.filters = MainSpecification.objects.filter(category__name = self.category_name).exclude(filter_name=None).values_list('main_specification_name', 'specification_name',  'feature')
        
        self.unique_parameters = {}
        self.intermediate_data = {}
        self.price = {}

    def unique_parameters_from_db(self) -> None:
        for data in self.parameters:

            details = data.get('details__parameters')

            if not details == 1:
                for main_key, key, feature in self.filters:
                    print(details, main_key, key)
                    value = details.get(main_key).get(f" {key} ").strip()
                    
                    if key == 'Модель':                                     
                        value = re.search(r"([a-zA-Z]+)", value).group()

                    if not self.unique_parameters.get(key):
                        self.unique_parameters[key] = set()

                    if feature and (not type(value) == int and not value.isdigit()):
                        
                        value = re.findall(r"[0-9]+\.?[0-9]?\s{1}", value)[0].strip()
                        
                    self.unique_parameters[key].add(value)

    def normalize_user_filters(self) -> None:
        self.unique_parameters_from_db()

        for filter in self.user_filters:
            key, value = filter
            
            if key.startswith('min') or key.startswith('max'):
                preffix = key[:3]
                key = key[3:]

                if key == 'price':
                    self.price[preffix] = value
                    continue 

                if self.intermediate_data.get(key):
                    self.intermediate_data[key][preffix] = value
                else:
                    self.intermediate_data[key] = { preffix: value }

                continue

            if key[-1].isdigit():
                key = key.split("_")[0]
            
            if not self.intermediate_data.get(key):
                self.intermediate_data[key] = set()

            self.intermediate_data[key].add(value)

    def conversion_to_single_type(self, unique_value, minimal, maximal, value) -> set:
        new_values_db = set()
                    
        if len(value) == 5:         # Если int
            if minimal and maximal:    # Если задан только min или max
                new_values_db.update([x for x in unique_value if int(minimal) <= int(x) and int(x) <= int(maximal) ])    
            elif minimal:
                new_values_db.update([x for x in unique_value if int(minimal) <= int(x)])
            else:                   
                new_values_db.update([x for x in unique_value if int(maximal) >= int(x)])
        else:               # Если float
            if minimal and maximal:
                new_values_db.update([x for x in unique_value if float(minimal) <= float(x) and float(x) <= float(maximal) ]) 
            elif minimal:
                new_values_db.update([x for x in unique_value if float(minimal) <= float(x)])
            else:
                new_values_db.update([x for x in unique_value if float(maximal) >= float(x)])
       
        return new_values_db

    def normalize_current_data(self) -> None:
        self.normalize_user_filters()
        for db_key, db_value in self.unique_parameters.items():
            if db_key in self.intermediate_data:
                if type(self.intermediate_data[db_key]) == dict:
                    value = [x for x in list(db_value)[:5] if x.isdigit()]
                    minimal, maximal = self.intermediate_data.get(db_key).get('min'), self.intermediate_data.get(db_key).get('max')
                
                    new_values_db = self.conversion_to_single_type(db_value, minimal, maximal, value)
                            
                    self.intermediate_data[db_key] = new_values_db
                    
                    continue
                else:
                    self.intermediate_data[db_key].intersection(db_value)
            else:
                self.intermediate_data[db_key] = db_value
        
    def find_current_products(self) -> dict:
        find_id = {}

        for data in self.parameters:
            id = data.get('id')
            details = data.get('details__parameters')
            if not details == 1:
                for main_key, key, feature in self.filters:
                    for filter_key, filter_value in self.intermediate_data.items():

                        if filter_key == key:
                            
                            value = details.get(main_key).get(f" {key} ").strip()

                            if key == 'Модель':
                                value = re.search(r"([a-zA-Z]+)", value).group()

                            if feature and (not type(value) == int and not value.isdigit()):
                                value = re.findall(r"[0-9]+\.?[0-9]?\s{1}", value)[0].strip()


                            if value in filter_value:
                                
                                if not find_id.get(id):
                                    find_id[id] = 0
                                find_id[id] += 1
        return find_id

    def get_id_product_satisfying_request(self, find_id) -> list:
        suitables_id = []

        if self.intermediate_data.get('page'):
            suitables_id = [key for key, value in find_id.items() if value == len(self.intermediate_data) - 1]
        else:
            suitables_id = [key for key, value in find_id.items() if value == len(self.intermediate_data)]    
        
        return suitables_id

    def get_min_and_max_price(self) -> tuple:
        return self.price.get('min'), self.price.get('max')

    def get_ready_data(self) -> Union[QuerySet, List[Product]]:
        self.normalize_current_data()
        suitables_id = self.get_id_product_satisfying_request(self.find_current_products())
        price_min, price_max = self.get_min_and_max_price()

        if price_min and price_max:    
            return Product.objects.filter(id__in = suitables_id, price__range = (price_min, price_max))
        elif price_min:
            return Product.objects.filter(id__in = suitables_id, price__gte = price_min)
        elif price_max:                   
            return Product.objects.filter(id__in = suitables_id, price__lte = price_max)
        else:
            return Product.objects.filter(id__in = suitables_id)