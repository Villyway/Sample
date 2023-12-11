from import_export import resources
from import_export.fields import Field

from utils.constants import OrderStatus
from orders.models import OrderOfProduct 



class OrderReport(resources.ModelResource):
    # order_no = Field(column_name='Order No.')
    # order_date = Field(column_name='Order Date.')
    # customer_name = Field(column_name='Customer Name')
    # time = Field(column_name='Date-Time')
    # old_stock = Field(column_name='Old Stock')
    # issued = Field(column_name='Issued')
    # received = Field(column_name='Received')
    # current_stock = Field(column_name='Current Stock')

    # def dehydrate_order_no(self,OrderOfProduct):
    #     order = getattr(OrderOfProduct, "order", "unknown")
    #     return order.order_no    
    
    # def dehydrate_order_date(self,OrderOfProduct):
    #     order = getattr(OrderOfProduct, "order", "unknown")
    #     return order.date    
    
    # def dehydrate_customer_name(self,OrderOfProduct):
    #     order = getattr(OrderOfProduct, "order", "unknown")
    #     return order.customer.name
    
    class Meta:
        model = OrderOfProduct  # sl.no, Customer Name, Order No, Date, Part No, Category, name, other specification, order Qty, UOM, Packing type, Order Status, sales challan, bill No, Lr No, dispatch date, transport details, deliverd date, remark
        fields = ('order__order_no','order__date','order__customer__name','product__code','product__name','order_qty','uom','packing_type','status', 'invoice_no', 'transport_compny', 'lr_no', 'dispatch_status', 'dispatch_date', 'delivered_date')
        export_order = ('order__order_no','order__date','order__customer__name','product__code','product__name','order_qty','uom','packing_type','status', 'invoice_no', 'transport_compny', 'lr_no', 'dispatch_status', 'dispatch_date', 'delivered_date')
        