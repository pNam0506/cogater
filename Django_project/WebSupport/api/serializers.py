# po_dsd_receive/api/serializers.py

from WebSupport.models import Product
from rest_framework import serializers
from datetime import datetime,date

class Receive_ItemsSerializer(serializers.ModelSerializer):
    po_no = serializers.SerializerMethodField()
    po_date = serializers.SerializerMethodField()
    store_code = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    
    class Meta:
        model = Receive_items
        fields = ['po_no','po_date','store_code','supplier','barcode', 'prodname','dlv_qty','lotno','exp']

    def get_po_no(self, obj):
        return obj.hd.po_no  # Access related field
    
    def get_po_date(self, obj):
        return obj.hd.po_date
    
    def get_store_code(self, obj):
        return obj.hd.store_code
    
    def get_supplier(self, obj):
        return obj.hd.supplier
    
class ReceiveSerializer(serializers.ModelSerializer):
    dt_set = Receive_ItemsSerializer(many=True)
    
    class Meta:
        model = Receive
        fields = ['po_no', 'po_date','store_code','supplier','dt_set']


    def create(self, validated_data):
        dt_data = validated_data.pop('dt_set')
        hd = Receive.objects.create(**validated_data)
        for dt in dt_data:
            print(dt)
            Receive_items.objects.create(hd=hd, **dt)
        return hd

    
class ShipmentSerializer(serializers.ModelSerializer):
    po_no = serializers.CharField(source='PONO')
    po_date = serializers.CharField(source='PODate')
    dlv_qty = serializers.CharField(source='DlvQty')
    barcode = serializers.CharField(source='BarCode')
    lotno = serializers.CharField(source='FTPdtLotNo')
    exp = serializers.CharField(source='FTPdtExpire')

    class Meta:
        model = Shipment
        fields = '__all__'

