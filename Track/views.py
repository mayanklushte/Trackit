from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.views import generic
from django.utils.safestring import mark_safe
import calendar
from django.shortcuts import render, get_object_or_404
from .models import *
from .utils import Calendar
from .forms import *
from django.db.models import Q

# Create your views here.


def index(request):

    return render(request, 'index.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def registers(request):

    registered = False

    if request.method == 'POST':

        form_p = UserForm(data=request.POST)
        form = Register_form(data=request.POST)

        if form.is_valid() and form_p.is_valid():

            user = form_p.save()
            user.set_password(user.password)
            user.save()

            form_r = form.save(commit=False)
            form_r.user = user  # here connected OneToOneField with user table

            if 'profile_photo' in request.FILES:
                form_r.profile_photo = request.FILES['profile_photo']

            form_r.save()

            return HttpResponseRedirect(reverse('login'))
        else:
            print(form_p.errors, form.errors)
    else:
        form_p = UserForm()
        form = Register_form()
    return render(request, 'login/register_page.html', {'form': form, 'form_p': form_p, 'registered': registered})

# login page view


def user_login(request):
    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user.is_superuser:

            # Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('r_com'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        elif user.is_staff:
            if user.is_active:
                # Log the user in.
                login(request, user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('ap_list'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        elif user.is_active:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse('accp_list'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        # Nothing has been provided for username or password.
        return render(request, 'login/login.html')

# ------ admin part starts here ------

# register company list


def reg_com(request):
    list = register.objects.all().exclude(user__is_superuser=True).exclude(user__is_staff=True)
    query = request.GET.get('q')
    if query:
        list = list.filter(company_name__icontains=query)
        return render(request, 'admin/r_com.html', {'list': list})

    return render(request, 'admin/r_com.html', {'list': list})


# project assign form


def project(request, id):
    try:
        r = register.objects.get(id=id)
        if request.method == 'POST':
            form = c_details_form(request.POST)
            form2 = RelationForm(request.POST)
            if form.is_valid() and form2.is_valid():

                dat = form.save(commit=False)
                dat.company_Name = r

                dat.save(True)

                dat2 = form2.save(commit=False)
                dat2.sender_r = r
                dat2.receiver_r = dat.staff_member
                dat2.save(True)

                return HttpResponseRedirect(reverse('comlist'))
        else:
            form = c_details_form()
            form2 = RelationForm()
        return render(request, 'admin/admin.html', {'form': form, 'form2': form2, 'list': r})
    except:
        r = register.objects.get(id=id)
        if request.method == 'POST':
            form = c_details_form(request.POST)
            form2 = RelationForm(request.POST)
            if form.is_valid() and form2.is_valid():
                dat2 = form2.save(commit=False)
                dat2.sender_r = None
                dat2.receiver_r = None
                dat2.save(True)

                dat = form.save(commit=False)
                dat.company_Name = r

                dat.save(True)

                return HttpResponseRedirect(reverse('comlist'))
        else:
            form = c_details_form()
            form2 = RelationForm()
        return render(request, 'admin/admin.html', {'form': form, 'form2': form2, 'list': r})


# chat list


def comlist(request):
    user = request.user

    list = register.objects.all().exclude(user_id=user)
    return render(request, 'admin/comlist.html', {'list': list})


# chat room


def comd(request, id):
    r = register.objects.get(id=id)
    messages = message.objects.filter(Q(sender=request.user, receiver=r.user) |
                                      Q(sender=r.user, receiver=request.user)).order_by('date', 'time')

    listsq = register.objects.filter(id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.sender = request.user
            data.receiver = r.user
            data.save(True)

        form = MessageForm()
    else:
        form = MessageForm()

    return render(request, 'admin/comdetails.html', {'listsq': listsq, 'form': form, 'message': messages})


# assigned project list


def a_comlist(request):
    list = comdetails.objects.filter(Q(status=True) | Q(status=False))

    return render(request, 'admin/a_comlist.html', {'list': list})


# assigned task details


def a_comd(request, id):

    listsq = comdetails.objects.filter(id=id)

    return render(request, 'admin/a_comd.html', {'listsq': listsq})

# track your progress calendar


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs,):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'cal/event.html', {'form': form})

# ------ admin part end here ----------

# -----user part start here -----------

# accepted project list


def accp_list(request):
    user = request.user
    list = comdetails.objects.filter(company_Name__user_id=user)
    return render(request, 'user/accp_list.html', {'list': list})

# accepted project details


def accp_details(request, id):
    try:
        listsq = comdetails.objects.get(id=id)

    except comdetails.DoesNotExist:
        raise Http404("")
    return render(request, 'user/accp_details.html', {'j': listsq})


def u_project(request):
    user = request.user
    list = comdetails.objects.filter(company_Name__user_id=user)
    return render(request, 'u_project.html', {'i': list})

# user event list


def u_event(request):
    user = request.user
    list = Event.objects.filter(company_Name__company_Name__user_id=user)
    return render(request, 'cal/cal2.html', {'list': list})

# event details


def event_d(request, id):
    list = Event.objects.get(id=id)

    return render(request, 'cal/event_det.html', {'list': list})


# project request list


def project_list(request):
    user = request.user
    list = comdetails.objects.filter(company_Name__user_id=user)
    return render(request, 'user/u_plist.html', {'list': list})

# project details


def project_details(request, id):
    try:
        listsq = comdetails.objects.get(id=id)

    except comdetails.DoesNotExist:
        raise Http404("")
    return render(request, 'user/u_pdetails.html', {'j': listsq})

# accept button view


def accept(request, id):
        try:
            listsz = comdetails.objects.get(id=id)
            listsz.status = True
            listsz.save()
            if listsz.status == True:
                return HttpResponseRedirect(reverse('accp_list'))

        except comdetails.DoesNotExist:
            raise Http404("")

        return render(request, 'user/u_pdetails.html', {'listsz': listsz})

# reject button view


def reject(request, id):
    try:
        listsy = comdetails.objects.get(id=id)
        listsy.status = False
        listsy.save()
        if listsy.status==False:
            return HttpResponseRedirect(reverse('accp_list'))

    except comdetails.DoesNotExist:
        raise Http404("")

    return render(request, 'user/u_pdetails.html', {'listsy': listsy})

# user event


def user_event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('u_event'))
    return render(request, 'cal/event.html', {'form': form})

# chat app user


def u_comlist(request):
    user = request.user
    list = User.objects.filter(is_superuser=True)
    list1 = relation.objects.all().exclude(~Q(sender_r__user_id=user))

    return render(request, 'user/chatlist.html', {'list':list, 'list1':list1})


# chat room user


def u_comd(request, id):
    r = User.objects.get(id=id)
    messages = message.objects.filter(Q(sender=request.user, receiver=r.id)| Q(sender=r.id, receiver=request.user)).order_by('date', 'time')

    list = User.objects.filter(id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.sender = request.user
            data.receiver = r.register.user
            data.save(True)

        form = MessageForm()
    else:
        form = MessageForm()

    return render(request, 'user/chatdetails.html', {'list': list, 'form': form, 'message': messages})


# third User data


def mi_add(request):
    list = comdetails.objects.filter(staff_member=request.user)
    return render(request, 'mi-add/comlist.html', {'list': list})


def mi_p_det(request, id):
    list = comdetails.objects.filter(id=id)
    return  render(request, 'mi-add/ma_comdet.html', {'list': list})


def au_event(request):

    list1 = Event.objects.filter(company_Name__staff_member=request.user)
    return render(request, 'mi-add/ma_event.html', {'list': list1})

# event details


def aevent_d(request, id):
    list = Event.objects.get(id=id)

    return render(request, 'mi-add/event_det.html', {'list': list})


def acomlist(request):
    user = request.user
    list2 = User.objects.filter(is_superuser=True)
    list = comdetails.objects.filter(staff_member=user)

    return render(request, 'mi-add/acomlist.html', {'list': list, 'list2': list2})


# chat room


def acomd(request, id):

    r = comdetails.objects.get(id=id)
    messages = message.objects.filter(Q(sender=request.user, receiver=r.company_Name.user) |
                                      Q(sender=r.company_Name.user, receiver=request.user)).order_by('date', 'time')

    listsq = comdetails.objects.filter(id=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.sender = request.user
            data.receiver = r.company_Name.user
            data.save(True)

        form = MessageForm()
    else:
        form = MessageForm()

    return render(request, 'mi-add/comdetails.html', {'listsq': listsq, 'form': form, 'message': messages})
