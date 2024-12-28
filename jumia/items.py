import scrapy
from itemloaders.processors import TakeFirst,MapCompose,Join,Compose
import re

def clean_value(value):
    try:
        return value[0].removeprefix('KSh').replace(',','').strip()
    except (IndexError, AttributeError):
        value = [0]
        return value[0]
    
class JumiaItem(scrapy.Item):
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    brand = scrapy.Field(
        output_processor = TakeFirst()
    )
    new_price = scrapy.Field(
        input_processor = Compose(lambda v:v[0],lambda u: u.removeprefix('KSh').replace(',','').strip()),
        output_processor = TakeFirst()
    )
        
    old_price = scrapy.Field()
