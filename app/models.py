from decimal import Decimal, ROUND_DOWN, InvalidOperation
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.db import models
from django.db.models import Sum
from django.utils import timezone


# --- Base ---
class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# --- Categorías y Lugares ---
class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def clean(self):
        if self.name and len(self.name.strip()) < 3:
            raise ValidationError({'name': 'El nombre debe tener al menos 3 caracteres.'})
        
        if self.description and len(self.description.strip()) < 10:
            raise ValidationError({'description': 'La descripción debe tener al menos 10 caracteres.'})

    @property
    def active_events_count(self):
        return self.events.filter(date__gte=timezone.now()).count()


class Venue(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.city}"

    def clean(self):
        if self.capacity and self.capacity <= 0:
            raise ValidationError({'capacity': 'La capacidad debe ser un número positivo.'})
        
        if self.city and self.city.isnumeric():
            raise ValidationError({'city': 'La ciudad no puede ser un número.'})

    @property
    def upcoming_events_count(self):
        return self.events.filter(date__gte=timezone.now()).count()


# --- Eventos ---
class Event(BaseModel):
    category = models.ManyToManyField('Category', related_name='events')
    venue_fk = models.ForeignKey("Venue", on_delete=models.CASCADE, related_name='events')
    autor = models.CharField(max_length=100, blank=True, null=True) 
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.date and self.date <= timezone.now():
            raise ValidationError({'date': 'La fecha del evento debe ser en el futuro.'})

    @property
    def is_past(self):
        return self.date <= timezone.now()

    @property
    def total_capacity(self):
        return self.ticket_tiers.aggregate(
            total=Sum('max_quantity')
        )['total'] or 0

    @property
    def available_capacity(self):
        sold = self.get_sold_tickets_count()
        return max(0, self.total_capacity - sold)

    def get_sold_tickets_count(self):
        return Ticket.objects.filter(
            ticket_tier__event=self
        ).aggregate(total=Sum('quantity'))['total'] or 0

    def get_base_price(self):
        tier = self.ticket_tiers.filter(is_available=True).order_by('price').first()
        return tier.price if tier else Decimal('0.00')

    def get_average_rating(self):
        from django.db.models import Avg
        avg = self.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating']
        return round(avg, 1) if avg else None

    def can_user_rate(self, user):
        if not user.is_authenticated:
            return False
        has_tickets = Ticket.objects.filter(
            ticket_tier__event=self,
            user_fk=user
        ).exists()
        has_already_rated = self.ratings.filter(user_fk=user).exists()
        return has_tickets and self.is_past and not has_already_rated


# --- Promociones ---
class Promotion(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='promotions')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}% para {self.event.title}"

    def clean(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError('La fecha de inicio debe ser anterior a la fecha de fin.')
        
        if self.discount_percentage and not (0 < self.discount_percentage <= 100):
            raise ValidationError({'discount_percentage': 'El descuento debe estar entre 0.01 y 100.'})

    @property
    def is_valid_now(self):
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )

    def can_be_used(self):
        return self.is_valid_now

    def use_promotion(self):
        if self.can_be_used():
            self.current_uses += 1
            self.save(update_fields=['current_uses'])
            return True
        return False


