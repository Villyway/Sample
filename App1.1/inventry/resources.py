from import_export import resources
from products.models import Product
from inventry.models import SimpleStockUpdte
from import_export.fields import Field
from utils.constants import StockTransection

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ("part_no","name","code","category__name","quality_type__name")
        export_order = ("part_no","name","code","category__name","quality_type__name")


class StockUpdateReport(resources.ModelResource):
    part_no = Field(column_name='Part No.')
    description = Field(column_name='Description')
    time = Field(column_name='Date-Time')
    old_stock = Field(column_name='Old Stock')
    issued = Field(column_name='Issued')
    received = Field(column_name='Received')
    current_stock = Field(column_name='Current Stock')

    def dehydrate_part_no(self,SimpleStockUpdte):
        part = getattr(SimpleStockUpdte, "part", "unknown")
        return part.part_no
    
    def dehydrate_description(self,SimpleStockUpdte):
        part = getattr(SimpleStockUpdte, "part", "unknown")
        return part.name
    
    def dehydrate_time(self,SimpleStockUpdte):
        date = getattr(SimpleStockUpdte, "created_at", "unknown")
        return date.strftime("%d-%m-%Y %H:%M:%S")
    
    def dehydrate_old_stock(self,SimpleStockUpdte):
        return getattr(SimpleStockUpdte, "old_stock", "unknown")
    
    def dehydrate_issued(self,SimpleStockUpdte):
        received_qty = getattr(SimpleStockUpdte, "received_qty", "unknown")
        transection_type = getattr(SimpleStockUpdte, "transection_type", "unknown")
        if transection_type == StockTransection.DR.value:
            return "-" + str(received_qty)
        else:
            return "-"
    
    def dehydrate_received(self,SimpleStockUpdte):
        received_qty = getattr(SimpleStockUpdte, "received_qty", "unknown")
        transection_type = getattr(SimpleStockUpdte, "transection_type", "unknown")
        if transection_type == StockTransection.CR.value:
            return "+" + str(received_qty)
        else:
            return "-"
    
    def dehydrate_current_stock(self,SimpleStockUpdte):
        return getattr(SimpleStockUpdte, "quantity_on_hand", "unknown")
    
    
    
    class Meta:
        model = SimpleStockUpdte
        fields = ("part_no","description","time","old_stock","issued","received","current_stock")
        export_order = ("part_no","description","time","old_stock","issued","received","current_stock")
        