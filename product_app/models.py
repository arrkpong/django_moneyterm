# product_app/models.py
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

class CardType(models.Model):
    card_name = models.CharField(max_length=255, unique=True, verbose_name="Card Name")
    description = models.TextField(blank=True, null=True, verbose_name="Product Description")
    image = models.ImageField(upload_to="card_images", blank=True, verbose_name="Card Image")
    is_popular = models.BooleanField(default=False, verbose_name="Popular Product")

    def __str__(self):
        return self.card_name

    class Meta:
        verbose_name = "Card Type"
        verbose_name_plural = "Card Types"

class CardPrice(models.Model):
    card_price = models.ForeignKey(CardType, on_delete=models.CASCADE, verbose_name="Card Type", related_name='card_prices')
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Card Price", default=0.0)
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantity of Cards")

    def __str__(self):
        return f"{self.card_price.card_name} - {self.price}"

    class Meta:
        verbose_name = "Card Price"
        verbose_name_plural = "Card Prices"

class CardDetail(models.Model):
    card_detail = models.ForeignKey(CardPrice, on_delete=models.CASCADE, verbose_name="Card Price", related_name='card_details') 
    serial_number = models.CharField(max_length=16, unique=True, verbose_name="Serial Number", validators=[RegexValidator(regex='^[0-9]{16}$', message='Serial number must be 16 digits and numeric only')])
    pin = models.CharField(max_length=4, verbose_name="Card PIN", validators=[RegexValidator(regex='^[0-9]{4}$', message='PIN must be 4 digits and numeric only')])
    is_active = models.BooleanField(default=True, verbose_name="Active")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    def __str__(self):
        return f"{self.card_detail.card_price} - {self.serial_number}"

    class Meta:
        verbose_name = "Card Detail"
        verbose_name_plural = "Card Details"

class Advertisement(models.Model):
    image = models.ImageField(upload_to="advertisement_images", verbose_name="Advertisement Image")
    description = models.TextField(verbose_name="Advertisement Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"

class Promotion(models.Model):
    card_price = models.ForeignKey(CardPrice, on_delete=models.CASCADE, related_name='promotions', verbose_name="Card Price")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Discount Percentage")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    def __str__(self):
        return f"{self.card_price} - {self.discount_percentage}%"

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

@receiver(pre_save, sender=CardType)
def delete_old_card_type_image(sender, instance, **kwargs):
    if instance.pk:
        old_instance = CardType.objects.get(pk=instance.pk)
        if old_instance.image != instance.image:
            if old_instance.image:
                old_instance.image.delete(save=False)

@receiver(post_save, sender=CardDetail)
@receiver(post_delete, sender=CardDetail)
def update_card_quantity(sender, instance, **kwargs):
    card_price = instance.card_detail
    card_price.quantity = card_price.card_details.count()
    card_price.save()

    # Alternative method:
    # card_price.quantity = CardDetail.objects.filter(card_detail=card_price).count()
    # card_price.save()
