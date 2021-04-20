from django.shortcuts import render, redirect
from .models import Day
from .forms import DayForm, CreateUserForm
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .choices import choice
from .views_functions import get_month, get_total_hours, get_strp_time, get_month_name_czech
import datetime
import json


class DayDetailView(DetailView):
    model = Day


class DayUpdateView(UpdateView):
    model = Day
    fields = ["number_start", "number_end"]

    def form_valid(self, form):
        number_s = form.cleaned_data["number_start"]
        number_e = form.cleaned_data["number_end"]
        form.instance.result = get_strp_time(number_s, number_e)
        return super(DayUpdateView, self).form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class DayDeleteView(DeleteView):
    model = Day
    success_url = "/"

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


def register_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account was created - {user}")
            return redirect("login-page")

    context = {"form": form}
    return render(request, "hours_app/register_test.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username or password is incorrect.")
    return render(request, "hours_app/login_test.html")


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect("login-page")
    else:
        messages.warning(request, "You are not logged in.")
        return redirect("login-page")


def history_page(request):
    context = {}
    if "submit" in request.POST:
        form = Day.objects.filter(author=request.user)
        form_v1 = form.filter(
            working_day__contains=request.POST.get("month").upper())
        get_dt = request.POST.get("month").upper()

        if get_month(get_dt):
            total_hours = get_total_hours(form_v1)

            with open("year_month_database.json") as file:
                data = json.load(file)
                form_list = [item.working_day.split(
                    "-")[0].strip() for item in form_v1]

            DAYS_IN_MONTH = data[get_month(get_dt)]
            for i in form_list:
                for x in DAYS_IN_MONTH:
                    if i == x[0]:
                        DAYS_IN_MONTH.remove(x)

            context.update(
                {"form": form_v1, "choices": DAYS_IN_MONTH, "hours": total_hours})
        else:
            messages.warning(
                request, "Insert full name of month ex.: Leden, Únor, Březen...")
            return redirect("history")

    if "select" in request.POST:
        request.session['working_day'] = request.POST.get("choice_field")
        return redirect("get-hours-django")

    return render(request, "hours_app/history_page.html", context)


def all_data(request):
    all_data = Day.objects.filter(author=request.user)
    all_data_filtered = all_data.filter(
        working_day__contains=get_month_name_czech())

    total_hours = get_total_hours(all_data_filtered)
    total_money = total_hours * 130

    return render(request, "hours_app/all_data.html",
                  {"all_data": all_data_filtered,
                   "total_hours": total_hours,
                   "total_money": total_money
                   }
                  )


def money(request):
    if "submit" in request.POST:
        data = Day.objects.filter(author=request.user)
        data_filtered = data.filter(
            working_day__contains=request.POST.get("month").upper())
        hours = get_total_hours(data_filtered)
        request.session["hours"] = hours
        return render(request, "hours_app/money.html", {"hours": hours})
    if "apply" in request.POST:
        money = float(request.POST.get("money")) * \
            float(request.session.get("hours"))
        del request.session['hours']
        return render(request, "hours_app/money.html", {"money": money})
    return render(request, "hours_app/money.html")


def holiday(request):
    data = Day.objects.filter(author=request.user)
    data_filtered = data.filter(
        working_day__contains=f"HOLIDAY.{get_month_name_czech()} 2021")
    listek = [item[0] for item in data_filtered.values_list()]
    for num in range(1, 20):
        if f"{num}HOLIDAY.{get_month_name_czech()} 2021 - {request.user}" not in listek:
            request.session["working_day"] = f"{num}HOLIDAY.{get_month_name_czech()} 2021"
            return redirect("get-hours-django")


def get_hours_django(request):
    form = DayForm(request.user, request.POST)
    day = request.session.get("working_day")
    if "submit" in request.POST:
        if form.is_valid():
            if day:
                day = request.session.get("working_day")
            else:
                day = form.cleaned_data["working_day"]

            number_s = form.cleaned_data["number_start"]
            number_e = form.cleaned_data["number_end"]
            res = get_strp_time(number_s, number_e)

            Day.objects.create(working_day=f"{day} - {request.user}", number_start=number_s,
                               number_end=number_e, result=res,
                               author=request.user)
            messages.success(request, f"{day} SAVED!")
            if "working_day" in request.session.keys():
                del request.session['working_day']
                return redirect("history")
        return redirect("get-hours-django")

    return render(request, "hours_app/hours_app.html", {"form": form, "working_day": day})
