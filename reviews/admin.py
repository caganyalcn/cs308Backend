from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'comment', 'approved', 'created_at']
    list_filter = ['approved', 'rating', 'created_at']
    search_fields = ['user__email', 'product__name', 'comment']
    actions = ['approve_reviews', 'decline_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(approved=True)
    approve_reviews.short_description = "Approve selected reviews"

    def decline_reviews(self, request, queryset):
        queryset.delete()
    decline_reviews.short_description = "Decline and delete selected reviews"