# --- Comentarios ---
class Comment(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_fk = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comentario de {self.user_fk.username} en {self.event_fk.title}"

# --- Ratings ---
class Rating(BaseModel):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_fk = models.ForeignKey("Event", on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        unique_together = ['user_fk', 'event_fk']
        ordering = ['-created_at']

    def __str__(self):
        return f"Rating {self.rating}/5 de {self.user_fk.username} para {self.event_fk.title}"

    def clean(self):
        if self.rating and not (1 <= self.rating <= 5):
            raise ValidationError({'rating': 'La calificación debe estar entre 1 y 5.'})

        if self.user_fk and self.event_fk:
            has_tickets = Ticket.objects.filter(
                ticket_tier__event=self.event_fk,
                user_fk=self.user_fk
            ).exists()
            if not has_tickets:
                raise ValidationError('Solo puedes calificar eventos para los que compraste entradas.')


# --- Entradas (Tickets) ---
class TicketTier(BaseModel):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='ticket_tiers')
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    max_quantity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['event', 'name']
        ordering = ['price']

    def __str__(self):
        return f"{self.event.title} - {self.name} (${self.price})"

    def clean(self):
        if self.event and self.max_quantity:
            total_capacity = self.event.venue_fk.capacity
            other_tiers_qty = self.event.ticket_tiers.exclude(pk=self.pk).aggregate(
                total=Sum('max_quantity')
            )['total'] or 0
            
            if (other_tiers_qty + self.max_quantity) > total_capacity:
                raise ValidationError({
                    'max_quantity': f'La capacidad total excede la del venue ({total_capacity})'
                })

    @property
    def sold_quantity(self):
        return self.ticket_set.aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def available_quantity(self):
        return max(0, self.max_quantity - self.sold_quantity)

    @property
    def is_sold_out(self):
        return self.available_quantity <= 0

    def has_available_quantity(self, requested_qty):
        return self.available_quantity >= requested_qty

    def get_available_quantity(self):
        if not self.max_quantity:
            return 0
        sold_qty = self.ticket_set.aggregate(total=Sum('quantity'))['total'] or 0
        return max(0, self.max_quantity - sold_qty)


class Ticket(BaseModel):
    ticket_tier = models.ForeignKey(TicketTier, on_delete=models.CASCADE)
    promotion_used = models.ForeignKey('Promotion', on_delete=models.SET_NULL, null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    user_fk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Ticket {self.pk} - {self.ticket_tier.event.title}"

    def clean(self):
        if self.quantity < 1:
            raise ValidationError({'quantity': 'La cantidad debe ser al menos 1.'})
        
        if self.ticket_tier and not self.ticket_tier.has_available_quantity(self.quantity):
            raise ValidationError({
                'quantity': f'Solo quedan {self.ticket_tier.available_quantity} entradas disponibles.'
            })

    def save(self, *args, **kwargs):
        if self.ticket_tier:
            self.original_price = (
                Decimal(str(self.ticket_tier.price)) * self.quantity
            ).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
            
            if self.promotion_used and self.promotion_used.is_valid_now:
                discount = self.original_price * (
                    Decimal(str(self.promotion_used.discount_percentage)) / 100
                )
                self.final_price = (self.original_price - discount).quantize(
                    Decimal('0.01'), rounding=ROUND_DOWN
                )
                if not self.pk:
                    self.promotion_used.use_promotion()
            else:
                self.final_price = self.original_price
                
        super().save(*args, **kwargs)

    @cached_property
    def has_pending_refund(self):
        return RefundRequest.objects.filter(
            ticket_code=str(self.pk), 
            approved=False
        ).exists()

    @property
    def can_request_refund(self):
        return (
            not self.has_pending_refund and
            not self.ticket_tier.event.is_past
        )

    def calculate_final_price(self):
        try:
            base_price = Decimal(str(self.ticket_tier.price))
            quantity = Decimal(str(self.quantity))
            total_price = base_price * quantity
            if self.promotion_used:
                discount = total_price * (Decimal(str(self.promotion_used.discount_percentage)) / 100)
                final_price = total_price - discount
            else:
                final_price = total_price
            return final_price.quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        except (InvalidOperation, ValueError, TypeError) as e:
            print(f"Error calculando precio: {e}")
            return Decimal('0.00')


# --- Notificaciones ---
class Notification(BaseModel):
    title = models.CharField(max_length=50)
    message = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=[('alta', 'Alta'), ('media', 'Media'), ('baja', 'Baja')],
        default='media'
    )
    is_read = models.BooleanField(default=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='notificaciones')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @classmethod
    def send_to_all_users(cls, title, message, priority='media'):
        notification = cls.objects.create(
            title=title,
            message=message,
            priority=priority
        )
        notification.users.set(User.objects.all())
        return notification


# --- Solicitudes de Reembolso ---
class RefundRequest(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='refund_requests')
    ticket_code = models.CharField(max_length=50, unique=True)
    reason = models.TextField()
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True, blank=True)
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='processed_refunds'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reembolso de {self.user.username} - Ticket {self.ticket_code}"

    def clean(self):
        try:
            ticket = Ticket.objects.get(pk=self.ticket_code, user_fk=self.user)
            if ticket.ticket_tier.event.is_past:
                raise ValidationError('No se pueden solicitar reembolsos para eventos que ya han pasado.')
        except Ticket.DoesNotExist:
            raise ValidationError('El ticket especificado no existe o no te pertenece.')

    def approve(self, processed_by=None):
        self.approved = True
        self.approval_date = timezone.now().date()
        if processed_by:
            self.processed_by = processed_by
        self.save()

    @property
    def ticket(self):
        try:
            return Ticket.objects.get(pk=self.ticket_code)
        except Ticket.DoesNotExist:
            return None


# --- Perfil de Usuario ---
class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def add_points(self, amount):
        self.points += amount
        self.save(update_fields=['points'])

    @property
    def total_spent(self):
        return self.user.tickets.aggregate(
            total=Sum('final_price')
        )['total'] or Decimal('0.00')
    
class Favorito(models.Model):
    user_fk=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    event_fk=models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_fk', 'event_fk'], name='unique_favorite')
        ]
