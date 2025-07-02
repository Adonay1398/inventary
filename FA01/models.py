# type: ignore
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

class Location(models.Model):
    LOCATION_TYPES = [
        ('warehouse', 'Almacén'),
        ('office', 'Oficina'),
        ('drugstore', 'Farmacia')
    ]
    
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

class Asset(models.Model):
    CATEGORIES = [
        ('pc', 'PC'),
        ('laptop', 'Laptop'),
        ('monitor', 'Monitor'),
        ('nobreak','Nobreak'),
        ('printer', 'Impresora'),
        ('network', 'Equipo de Red'),
        ('peripheral', 'Periférico'),
        ('server', 'Servidor'),
        ('other', 'Otro')
    ]

    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('in_use', 'En Uso'),
        ('maintenance', 'En Mantenimiento'),
        ('repair', 'En Reparación'),
        ('retired', 'Retirado'),
        ('lost', 'Perdido'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100, verbose_name='Marca', blank=True)
    model = models.CharField(max_length=100, verbose_name='Modelo', blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    warranty_expiration = models.DateField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, help_text="Cantidad de unidades similares")
    preferred_usage_period = models.PositiveIntegerField(
        default=36,
        help_text="Período de uso preferente en meses"
    )
    specifications = models.TextField(help_text="Características técnicas del equipo", blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name='Categoría')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to_name = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre del responsable (puede no ser usuario del sistema)")
    notes = models.TextField(help_text="Observaciones adicionales", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

    def get_age(self):
        """Calculate the age of the asset in years"""
        today = timezone.now().date()
        if not self.purchase_date:
            return 0
        age = today.year - self.purchase_date.year
        # Adjust age if birthday hasn't occurred yet this year
        if (today.month, today.day) < (self.purchase_date.month, self.purchase_date.day):
            age -= 1
        return max(0, age)  # Ensure we don't return negative ages

    def is_nearing_end_of_life(self):
        """Check if the asset is nearing its preferred usage period"""
        if not self.purchase_date:
            return False
        
        today = timezone.now().date()
        months_since_purchase = (today.year - self.purchase_date.year) * 12 + today.month - self.purchase_date.month
        
        # Consider an asset as nearing end of life if it's within 3 months of its preferred usage period
        return months_since_purchase >= (self.preferred_usage_period - 3)

    def send_end_of_life_notification(self):
        """Send email notification about asset nearing end of life"""
        if not self.is_nearing_end_of_life():
            return

        subject = f'Alerta: {self.name} está próximo a alcanzar su período de uso preferente'
        message = f"""
        El siguiente activo está próximo a alcanzar su período de uso preferente:

        Nombre: {self.name}
        Número de Serie: {self.serial_number}
        Fecha de Compra: {self.purchase_date}
        Período de Uso Preferente: {self.preferred_usage_period} meses
        Ubicación: {self.location.name if self.location else 'No asignada'}
        Responsable: {self.assigned_to.username if self.assigned_to else 'No asignado'}

        Por favor, considere realizar una evaluación del equipo para determinar si necesita ser reemplazado.
        """
        
        # Send to all staff users
        staff_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
        if staff_emails:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                staff_emails,
                fail_silently=True,
            )

    class Meta:
        verbose_name = 'Activo'
        verbose_name_plural = 'Activos'

class Movement(models.Model):
    MOVEMENT_TYPES = [
        ('location', 'Cambio de Ubicación'),
        ('assignment', 'Cambio de Responsable'),
        ('maintenance', 'Envío a Mantenimiento'),
        ('return', 'Retorno de Mantenimiento'),
        ('retirement', 'Dado de Baja')
    ]

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    from_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='movements_from')
    to_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='movements_to')
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movements_from')
    assigned_to_name = models.CharField(max_length=100, blank=True, null=True)
    movement_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    movement = models.CharField(max_length=20,choices=MOVEMENT_TYPES,verbose_name='Movimiento')
    
    def __str__(self):
        return f"Movement of {self.asset.name} on {self.movement_date}"

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    extension = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=50, unique=True)
    responsable = models.CharField(max_length=100)
    token = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

class DispositivoSucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='dispositivos')
    fecha_envio = models.DateTimeField()
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=50)
    hostname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.hostname} ({self.ip}) - {self.sucursal.codigo}"

    class Meta:
        verbose_name = 'Dispositivo de Sucursal'
        verbose_name_plural = 'Dispositivos de Sucursal'

class AssetImage(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='assets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.asset.name} ({self.id})"

class Responsibility(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='letter_responsibilities')
    letter_responsibility = models.ImageField(upload_to='letter_responsibility/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Responsiva de {self.asset.name} ({self.id})"

    class Meta:
        verbose_name = 'Responsiva'
        verbose_name_plural = 'Responsivas'