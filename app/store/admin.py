from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'image']
    # name(상품명) 에 입력을 함과 동시에 공백을 하이픈으로, 대문자를 소문자로 실시간 자동 입력
    prepopulated_fields = {'slug': ('name',)}


# admin 에 Category 모델과 CategoryAdmin 모델을 등록
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'updated_at']
    # admin 페이지에서 수정할 수 있도록 editable 옵션을 추가
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20


admin.site.register(Product, ProductAdmin)
