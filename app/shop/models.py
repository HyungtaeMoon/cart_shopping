from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    # 글자, 숫자, 밑줄, 하이픈만 취급.
    #   url 주소에 대문자, 공백이 들어갈 경우에 %20 과 같은 문자가 들어가게 되어
    #   명확한 url 주소가 아님.
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    # media/category 경로에 이미지가 저장됨
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 소수점까지 표현할 수 있는 Decimafield 를 사용
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    # 체크박스 형태로 True/False 를 가짐
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
