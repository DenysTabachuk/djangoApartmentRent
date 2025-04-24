from django import forms
from .models import Apartment

class ApartmentForm(forms.ModelForm):
    city = forms.ChoiceField(
        choices=Apartment.CITY_CHOICES,  
        label='Місто',  
        widget=forms.Select(attrs={'class': 'form-control'})  
    )
    
    street = forms.CharField(
        max_length=255, 
        label='Вулиця',  
        widget=forms.TextInput(attrs={'class': 'form-control'})  
    )

    house_number = forms.CharField(
        max_length=50, 
        label='Номер будинку',  
        widget=forms.TextInput(attrs={'class': 'form-control'})  
    )


    class Meta:
        model = Apartment  
        fields = ['title', 'description', 'price', 'city', 'street', 'house_number']  
        labels = { 
            'title': 'Назва оголошення',
            'description': 'Опис',
            'price': 'Ціна',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  
            'price': forms.NumberInput(attrs={'class': 'form-control'}),  
        }


    def clean(self):
        cleaned_data = super().clean()  
        city = cleaned_data.get('city') 
        street = cleaned_data.get('street') 
        house_number = cleaned_data.get('house_number') 


        if city and street and house_number:
            cleaned_data['location'] = {
                'city': city,
                'street': street,
                'house_number': house_number,
            }
        else:
            raise forms.ValidationError("Будь ласка, заповніть усі поля адреси.")
        
        return cleaned_data  

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 5:
            raise forms.ValidationError("Назва оголошення повинна містити щонайменше 5 символів.")
        return title
    
    def clean_description(self):
        title = self.cleaned_data.get('description')
        if len(title.strip()) < 10:
            raise forms.ValidationError("Опис має містити не менше 10 символів.")
        return title

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Ціна повинна бути більшою за 0.")
        return price

    def save(self, commit=True):
        instance = super().save(commit=False)  # Створюємо екземпляр моделі, але ще не зберігаємо в БД
        instance.location = self.cleaned_data['location']  # Зберігаємо локацію (JSON) в моделі
        if commit:
            instance.save()  # Якщо commit = True — зберігаємо екземпляр у БД
        return instance  # Повертаємо збережений екземпляр



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Якщо є instance і в нього є локація — заповнюємо поля вручну
        if self.instance and self.instance.location:
            self.fields['city'].initial = self.instance.location.get('city', '')
            self.fields['street'].initial = self.instance.location.get('street', '')
            self.fields['house_number'].initial = self.instance.location.get('house_number', '')