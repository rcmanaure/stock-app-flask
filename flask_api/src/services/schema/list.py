from marshmallow import (
    Schema      
)

class StockResponseSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ('symbol', 'name', 'qty', 'last_price')
        
