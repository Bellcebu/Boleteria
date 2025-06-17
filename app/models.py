from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings


class BaseModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def validate_required_fields(cls, **fields):
        errors = {}
        for field_name, value in fields.items():
            if not value:
                errors[field_name] = f"El campo {field_name} es obligatorio"
        return errors


# --- Categorías y lugares ---
class Category(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @classmethod
    def validate(cls, name):
        return cls.validate_required_fields(name=name)

    @classmethod
    def new(cls, name, description='', is_active=True):
        errors = cls.validate(name)
        if errors:
            return False, errors
        category = cls.objects.create(name=name, description=description, is_active=is_active)
        return True, category

    def update(self, name=None, description=None, is_active=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if is_active is not None:
            self.is_active = is_active
        self.save()


class Venue(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    capacity = models.IntegerField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"

    @classmethod
    def validate(cls, name, address, city, capacity, contact):
        errors = cls.validate_required_fields(name=name, address=address, city=city, contact=contact)
        if capacity is None or capacity <= 0:
            errors["capacity"] = "La capacidad debe ser un número positivo"
        return errors

    @classmethod
    def new(cls, name, address, city, capacity, contact):
        errors = cls.validate(name, address, city, capacity, contact)
        if errors:
            return False, errors
        venue = cls.objects.create(
            name=name,
            address=address,
            city=city,
            capacity=capacity,
            contact=contact
        )
        return True, venue

    def update(self, name=None, address=None, city=None, capacity=None, contact=None):
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        if city is not None:
            self.city = city
        if capacity is not None:
            self.capacity = capacity
        if contact is not None:
            self.contact = contact
        self.save()


# --- Eventos, Comentarios, Ratings ---
class Event(BaseModel):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='events'
    )
    venue_fk = models.ForeignKey(
        "Venue",
        on_delete=models.CASCADE,
        default=None
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_base_price(self):
        tier = self.ticket_tiers.filter(is_available=True).order_by('price').first()
        return tier.price if tier else 0

    @classmethod
    def validate(cls, title, description, date):
        errors = cls.validate_required_fields(title=title, description=description)
        if not date:
            errors["date"] = "La fecha es obligatoria"
        elif date and date < models.DateTimeField().to_python('now'):
            pass
        return errors

    @classmethod
    def new(cls, title, description, date, category, venue):
        errors = cls.validate(title, description, date)
        if errors:
            return False, errors
        event = cls.objects.create(
            title=title,
            description=description,
            date=date,
            category=category,
            venue_fk=venue
        )
        return True, event

    def update(self, title=None, description=None, date=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if date is not None:
            self.date = date
        self.save()


class Promotion(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2) 
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='promotions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_uses = models.IntegerField(null=True, blank=True)  
    current_uses = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}% para {self.event.title}"


class Comment(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user_fk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    event_fk = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        default=None
    )

    @classmethod
    def validate(cls, title, text):
        return cls.validate_required_fields(title=title, text=text)

    @classmethod
    def new(cls, title, text, user, event):
        errors = cls.validate(title, text)
        if errors:
            return False, errors
        return cls.objects.create(
            title=title,
            text=text,
            user_fk=user,
            event_fk=event
        )

    def update(self, title=None, text=None):
        if title is not None:
            self.title = title
        if text is not None:
            self.text = text
        self.save()


class Rating(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_fk = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None
    )
    event_fk = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        default=None
    )

    @classmethod
    def validate(cls, title, text, rating):
        errors = cls.validate_required_fields(title=title, text=text)
        if rating is None or not (1 <= rating <= 5):
            errors["rating"] = "La calificación debe estar entre 1 y 5"
        return errors

    @classmethod
    def new(cls, title, text, rating, user, event):
        errors = cls.validate(title, text, rating)
        if errors:
            return False, errors
        return cls.objects.create(
            title=title,
            text=text,
            rating=rating,
            user_fk=user,
            event_fk=event
        )

    def update(self, title=None, text=None, rating=None):
        if title is not None:
            self.title = title
        if text is not None:
            self.text = text
        if rating is not None:
            self.rating = rating
        self.save()


# --- Tickets ---
class TicketTier(models.Model):    
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='ticket_tiers')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)  
    max_quantity = models.IntegerField(null=True, blank=True) 
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['event', 'name'] 
    
    def __str__(self):
        return f"{self.event.title} - {self.name} (${self.price})"


class Ticket(models.Model):
    ticket_tier = models.ForeignKey(TicketTier, on_delete=models.CASCADE)
    promotion_used = models.ForeignKey('Promotion', on_delete=models.SET_NULL, null=True, blank=True)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    final_price = models.DecimalField(max_digits=8, decimal_places=2)  
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def calculate_final_price(self):
        price = self.ticket_tier.price * self.quantity
        if self.promotion_used:
            discount = price * (self.promotion_used.discount_percentage / 100)
            price -= discount
        return price
    
    def __str__(self):
        return f"Ticket {self.id} - {self.ticket_tier.event.title}"


# --- Notificaciones ---
class Notificacion(BaseModel):
    title = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    priority = models.CharField(
        max_length=10,
        choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')],
        default='media'
    )
    is_read = models.BooleanField(default=False)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='notificaciones'
    )

    @classmethod
    def validate(cls, title, message, priority):
        errors = cls.validate_required_fields(title=title, message=message)
        if priority not in ['alta', 'media', 'baja']:
            errors["priority"] = "Prioridad inválida"
        return errors

    @classmethod
    def new(cls, title, message, priority='media', users=None):
        errors = cls.validate(title, message, priority)
        if errors:
            return False, errors
        notificacion = cls.objects.create(title=title, message=message, priority=priority)
        if users:
            notificacion.users.set(users)
        return True, notificacion

    def update(self, title=None, message=None, priority=None, is_read=None, users=None):
        if title is not None:
            self.title = title
        if message is not None:
            self.message = message
        if priority is not None:
            self.priority = priority
        if is_read is not None:
            self.is_read = is_read
        self.save()
        if users is not None:
            self.users.set(users)


# --- Solicitudes de Reembolso ---
class RefundRequest(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refund_requests'
    )
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    ticket_code = models.CharField(max_length=50)
    reason = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    @classmethod
    def validate(cls, ticket_code, reason):
        return cls.validate_required_fields(ticket_code=ticket_code, reason=reason)

    @classmethod
    def new(cls, user, ticket_code, reason):
        errors = cls.validate(ticket_code, reason)
        if errors:
            return False, errors
        refund_request = cls.objects.create(
            user=user,
            ticket_code=ticket_code,
            reason=reason,
        )
        return True, refund_request

    def update(self, ticket_code=None, reason=None, approved=None):
        if ticket_code is not None:
            self.ticket_code = ticket_code
        if reason is not None:
            self.reason = reason
        if approved is not None:
            self.approved = approved
        self.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

