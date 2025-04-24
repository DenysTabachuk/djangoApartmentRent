from django.db import models
from django.conf import settings

class Apartment(models.Model):
    CITY_CHOICES = [
        ('Kyiv', 'Київ'),
        ('Lviv', 'Львів'),
        ('Odessa', 'Одеса'),
        ('Kharkiv', 'Харків'),
        ('Dnipro', 'Дніпро'),
        ('Zaporizhzhia', 'Запоріжжя'),
        ('Kryvyi Rih', 'Кривий Ріг'),
        ('Mykolaiv', 'Миколаїв'),
        ('Cherkasy', 'Черкаси')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    location = models.JSONField() 
    status = models.CharField(
        max_length=20,
        choices=[   
                 ('approved', 'Підтверджено'),
                 ('pending', 'Очікує'),
                 ('rejected', 'Відмовлено')
                ],
        default='pending'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартири"