from django.db import models


class Publication(models.Model):
    title = models.CharField(max_length=200, help_text='Enter the title of the publication')
    year = models.IntegerField(default=2024)
    author = models.CharField(max_length=200, help_text='eg: J. Zhang, J. Peng, Y. Zhu, D. Hu* and Z. Lan*', verbose_name='Authors')
    class Meta:
        abstract = True

class Book(Publication):
    publisher = models.CharField(max_length=100)
    book_title = models.CharField(max_length=200, verbose_name="Book Title")
    editor = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Paper(Publication):
    journal_name = models.CharField(max_length=100, help_text='Please follow the standard journal abbreviation (ISO4), eg: J. Phys. Chem. Lett.')
    volume = models.CharField(max_length=20)
    page = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    indexed = models.CharField(max_length=20, default = 'SCI')

    def __str__(self):
        return self.title


class Funding(models.Model):
    title_in_Cn = models.CharField(max_length=200, help_text="Enter the title of the funding in Chinese")

    source_in_En = models.CharField(max_length=100, default='NSFC', help_text="Enter the funding source in English, eg: NSFC")
    source_in_Cn = models.CharField(max_length=100, default='国家自然科学基金委',help_text="Enter the funding source in Chinese,eg: 国家自然科学基金委")

    category_in_En = models.CharField(max_length=20, help_text="Enter the funding category in English, eg: major project")
    category_in_Cn = models.CharField(max_length=20, help_text="Enter the funding category in Chinese,eg: 重点项目")

    start_year = models.IntegerField(help_text="Enter the start year", default=2024)
    start_month = models.IntegerField(help_text="Enter the start month", choices=[(i, i) for i in range(1, 13)])
    end_year = models.IntegerField(help_text="Enter the end year", default=2024)
    end_month = models.IntegerField(help_text="Enter the end month", choices=[(i, i) for i in range(1, 13)])

    total_funding=models.IntegerField(help_text="Enter the total funding amount (in RMB)", verbose_name='Total Funding (W)')
    direct_funding=models.IntegerField(help_text="Enter the direct funding amount (in RMB)", verbose_name='Direct Funding (W)')



    def __str__(self):
        return f'{self.title_in_Cn}, {self.source_in_Cn}-{self.category_in_Cn}, {self.start_year}.{self.start_month}-{self.end_year}.{self.end_month}'


class Talk(models.Model):
    title  = models.CharField(max_length=200, help_text="Enter the title of the talk")
    conference_in_EN  = models.CharField(max_length=200, help_text="Enter the title of the conference in english")
    conference_in_CN  = models.CharField(max_length=200, help_text="Enter the title of the conference in chinese")

    start_date = models.DateField(help_text="Select the start date of the conference")
    end_date = models.DateField(help_text="Select the end date of the conference")

    country_in_CN = models.CharField(max_length=100, help_text="Enter the country of the conference in Chinese")
    city_in_CN = models.CharField(max_length=100, help_text="Enter the city of the conference in Chinese")

    country_in_EN = models.CharField(max_length=100, help_text="Enter the country of the conference in English")
    city_in_EN = models.CharField(max_length=100, help_text="Enter the city of the conference in English")

    category_in_Cn = models.CharField(max_length=100, help_text="Enter the category of the talk, eg: 大会报告")
    def __str__(self):
        return f"{self.conference_in_EN} ({self.start_date} - {self.end_date}), {self.city_in_CN}, {self.country_in_CN}"
