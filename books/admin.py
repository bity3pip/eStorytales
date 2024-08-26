from django.contrib import admin
from books.models import Book, Order, BookReview, Card, CardItem

admin.site.register(Book)
admin.site.register(BookReview)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'created', 'get_product')
    list_filter = ('created', 'user')
    search_fields = ('first_name', 'last_name', 'address', 'country', 'city', 'postal_code')
    actions = ['delete_selected_orders']

    def get_product(self, obj):
        return obj.product.title if obj.product else 'No product'

    get_product.short_description = 'Product'

    def delete_selected_orders(self, request, queryset):
        num_deleted, _ = queryset.delete()
        self.message_user(request, f"{num_deleted} order(s) were deleted.")

    delete_selected_orders.short_description = "Delete selected orders"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'total_items')
    search_fields = ('user__username',)


@admin.register(CardItem)
class CardItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'book', 'quantity')
    search_fields = ('card__id', 'book__title')
