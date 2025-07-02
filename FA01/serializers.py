from rest_framework import serializers
from .models import Sucursal, DispositivoSucursal

class DispositivoSucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispositivoSucursal
        fields = ['id', 'fecha_envio', 'ip', 'mac', 'hostname']

class SucursalSerializer(serializers.ModelSerializer):
    dispositivos = DispositivoSucursalSerializer(many=True, read_only=True)

    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'codigo', 'responsable', 'dispositivos'] 