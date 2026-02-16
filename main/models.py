from django.db import models


class Advisor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reviewer(models.Model):
    name = models.CharField(max_length=100)
    stack = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):

    STATUS_PENDING = "pending"
    STATUS_NOT_DONE = "not_done"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_NOT_DONE, "Not Done"),
        (STATUS_DONE, "Done"),
    ]

    review_date = models.DateField()

    advisor = models.ForeignKey(Advisor, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)

    intern = models.CharField(max_length=120)
    current_week = models.CharField(max_length=50)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intern} - {self.advisor.name} - {self.reviewer.name} - {self.review_date}"