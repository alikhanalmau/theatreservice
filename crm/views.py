import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EventForm, ExcursionForm, ExcursionSlotForm, TicketOrderForm, UserRoleForm
from django.contrib.auth.decorators import user_passes_test
from theatre.models import Event, ExcursionOrder, ExcursionSlot, TicketOrder
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm



def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def dashboard(request):
    User = get_user_model()

    stats = {
        'event_count': Event.objects.count(),
        'excursion_count': ExcursionOrder.objects.count(),
        'ticket_count': TicketOrder.objects.count(),
        'user_count': User.objects.count(),
    }

    return render(request, 'crm/dashboard.html', {'stats': stats})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'crm/event_list.html', {'events': events})


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def event_edit(request, event_id=None):
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    else:
        event = None

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('crm-event-list')
    else:
        form = EventForm(instance=event)

    return render(request, 'crm/event_form.html', {'form': form, 'event': event})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('crm-event-list')

    return render(request, 'crm/event_confirm_delete.html', {'event': event})

def crm_login(request):
    if request.user.is_authenticated:
        return redirect('crm-dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('crm-dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'crm/login.html', {'form': form})


def crm_logout(request):
    logout(request)
    return redirect('crm-login')


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def excursion_list(request):
    excursions = ExcursionOrder.objects.select_related('slot').order_by('slot__date', 'slot__time')
    return render(request, 'crm/excursion_list.html', {'excursions': excursions})


@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def excursion_edit(request, excursion_id=None):
    excursion = ExcursionOrder.objects.get(pk=excursion_id) if excursion_id else None

    if request.method == 'POST':
        form = ExcursionForm(request.POST, instance=excursion)
        if form.is_valid():
            form.save()
            return redirect('crm-excursion-list')
    else:
        form = ExcursionForm(instance=excursion)

    return render(request, 'crm/excursion_form.html', {'form': form, 'excursion': excursion})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def excursion_delete(request, excursion_id):
    excursion = ExcursionOrder.objects.get(pk=excursion_id)
    if request.method == 'POST':
        excursion.delete()
        return redirect('crm-excursion-list')
    return render(request, 'crm/excursion_confirm_delete.html', {'excursion': excursion})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def ticket_list(request):
    tickets = TicketOrder.objects.select_related('user', 'event').order_by('-created_at')
    return render(request, 'crm/ticket_list.html', {'tickets': tickets})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def ticket_edit(request, ticket_id=None):
    ticket = TicketOrder.objects.get(pk=ticket_id) if ticket_id else None

    if request.method == 'POST':
        form = TicketOrderForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('crm-ticket-list')
    else:
        form = TicketOrderForm(instance=ticket)

    return render(request, 'crm/ticket_form.html', {'form': form, 'ticket': ticket})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def ticket_delete(request, ticket_id):
    ticket = TicketOrder.objects.get(pk=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('crm-ticket-list')
    return render(request, 'crm/ticket_confirm_delete.html', {'ticket': ticket})


User = get_user_model()

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'crm/user_list.html', {'users': users})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def ticket_list(request):
    tickets = TicketOrder.objects.select_related('user', 'event').order_by('-created_at')
    
    # Фильтрация
    user_id = request.GET.get('user')
    event_id = request.GET.get('event')

    if user_id:
        tickets = tickets.filter(user_id=user_id)

    if event_id:
        tickets = tickets.filter(event_id=event_id)

    users = User.objects.all()
    events = Event.objects.all()

    return render(request, 'crm/ticket_list.html', {
        'tickets': tickets,
        'users': users,
        'events': events,
        'selected_user': user_id,
        'selected_event': event_id,
    })

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserRoleForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('crm-user-list')
    else:
        form = UserRoleForm(instance=user)

    return render(request, 'crm/user_form.html', {'form': form, 'user_obj': user})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def export_tickets_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ticket_orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Пользователь', 'Спектакль', 'Кол-во', 'Статус', 'Комментарий', 'Дата'])

    tickets = TicketOrder.objects.select_related('user', 'event').order_by('-created_at')
    for t in tickets:
        writer.writerow([
            t.user.username,
            t.event.title,
            t.count,
            t.get_status_display(),
            t.comment,
            t.created_at.strftime('%d.%m.%Y %H:%M'),
        ])

    return response

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Логин', 'Email', 'Имя', 'Фамилия', 'Роль', 'Дата регистрации'])

    users = User.objects.all().order_by('-date_joined')
    for user in users:
        writer.writerow([
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            user.role,
            user.date_joined.strftime('%d.%m.%Y %H:%M'),
        ])

    return response

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def user_list(request):
    role = request.GET.get('role')
    users = User.objects.all().order_by('-date_joined')
    if role:
        users = users.filter(role=role)

    roles = User.objects.values_list('role', flat=True).distinct()

    return render(request, 'crm/user_list.html', {
        'users': users,
        'roles': roles,
        'selected_role': role,
    })

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def export_excursions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="excursions.csv"'

    writer = csv.writer(response)
    writer.writerow(['Пользователь', 'Дата', 'Время', 'Комментарий', 'Создано'])

    excursions = ExcursionOrder.objects.select_related('user').order_by('-created_at')
    for e in excursions:
        writer.writerow([
            e.user.username,
            e.date.strftime('%d.%m.%Y'),
            e.time.strftime('%H:%M'),
            e.comment,
            e.created_at.strftime('%d.%m.%Y %H:%M'),
        ])

    return response

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def export_events_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="events.csv"'

    writer = csv.writer(response)
    writer.writerow(['Название', 'Описание', 'Дата', 'Дата создания', 'Изображение'])

    events = Event.objects.all().order_by('-date')
    for event in events:
        writer.writerow([
            event.title,
            event.description,
            event.date.strftime('%d.%m.%Y %H:%M'),
            event.created_at.strftime('%d.%m.%Y %H:%M'),
            event.image.url if event.image else '',
        ])

    return response

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def add_excursion_slot(request):
    if request.method == 'POST':
        form = ExcursionSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crm-excursion-slot-list')
    else:
        form = ExcursionSlotForm()
    return render(request, 'crm/excursion_slot_form.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='crm-login')
def excursion_slot_list(request):
    slots = ExcursionSlot.objects.order_by('-date', '-time')
    return render(request, 'crm/excursion_slot_list.html', {'slots': slots})