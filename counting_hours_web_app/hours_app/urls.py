from django.urls import path
from hours_app import views
from .decorators import unauthenticated_user, authenticated_user, del_session

urlpatterns = [
    path('', del_session(unauthenticated_user(
        views.all_data)), name='home'),
    path('day/<pk>', unauthenticated_user(
        views.DayDetailView.as_view()), name='day-detail'),
    path('day/<pk>/update', unauthenticated_user(
        views.DayUpdateView.as_view()), name='day-update'),
    path('day/<pk>/delete', unauthenticated_user(
        views.DayDeleteView.as_view()), name='day-delete'),
    path('get_hours_django', unauthenticated_user(
        views.get_hours_django), name="get-hours-django"),
    path('register', authenticated_user(
        views.register_page), name='register-page'),
    path('login', authenticated_user(
        views.login_page), name='login-page'),
    path('logout', del_session(unauthenticated_user(
        views.logout_page)), name='logout-page'),
    path('history', del_session(unauthenticated_user(
        views.history_page)), name='history'),
    path('money', del_session(unauthenticated_user(
        views.money)), name='money'),
    path('holiday', del_session(unauthenticated_user(
        views.holiday)), name='holiday')
]
