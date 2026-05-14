from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# @login_required
# def profile_view(request):
#     """Страница профиля пользователя"""
#     # Пока просто редирект на главную или рендер шаблона
#     return render(request, "users/profile.html", {"user": request.user})
