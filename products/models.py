from django.db import models
from django.urls import reverse
from math import ceil

class Category(models.Model):
    name = models.CharField('Nombre', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField('Nombre', max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Categoría')
    code = models.CharField('Código', max_length=50, unique=True)
    description = models.TextField('Descripción', blank=True)
    purchase_price = models.IntegerField('Precio de Compra')
    is_purchase_with_tax = models.BooleanField('Precio de compra incluye IVA', default=False)
    net_purchase_price = models.IntegerField('Precio de Compra Neto')
    profit_percentage = models.IntegerField('Porcentaje de Ganancia')
    suggested_price = models.IntegerField('Precio Sugerido sin IVA', default=0)  # Añadimos default=0
    sale_price = models.IntegerField('Precio de Venta Final')
    stock = models.IntegerField('Stock', default=0)
    image = models.ImageField('Imagen', upload_to='products', blank=True, null=True)
    is_active = models.BooleanField('Activo', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Calcular precio neto de compra
        if self.is_purchase_with_tax:
            self.net_purchase_price = ceil(self.purchase_price / 1.19)
        else:
            self.net_purchase_price = self.purchase_price

        # Si no hay precio de venta pero hay porcentaje de ganancia, calcular precio sugerido y de venta
        if not self.sale_price and self.profit_percentage:
            self.suggested_price = ceil(self.net_purchase_price * (1 + (self.profit_percentage / 100)))
            self.sale_price = ceil(self.suggested_price * 1.19)
        # Si hay precio de venta pero no porcentaje de ganancia, calcular porcentaje y precio sugerido
        elif self.sale_price and not self.profit_percentage:
            net_sale_price = ceil(self.sale_price / 1.19)
            self.suggested_price = net_sale_price
            self.profit_percentage = ceil(((net_sale_price - self.net_purchase_price) / self.net_purchase_price) * 100)
        # Si no hay ninguno, establecer valores por defecto
        else:
            self.suggested_price = self.net_purchase_price
            self.sale_price = ceil(self.suggested_price * 1.19)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})