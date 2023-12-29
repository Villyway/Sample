import datetime

from import_export import resources
from import_export.fields import Field

from utils.constants import OrderStatus
from orders.models import OrderOfProduct 



class OrderReport(resources.ModelResource):

    order_no = Field(column_name='Order No.')
    order_date = Field(column_name='Order Date.')
    customer_name = Field(column_name='Customer Name')
    product_code = Field(column_name='Part No.')
    product_name = Field(column_name='Description')
    product_specifaction = Field(column_name='Specification')
    qty = Field(column_name='QTY')
    uom = Field(column_name='Unit')
    pack_type = Field(column_name='Packaging Type')
    dispatch_status = Field(column_name='Dispatch Status')
    dispatch_date = Field(column_name='Dispatch Date')
    transport = Field(column_name='Transport')
    invoice_no = Field(column_name='Invoice No.')
    lr_no = Field(column_name='LR NO')
    order_status = Field(column_name='Order Status')
    delivered_date = Field(column_name='Delivered Date')

    # def dehydrate_order_no(self,OrderOfProduct):
    #     order = getattr(OrderOfProduct, "order", "unknown")
    #     return order.order_no

    def dehydrate_order_no(self,OrderOfProduct):
        order = getattr(OrderOfProduct, "order", "unknown")
        return order.order_no    
    
    def dehydrate_order_date(self,OrderOfProduct):
        order = getattr(OrderOfProduct, "order", "unknown")
        return order.date.strftime("%d/%m/%Y")
    
    def dehydrate_customer_name(self,OrderOfProduct):
        order = getattr(OrderOfProduct, "order", "unknown")
        return order.customer.name
    
    def dehydrate_product_code(self,OrderOfProduct):
        product = getattr(OrderOfProduct, "product", "unknown")
        return product.code
    
    def dehydrate_product_name(self,OrderOfProduct):
        product = getattr(OrderOfProduct, "product", "unknown")
        return product.name
    
    def dehydrate_product_specifaction(self,OrderOfProduct):
        product = getattr(OrderOfProduct, "product", "unknown")
        return product.specifaction
    
    def dehydrate_product_specifaction(self,OrderOfProduct):
        product = getattr(OrderOfProduct, "product", "unknown")
        return product.specification
    
    def dehydrate_qty(self,OrderOfProduct):
        qty = getattr(OrderOfProduct, "order_qty", "unknown")
        return qty
    
    def dehydrate_uom(self,OrderOfProduct):
        uom = getattr(OrderOfProduct, "uom", "unknown")
        return uom
    
    def dehydrate_pack_type(self,OrderOfProduct):
        type = getattr(OrderOfProduct, "packing_type", "unknown")
        return type

    # def dehydrate_pack_type(self,OrderOfProduct):
    #     type = getattr(OrderOfProduct, "packing_type", "unknown")
    #     return type

    def dehydrate_dispatch_status(self,OrderOfProduct):
        dispatch_status = getattr(OrderOfProduct, "dispatch_status", "unknown")
        return dispatch_status
    
    def dehydrate_dispatch_date(self,OrderOfProduct):
        dispatch_date = getattr(OrderOfProduct, "dispatch_date", "unknown")
        if dispatch_date:
            return dispatch_date.strftime("%d/%m/%Y")
        else:
            return '-'
    
    def dehydrate_transport(self,OrderOfProduct):
        transport_compny = getattr(OrderOfProduct, "transport_compny", "unknown")
        if transport_compny:
            return transport_compny
        else:
            return '-'
    
    def dehydrate_invoice_no(self,OrderOfProduct):
        invoice_no = getattr(OrderOfProduct, "invoice_no", "unknown")
        if invoice_no:
            return invoice_no
        else:
            return '-'
    
    def dehydrate_lr_no(self,OrderOfProduct):
        lr_no = getattr(OrderOfProduct, "lr_no", "unknown")
        if lr_no:
            return lr_no
        else:
            return '-'
    
    def dehydrate_order_status(self,OrderOfProduct):
        status = getattr(OrderOfProduct, "status", "unknown")
        return status
    
    def dehydrate_delivered_date(self,OrderOfProduct):
        delivered_date = getattr(OrderOfProduct, "delivered_date", "unknown")
        if delivered_date:
            return delivered_date.strftime("%d/%m/%Y")
        else:
            return '-'
    
    class Meta:
        model = OrderOfProduct  # sl.no, Customer Name, Order No, Date, Part No, Category, name, other specification, order Qty, UOM, Packing type, Order Status, sales challan, bill No, Lr No, dispatch date, transport details, deliverd date, remark
        fields = ('order_no', 'order_date', 'customer_name', 'product_code', 'product_name', 'product_specifaction', 'qty', 'uom', 'pack_type', 'dispatch_status', 'dispatch_date', 'transport', 'invoice_no', 'lr_no', 'order_status', 'delivered_date')
        export_order = ('order_no', 'order_date', 'customer_name', 'product_code', 'product_name', 'product_specifaction', 'qty', 'uom', 'pack_type', 'dispatch_status', 'dispatch_date', 'transport', 'invoice_no', 'lr_no', 'order_status', 'delivered_date')
        
