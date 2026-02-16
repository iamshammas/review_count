from datetime import date
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Advisor, Reviewer, Review
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def update_status(request):
    if request.method == "POST":
        data = json.loads(request.body)

        review = Review.objects.get(id=data["id"])
        review.status = data["status"]
        review.save()

        return JsonResponse({"success": True})


# ---------- HISTORY ----------
def review_history(request):
    today = date.today()
    first_day = today.replace(day=1)

    start = request.GET.get("start")
    end = request.GET.get("end")

    reviews = Review.objects.all()

    if start and end:
        reviews = reviews.filter(review_date__range=[start, end])
    else:
        reviews = reviews.filter(review_date__gte=first_day)

    reviews = reviews.select_related(
        "advisor", "reviewer"
    ).order_by("-review_date")

    return render(request, "reviews/history.html", {
        "reviews": reviews,
    })


# ---------- ADD MULTIPLE REVIEWS ----------
def add_review(request):
    advisors = {a.name: a.id for a in Advisor.objects.all()}
    reviewers = {r.name: r.id for r in Reviewer.objects.all()}

    if request.method == "POST":
        review_date = request.POST["review_date"]
        bulk_text = request.POST["bulk_data"]

        lines = bulk_text.splitlines()

        for line in lines:
            parts = [p.strip() for p in line.split("|")]

            if len(parts) != 4:
                continue

            advisor_name, intern, week, reviewer_name = parts

            # advisor must exist
            if advisor_name not in advisors:
                continue

            # create reviewer if not exists
            if reviewer_name not in reviewers:
                reviewer = Reviewer.objects.create(
                    name=reviewer_name,
                    stack="Unknown"
                )
                reviewers[reviewer_name] = reviewer.id

            Review.objects.create(
                review_date=review_date,
                advisor_id=advisors[advisor_name],
                reviewer_id=reviewers[reviewer_name],
                intern=intern,
                current_week=week,
            )

        return redirect("review_history")

    return render(request, "reviews/add_review.html")




# ---------- DASHBOARD ----------
def dashboard(request):
    today = date.today()
    first_day = today.replace(day=1)

    start = request.GET.get("start")
    end = request.GET.get("end")
    advisor_id = request.GET.get("advisor")
    reviewer_id = request.GET.get("reviewer")

    qs = Review.objects.all()

    # date filter
    if start and end:
        qs = qs.filter(review_date__range=[start, end])
    else:
        qs = qs.filter(review_date__gte=first_day)

    # advisor filter
    if advisor_id:
        qs = qs.filter(advisor_id=advisor_id)

    # reviewer filter
    if reviewer_id:
        qs = qs.filter(reviewer_id=reviewer_id)

    advisor_counts = qs.values(
        "advisor__name"
    ).annotate(total=Count("id"))

    reviewer_counts = qs.values(
        "reviewer__name"
    ).annotate(total=Count("id"))

    return render(request, "reviews/dashboard.html", {
        "advisor_counts": advisor_counts,
        "reviewer_counts": reviewer_counts,
        "advisors": Advisor.objects.all(),
        "reviewers": Reviewer.objects.all(),
    })
