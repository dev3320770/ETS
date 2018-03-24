# Create your views here.
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .models import LicenceInfo
from .models import Ticket
from .models import Profile
from .forms import DirectionForm
from.forms import ProfileUpdate
from .forms import SignUpForm
from .models import VehicleInfo
from ets import models
from ets import paypal
from datetime import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.idNumber = form.cleaned_data.get('idNumber')
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your ETIMS Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def user_account(request):
    if request.user.is_authenticated:

        #owner = request.user.profile.idNumber

        #lics = LicenceInfo.objects.raw('select * from ets_licenceInfo where owner = %s', owner)
        lics = LicenceInfo.objects.filter(owner=request.user.profile.idNumber)
        #vehs = VehicleInfo.objects.raw('select * from ets_vehicleInfo where owner = %s', owner)
        vehs = VehicleInfo.objects.filter(owner=request.user.profile.idNumber)

        for lic in lics:
            licinfo = lic.licenceBarcode

            for veh in vehs:
                vehinfo = veh.regNumber

                tics = Ticket.objects.raw(
                    'select *   from ets_ticket where ets_ticket.regNumber = %s or ets_ticket.licenceBarcode=%s group by ets_ticket.id', [vehinfo, licinfo])

                total = 0

                for tic in tics:
                    total += tic.amount

                    #
                    #
                    # orig_date1 = str(tic.dateCreated)
                    # orig_date2 = str(tic.deadline)
                    #
                    # dt1 = datetime.strptime(orig_date1, "%Y-%m-%d %H:%M:%S.%f%z")
                    # dt2 = datetime.strptime(orig_date2, "%Y-%m-%d %H:%M:%S%z")


                #total = models.Ticket.objects.filter(paymentBy=request.user)


        # for lic in lics:
            #
            # tics = Ticket.objects.all().filter(licenceBarcode=lic.licenceBarcode).distinct()
            # total = Ticket.objects.all().filter(licenceBarcode=lic.licenceBarcode).aggregate(total=Sum('amount'))['total']or ''
            #
            # for veh in vehs:
            #         ticsvehs = Ticket.objects.all().filter(regNumber=veh.regNumber).distinct()
            #         totalveh = Ticket.objects.all().filter(regNumber=veh.regNumber).aggregate(total=Sum('amount'))['total']or ''

            #  total = Ticket.objects.filter(licenceBarcode=lic.licenceBarcode).aggregate(total=Sum('amount'))
            #  totalveh = Ticket.objects.filter(regNumber=veh.regNumber).aggregate(total=Sum('amount'))
            #totalamout = totalveh + total


            # tickets = connection.cursor()
            #tickets.execute("""select * from ets_ticket where ets_ticket.regNumber = 'N123W' or ets_ticket.licenceBarcode='9191' group by ets_ticket.id""")
            #result = tickets.fetchall()

    return render(request, 'home.html', locals())

@login_required
def my_profile(request):
    pros = Profile.objects.filter(user=request.user.id)


    return render(request, 'profile.html', locals())


@login_required
def settings(request):
    return render(request, 'settings.html', locals())


def direction_create(request):
    if request.method == 'POST':
        direction_form = DirectionForm(data=request.POST)

        if direction_form.is_valid():
            direction = direction_form.save()
            return redirect('/direction', pk=direction.pk)
    else:
        direction_form = DirectionForm()
    return render(request, "contact.html", {"form": direction_form})



@login_required() # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = ProfileUpdate(instance=user)

    # The sorcery begins from here, see explanation below
    profileinlineformset = inlineformset_factory(User, Profile, fields=('photo', 'gender', 'idNumber', 'cellNumber', 'country', 'town', 'organization', 'occupation', 'dob'))
    formset = profileinlineformset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = ProfileUpdate(request.POST, request.FILES, instance=user)
            formset = profileinlineformset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = profileinlineformset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():

                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/profile/')

        return render(request, "demo.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied



@login_required
def details(request, id):
    ticket = get_object_or_404(models.Ticket, pk=id)
    return render(request, 'details.html', locals())

@login_required
def pay(request, id):
    ticket = get_object_or_404(models.Ticket, pk=id)

    try:
        #payment = Payment.objects.get( paymentBy=request.user )
        payment = models.Payment.objects.get(ticket=ticket, paymentBy=request.user)
        #tics = Ticket.objects.all().filter(licenceBarcode=lic.licenceBarcode).distinct()


        return payment

    except models.Payment.DoesNotExist:

        return render_to_response('purchase.html', { 'ticket': ticket, 'paypal_url': 'https://www.sandbox.paypal.com/au/cgi-bin/webscr', 'paypal_email': 'festusiipito-facilitator@gmail.com', 'paypal_return_url': 'http://127.0.0.1:8000'  } )


def paid( request, uid, id ):
    ticket = get_object_or_404( models.Ticket, pk=id )
    user = get_object_or_404( User, pk=uid )

    if request.REQUEST.has_key('tx'):
        tx = request.REQUEST['tx']
        try:
            existing = models.Payment.objects.get( tx=tx )
            return render_to_response('error.html', { 'error': "Duplicate transaction" })

        except models.Payment.DoesNotExist:
            result = paypal.Verify( tx )

        if result.success() and ticket.amount == payment.amount(): # valid
            payment = models.Payment( ticket=ticket, paymentBy=user, tx=tx )
            payment.save()
            return render_to_response('purchased.html', { 'ticket': ticket })

        else: # didn't validate
            return render_to_response('error.html', { 'error': "Failed to validate payment" })












