def calculate_average_rating(reviews_queryset):

    try:
        count = reviews_queryset.count()
        if count == 0:
            return 0.0

        total = sum(review.rating for review in reviews_queryset)
        return round(total / count, 2)
    
    except Exception:
        return 0.0