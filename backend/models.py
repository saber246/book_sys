from tortoise import fields
from tortoise.models import Model


class Book(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    author = fields.CharField(max_length=255)
    ISBN = fields.CharField(max_length=255)
    publisher = fields.CharField(max_length=255)
    publish_date = fields.DateField()
    price = fields.DecimalField(max_digits=8, decimal_places=2)
    category = fields.CharField(max_length=255)
    location = fields.CharField(max_length=255)
    stock = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta: # type: ignore
        table = "books"
    
    
    