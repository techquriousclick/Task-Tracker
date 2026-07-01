# Task 3 - Debugging Challenge (25 minutes)
#
# The code below is part of a "Task Tracker" app (same theme as Task 2).
# It currently has 3 bugs that cause incorrect behavior or performance
# problems. They will NOT always throw an obvious error — some fail
# silently or only show up under certain conditions.
#
# Instructions:
#   1. Find all 3 bugs.
#   2. For each one, write 1-2 sentences explaining WHY it's a bug
#      (not just what the fix is).
#   3. Fix the code.
#
# You do NOT need a running Django project to do this — reasoning about
# the code and writing the corrected version is enough.

from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Task, Course


# --- Function 1 ---------------------------------------------------------
def add_tags_to_task(task, tags=[]):
    """
    Adds a list of tags to a task's tag list and returns it.
    Called repeatedly, once per task, when tasks are created via the API.
    """
    tags.append(f"course:{task.course_id}")
    task.tags = tags
    task.save()
    return tags


# --- Function 2 ---------------------------------------------------------
def get_courses_with_task_counts():
    """
    Returns a list of dicts: [{course_name, task_count}, ...]
    for every course in the system. Used on the dashboard page,
    which loads on every login.
    """
    results = []
    courses = Course.objects.all()

    for course in courses:
        task_count = Task.objects.filter(course=course).count()
        results.append({
            "course_name": course.title,
            "task_count": task_count
        })

    return results


# --- Function 3 ---------------------------------------------------------
def get_paginated_tasks(request):
    """
    Returns page `page_num` of tasks, 10 per page, as JSON.
    e.g. /tasks/?page=2 should return tasks 11-20.
    """
    page_num = int(request.GET.get("page", 1))
    page_size = 10

    all_tasks = Task.objects.all().order_by("id")
    start = page_num * page_size
    end = start + page_size

    page_tasks = all_tasks[start:end]

    data = [{"id": t.id, "title": t.title} for t in page_tasks]
    return JsonResponse({"page": page_num, "tasks": data})
