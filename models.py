from django.db import models
#from .validators import validate_com

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Contact(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    #sender = models.EmailField(validators=[validate_com])
    cc_myself = models.BooleanField(blank=True, null=True)