from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords

User = get_user_model()

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Hero(models.Model):
    HERO_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archieved', 'Archieved'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)# If a hero ever decides to be a user on our site
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='heroes/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='heroes')
    origin_nomination = models.ForeignKey(
        "Nomination",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="origin_hero"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_heroes"
    )
    status = models.CharField(
        max_length=20,
        choices=HERO_STATUS,
        default='draft'
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Hero"
        verbose_name_plural = "Heroes"

    @property
    def display_name(self):
        if self.user:
            return self.user.username

        return self.name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Nomination(models.Model):
    NOMINATION_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    CONTACT_STATUS = [
        ('not_contacted', 'Not Contacted'),
        ('contacted', 'Contacted'),
        ('follow_up', 'Follow Up'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Nominee details
    nominee_name = models.CharField(max_length=255)
    nominee_email = models.CharField(blank=True, null=True)
    nominee_phone = models.CharField(max_length=15, blank=True, null=True)
    nominee_location = models.CharField(max_length=255, blank=True, null=True)

    # Nominator
    nominator_name = models.CharField(max_length=255, blank=True, null=True)
    nominator_email = models.CharField(blank=True, null=True)
    nominator_phone = models.CharField(max_length=15, blank=True, null=True)
    nominator_location = models.CharField(max_length=255, blank=True, null=True)

    # Story and metadata
    story = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    nominated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='nominations'
    )
    status = models.CharField(max_length=20, choices=NOMINATION_STATUS, default='pending')

    contact_status = models.CharField(max_length=20, choices=CONTACT_STATUS, default='not_contacted')
    
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_nominations')
    approved_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.nominated_by:
            nominator_name = self.nominated_by.username
        else:
            nominator_name = self.nominee_name
        return f"{self.nominee_name} nominated by {nominator_name} - {self.status}"

class Interview(models.Model):
    INTERVIEW_STATUS = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interviews'
    )
    story = models.ForeignKey('Story', on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews')
    nomination = models.ForeignKey('Nomination', on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews')
    hero = models.ForeignKey('Hero', on_delete=models.SET_NULL, null=True, blank=True, related_name='interviews')
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        creating = self._state.adding
        super().save(*args, **kwargs)

        if creating:
            hero, created = Hero.objects.get_or_create(
                name=self.nomination.nominee_name,
                email=self.nomination.nominee_email,
                phone_number=self.nomination.nominee_phone,
                location=self.nomination.nominee_location,
            )
            self.hero = hero
            super().save(update_fields=['hero'])

            print("Updating nomination", self.nomination.status, self.nomination.contact_status)
            self.nomination.contact_status = 'interview_scheduled'
            self.nomination.status = 'approved'
            self.nomination.save()
            print("Done udating nomination", self.nomination.status, self.nomination.contact_status)

        if self.status == 'completed':
            story, _ = Story.objects.get_or_create(
                hero=self.hero,
                nomination=self.nomination,
                title=f"{self.hero.name} Interview title - draft",
                content=self.notes if self.notes else f"{self.hero.name}",
            )
            self.story = story
            super().save(update_fields=['story'])

            self.nomination.contact_status = 'completed'
            self.nomination.save()

    def __str__(self):
        return f"Interview for {self.nomination.nominee_name} - {self.status}"

class Story(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('published', 'Published')
    ]

    hero = models.ForeignKey('Hero', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    nomination = models.ForeignKey('Nomination', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    title = models.CharField(max_length=255)
    content = models.JSONField()
    intro = models.TextField(help_text='Short summary for listing previews', null=True, blank=True)
    impact = models.TextField(null=True, blank=True)
    aurthor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_stories')
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Stories"

    def __str__(self):
        return f"{self.title} for {self.hero.display_name}"
