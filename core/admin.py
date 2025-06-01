from django.contrib import admin
from .models import BucketListItem, CompletedItem, ItemView

@admin.register(BucketListItem)
class BucketListItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'date_created', 'is_approved', 'views')
    list_filter = ('is_approved', 'date_created')
    search_fields = ('title', 'description', 'created_by__username')
    actions = ['approve_items']
    
    def approve_items(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} items have been approved.")
    approve_items.short_description = "Approve selected items"

@admin.register(CompletedItem)
class CompletedItemAdmin(admin.ModelAdmin):
    list_display = ('bucket_item', 'user', 'date_completed')
    list_filter = ('date_completed',)
    search_fields = ('bucket_item__title', 'user__username', 'description')

@admin.register(ItemView)
class ItemViewAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'ip_address', 'timestamp')
    list_filter = ('timestamp',)