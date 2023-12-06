from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='책 제목')
    # ManyToManyField는 다대다 FK관계일 때 쓰인다.
    authors = models.ManyToManyField('Author', verbose_name='저자')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    publication_date = models.DateField(verbose_name='출판날짜')

    def __str__(self):
        return self.title


class Author(models.Model):
    salutation = models.CharField(max_length=100, verbose_name='인사말')
    name = models.CharField(max_length=50, verbose_name='이름')
    email = models.EmailField(verbose_name='이메일 주소')

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    website = models.URLField()

    def __str__(self):
        return self.name