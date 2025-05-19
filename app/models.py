from django.db import models
from django.core.exceptions import ValidationError

class Rating(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=100)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user_fk = models.ForeignKey('User', on_delete=models.CASCADE)

    @classmethod
    def new(cls, title, text, rating, user):
        if not title or not text:
            raise ValidationError("Title and text are required.")
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5.")

        return cls.objects.create(
            title=title,
            text=text,
            rating=rating,
            user_fk=user
        )

    def update(self, title, text, rating):
        self.title = title or self.title
        self.text = text or self.text
        self.rating = rating or self.rating
        self.save()


class Ticket(models.Model):
    class TicketType(models.TextChoices):
        GENERAL = 'GENERAL', 'General'
        VIP = 'VIP', 'VIP'

    buy_date = models.DateField(auto_now_add=True)
    ticket_code = models.TextField(max_length=100)
    quantity = models.IntegerField()
    type = models.CharField(
        max_length=10,
        choices=TicketType.choices,
        default=TicketType.GENERAL,
    )
    user_fk = models.ForeignKey('User', on_delete=models.CASCADE)

    @classmethod
    def new(cls, ticket_code, quantity, type, user):
        if not ticket_code:
            raise ValidationError("Ticket code is required.")
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than 0.")
        if type not in cls.TicketType.values:
            raise ValidationError(f"Type must be one of: {cls.TicketType.values}")

        return cls.objects.create(
            ticket_code=ticket_code,
            quantity=quantity,
            type=type,
            user_fk=user
        )

    def update(self, ticket_code, quantity, type):
        self.ticket_code = ticket_code or self.ticket_code
        self.quantity = quantity or self.quantity
        self.type = type or self.type
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

    def update(self, name, address, city, capacity, contact):
        self.name = name or self.name
        self.address = address or self.address
        self.city = city or self.city
        self.capacity = capacity or self.capacity
        self.contact = contact or self.contact
        self.save()


class Comment(models.Model):
    title = models.TextField(max_length=100)
    text = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    user_fk = models.ForeignKey('User', on_delete=models.CASCADE)

    @classmethod
    def new(cls, title, text, user):
        if not title or not text:
            raise ValidationError("Title and text are required.")

        return cls.objects.create(
            title=title,
            text=text,
            user_fk=user
        )

    def update(self, title, text):
        self.title = title or self.title
        self.text = text or self.text
        self.save()

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def validate(cls, title, description, date):
        errors = {}

        if title == "":
            errors["title"] = "Por favor ingrese un titulo"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion"

        return errors

    @classmethod
    def new(cls, title, description, date):
        errors = Event.validate(title, description, date)

        if len(errors.keys()) > 0:
            return False, errors

        Event.objects.create(
            title=title,
            description=description,
            date=date,
        )

        return True, None

    def update(self, title, description, date):
        self.title = title or self.title
        self.description = description or self.description
        self.date = date or self.date

        self.save()
