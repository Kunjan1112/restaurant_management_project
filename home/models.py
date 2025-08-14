from django.db import models

class Feedback(models.Model):
    comments = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comments[:20]