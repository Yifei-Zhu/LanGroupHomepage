from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=500, help_text="Enter the author's name")

    def __str__(self):
        return self.name

class Publication(models.Model):
    title = models.CharField(max_length=200, help_text='Enter the title of the publication')
    year = models.IntegerField(default=2024)
    authors = models.ManyToManyField(Author, help_text='Select authors for this publication')
    # 注意这里我们将字段名从单数变为了复数，更好地反映了其含义

    class Meta:
        abstract = True
    def __str__(self):
        author_names = ", ".join([author.name for author in self.authors.all()])
        return f"{author_names}"

class Book(Publication):
    publisher = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200, verbose_name="Book Title")
    editor = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Paper(Publication):
    journal_name = models.CharField(max_length=100)
    volume = models.CharField(max_length=20)
    page = models.CharField(max_length=20)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.title



