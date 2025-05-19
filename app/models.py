from django.db import models

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


class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    @classmethod
    def validate(cls, username, email):
        errors = {}
        if not username:
            errors["username"] = "El nombre de usuario es obligatorio"
        if not email:
            errors["email"] = "El email es obligatorio"
        return errors

    @classmethod
    def new(cls, username, email):
        errors = cls.validate(username, email)
        if errors:
            return False, errors
        user = cls.objects.create(username=username, email=email)
        return True, user

    def update(self, username=None, email=None):
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        self.save()

class RefundRequest(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='refund_requests')
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(auto_now_add=True)
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
    def new(cls, user, ticket_code, reason, approved=False):
        errors = cls.validate(ticket_code, reason)
        if errors:
            return False, errors
        refund_request = cls.objects.create(
            user=user,
            ticket_code=ticket_code,
            reason=reason,
            approved=approved
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
    users = models.ManyToManyField('User', related_name='notificaciones')

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


class Event(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def validate(cls, title, description, date):
        errors = {}
        if not title:
            errors["title"] = "Por favor ingrese un titulo"
        if not description:
            errors["description"] = "Por favor ingrese una descripcion"
        return errors

    @classmethod
    def new(cls, title, description, date):
        errors = cls.validate(title, description, date)
        if errors:
            return False, errors
        event = cls.objects.create(title=title, description=description, date=date)
        return True, event

    def update(self, title, description, date):
        self.title = title or self.title
        self.description = description or self.description
        self.date = date or self.date
        self.save()
