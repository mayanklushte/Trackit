from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.urls import reverse

# Create your models here.


class register(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50, null=True)
    moblie_no = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    # address = models.CharField(max_length=200)
    # state = models.CharField(max_length=20)
    # pincode = models.CharField(max_length=6)
    # age = models.PositiveIntegerField()
    # sex = models.CharField(max_length=10)
    # profile_photo = models.ImageField(upload_to='profile_pic',blank=True)

    def __str__(self):
        return self.company_name


class comdetails(models.Model):
    company_Name = models.ForeignKey(register, on_delete=models.CASCADE)
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},null=True)
    project_name = models.CharField(max_length=50)
    technology = models.CharField(max_length=20)
    Domain = models.CharField(max_length=100)
    requirements = models.CharField(max_length=500)
    status = models.BooleanField(null=True)

    def __str__(self):
        return self.company_Name.company_name


class Event(models.Model):
    title = models.CharField(max_length=200)
    company_Name = models.ForeignKey(comdetails, on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.company_Name.staff_member} </a>'


class message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField(max_length=1000)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return self.sender.username


class relation(models.Model):
    sender_r = models.ForeignKey(register, on_delete=models.CASCADE, related_name='sender_r', null=True, blank=True)
    receiver_r = models.ForeignKey(User, on_delete=models.CASCADE,
                                   limit_choices_to={'is_staff': True},
                                   related_name='receiver_r', blank=True, null=True)

    class Meta:
        unique_together = ["sender_r", "receiver_r"]
