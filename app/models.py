from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


# --- Categorías y lugares ---
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    @classmethod
    def validate(cls, name):
        errors = {}
        if not name:
            errors["name"] = "El nombre es obligatorio"
        return errors

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


class Venue(models.Model):
    name = models.TextField(max_length=100)
    address = models.TextField(max_length=100)
    city = models.TextField(max_length=100)
    capacity = models.IntegerField()
    contact = models.TextField(max_length=100)

    @classmethod
    def new(cls, name, address, city, capacity, contact):
        if not name or not address or not city or not contact:
            raise ValidationError("All fields except capacity are required.")
        if capacity <= 0:
            raise ValidationError("Capacity must be a positive number.")
        return cls.objects.create(
            name=name,
            address=address,
            city=city,
            capacity=capacity,
            contact=contact
        )

    def update(self, name=None, address=None, city=None, capacity=None, contact=None):
        self.name = name or self.name
        self.address = address or self.address
        self.city = city or self.city
        self.capacity = capacity or self.capacity
        self.contact = contact or self.contact
        self.save()


# --- Eventos, Comentarios, Ratings ---
class Event(models.Model):
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
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def validate(cls, title, description, date):
        errors = {}
        if not title:
            errors["title"] = "Por favor ingrese un título"
        if not description:
            errors["description"] = "Por favor ingrese una descripción"
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
        self.title = title or self.title
        self.description = description or self.description
        self.date = date or self.date
        self.save()


class Comment(models.Model):
    title = models.TextField(max_length=100)
    text = models.TextField(max_length=100)
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
    def new(cls, title, text, user, event):
        if not title or not text:
            raise ValidationError("Title and text are required.")
        return cls.objects.create(
            title=title,
            text=text,
            user_fk=user,
            event_fk=event
        )

    def update(self, title=None, text=None):
        self.title = title or self.title
        self.text = text or self.text
        self.save()


class Rating(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=250)
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
    def new(cls, title, text, rating, user, event):
        if not title or not text:
            raise ValidationError("Title and text are required.")
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")
        return cls.objects.create(
            title=title,
            text=text,
            rating=rating,
            user_fk=user,
            event_fk=event
        )

    def update(self, title=None, text=None, rating=None):
        self.title = title or self.title
        self.text = text or self.text
        self.rating = rating or self.rating
        self.save()


# --- Tickets ---
class Ticket(models.Model):
    class TicketType(models.TextChoices):
        GENERAL = 'GENERAL', 'General'
        VIP = 'VIP', 'VIP'

    ticket_code = models.TextField(max_length=100, primary_key=True)
    buy_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    type = models.CharField(
        max_length=10,
        choices=TicketType.choices,
        default=TicketType.GENERAL,
    )
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
    def new(cls, ticket_code, quantity, ticket_type, user, event):
        if not ticket_code:
            raise ValidationError("Ticket code is required.")
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        if ticket_type not in cls.TicketType.values:
            raise ValidationError(f"Type must be one of: {cls.TicketType.values}")
        return cls.objects.create(
            ticket_code=ticket_code,
            quantity=quantity,
            type=ticket_type,
            user_fk=user,
            event_fk=event
        )

    def update(self, ticket_code=None, quantity=None, ticket_type=None):
        self.ticket_code = ticket_code or self.ticket_code
        self.quantity = quantity or self.quantity
        self.type = ticket_type or self.type
        self.save()


# --- Notificaciones ---
class Notificacion(models.Model):
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
        errors = {}
        if not title:
            errors["title"] = "El título es obligatorio"
        if not message:
            errors["message"] = "El mensaje es obligatorio"
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
class RefundRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refund_requests'
    )
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(default=None)
    ticket_code = models.CharField(max_length=50)
    reason = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    @classmethod
    def validate(cls, ticket_code, reason):
        errors = {}
        if not ticket_code:
            errors["ticket_code"] = "El código del ticket es obligatorio"
        if not reason:
            errors["reason"] = "La razón es obligatoria"
        return errors

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
