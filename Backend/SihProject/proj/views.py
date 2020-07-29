from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .forms import AppUserForm, ExtendedUserForm, MyForm1
from .decorators import allowed_users
from django.template.loader import render_to_string
from .models import UserContributionModel
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib.auth import authenticate, login, logout
from .tokens import account_activation_token
from .models import AppUser, ActiveImages, UserContributionModel, ActiveArea, Queries
from django.db.models import Q, F
import time
from datetime import datetime, timedelta
from .generate_index_rough import GetUnAssignedIndexes
from rest_framework.authtoken.models import Token
from field_history.models import FieldHistory


def HomeView(request):
    li = UserContributionModel.objects.order_by('-contribution')
    l1 = []
    l2 = []
    l3 = []
    # print(li)
    c = 0
    for x in li:
        if(x.user.groups.all()[0].name == "NGO"):
            l1.append(x)
            l2.append(x.user)
            l3.append(AppUser(user=x.user))
            c += 1
            if(c == 3):
                break
    x1 = {}
    x2 = {}
    x3 = {}
    if(len(l1) > 0):
        x1 = {"name": l2[0].username, "contribution": l1[0].contribution,
              "address": l3[0].address, "mobile": l3[0].mob},
        x1 = x1[0]
    if(len(l1) > 1):
        x2 = {"name": l2[1].username, "contribution": l1[1].contribution,
              "address": l3[1].address, "mobile": l3[1].mob},
        x2 = x2[0]
    if(len(l1) > 2):
        x3 = {"name": l2[2].username, "contribution": l1[2].contribution,
              "address": l3[2].address, "mobile": l3[2].mob}
        x3 = x3[0]
    return render(request, 'index.html', {"li": {"one": x1, "two": x2, "three": x3}})


def Home2(request):
    return render(request, 'home.html')


@csrf_exempt
def SubmitQuery(request):
    if(request.method == 'POST'):
        try:
            print(request.user)
            print(request.POST)
            if(request.user.is_anonymous):
                user = None
                name = request.POST['name']
                email = request.POST['email']
            else:
                user = request.user
                name = request.user.username,
                name = name[0]
                email = request.user.email,
                email = email[0]

            message = request.POST['message']
            print(type(name))
            print(name)
            try:
                q1 = Queries.objects.create(
                    user=user,
                    name=name,
                    email=email,
                    message=message,
                )
                return HttpResponseRedirect('')
            except Exception as e:
                print("Exception")
                print(e)
                return HttpResponse(500)
        except Exception as e:
            print("Exception")
            print(e)
            return HttpResponse(500)


def UserRegister(request):
    if (request.method == 'POST'):
        # if 'signup' in request.POST:
        # print(request.POST)
        form1 = ExtendedUserForm(request.POST)
        form2 = AppUserForm(request.POST)
        # print(form1.is_valid())
        # print(form2.is_valid())
        choice = request.POST['choice']
        if (form1.is_valid() and form2.is_valid() and form1.clean()):
            user = form1.save(commit=False)
            print("Form validated")
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = "ctrlaltelitesih2020@gmail.com"
            send_mail(message=message,
                      from_email=email,
                      recipient_list=[user.email],
                      subject="Activate Your account")
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()
            UserContributionModel.objects.create(user=user)
            group = Group.objects.get(name=choice)
            group.user_set.add(user)
            return render(request, 'checkEmail.html')
        else:
            print(form1.errors)
            print(form2.errors)
            args = {
                'form1': form1,
                'form2': form2,
                "errors1": form1.errors,
                "errors2": form2.errors
            }
            return render(request, 'registration/register.html', args)

    else:
        # print(form1.errors)
        # print(form2.errors)
        form1 = ExtendedUserForm()
        form2 = AppUserForm()
        args = {'form1': form1, 'form2': form2}
        return


# Like This we can add allowed roles
@csrf_exempt
def UserRegisterMobile(request):
    if (request.method == 'POST'):
        # print("Here we are")
        # print(request.POST)
        form1 = ExtendedUserForm(request.POST)
        print(form1.is_valid())
        form2 = AppUserForm(request.POST)
        print(form2.is_valid())
        choice = request.POST['choice']
        print(form1.clean())
        # print(choice)

        if (form1.is_valid() and form2.is_valid() and form1.clean()):
            user = form1.save(commit=False)
            print("Form validated")
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = "ctrlaltelitesih2020@gmail.com"
            send_mail(message=message,
                      from_email=email,
                      recipient_list=[user.email],
                      subject="Activate Your account")
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()
            UserContributionModel.objects.create(user=user)
            group = Group.objects.get(name=choice)
            group.user_set.add(user)
            return HttpResponse(json.dumps({"status": 1}))
        else:
            print("Form Not validated")
            args = {
                'form1': form1,
                'form2': form2,
                "errors1": form1.errors,
                "errors2": form2.errors
            }
            z = {**form1.errors, **form2.errors}
            return HttpResponse(json.dumps({"status": 0, "errors": z}))

    else:
        form1 = ExtendedUserForm()
        print("Form Not validated 2")
        form2 = AppUserForm()
        args = {'form1': form1, 'form2': form2}
        z = {**form1.errors, **form2.errors}
        return HttpResponse(json.dumps({"status": 0, "errors": z}))


def LogoutView(request):
    logout(request)
    return redirect('/login')


@allowed_users(allowed_roles=['Government'])
def CheckOnlyGovernMentView(request):
    return render(request, 'gov.html')
    pass


# @allowed_users(allowed_roles=['NGO'])
def CheckOnlyNgoView(request):
    user = request.user
    return render(request, 'ngo.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return HttpResponse(
            'Thank you for your email confirmation. Now you can login your account.'
        )
    else:
        return HttpResponse('Activation link is invalid!')


@allowed_users(allowed_roles=['Government'])
def GetLocationList(request):
    if(request.method == "GET"):
        days = 1
        # Show All Images that are not completed and atleast 1 month old
        obj = ActiveArea.objects.filter(
            Q(completed=False) & Q(timestamp__lte=datetime.now()-timedelta(days=days)))

        # print(obj)

        return render(request, 'gov.html', {"list": obj})


# @allowed_users(allowed_roles=['Government'])
def GetAllRegisteredNGOs(request):
    # print("Here we Are")
    # Will Give Government the list of all registered NGOs
    if(request.method == "GET"):
        li = User.objects.filter(groups__name='NGO')
        print(li)

        l1 = []
        for x in li:
            z = AppUser.objects.get(user=x)
            y = UserContributionModel.objects.get(user=x)
            l1.append({
                "id": z.id,
                "name": z.user,
                "address": z.address,
                "rating": y.contribution,
                "workCompleted": y.workCompleted
            })
        print(l1)
        return render(request, 'NGOList.html', {"list": l1})


@allowed_users(allowed_roles=['NGO'])
@csrf_exempt
def NGOsHomePage(request):
    if(request.GET.get('mybtn')):
        i = request.GET.get('id')
        user = request.user
        z = ActiveArea.objects.get(pk=i)
        z.reviewed = True
        z.ngo = user
        z.save()
    if(request.GET.get('mybtn2')):
        i = request.GET.get('id')
        # Which Area Object is clicked
        # Get all Active Images linked to this one
        # And show them
        obj = ActiveArea.objects.get(pk=i)
        li = obj.activeimages_set.all()
        print(len(li))
        return render(request, "view-area.html", {"args": li})
    review_not_comp = ActiveArea.objects.filter(
        Q(completed=False) & Q(reviewed=False))
    return render(request, 'ngo.html', {"list": review_not_comp})


def CustomRedirect(request):
    if (request.user.groups.exists()):
        group = request.user.groups.all()[0].name
        print(group)
        if(group == "NGO"):
            return redirect('/ngolist')
        elif(group == "AppUsers"):
            return HttpResponse("Please Visit App this page is not designed for you")
        else:
            return redirect('/gov-ngoreviewed')


@allowed_users(allowed_roles=['NGO'])
def NGOProfilePage(request):
    if(request.GET.get('mybtn')):
        i = request.GET.get('id')
        print(i)
        obj = ActiveArea.objects.get(pk=i)
        li = obj.activeimages_set.all()
        li.update(completed=True)
        # print(type(obj.completed))
        var = True
        obj.completed = var
        obj.timestamp = datetime.now()
        obj.save()
        obj2 = UserContributionModel.objects.get(user=request.user)
        obj2.workCompleted += 1
        obj2.save()
    if(request.GET.get('mybtn2')):
        i = request.GET.get('id')
        # Which Area Object is clicked
        # Get all Active Images linked to this one
        # And show them
        obj = ActiveArea.objects.get(pk=i)
        li = obj.activeimages_set.all()
        print(len(li))
        return render(request, "view-area.html", {"args": li})

    # args1 = ActiveArea.objects.filter(
    #     Q(ngoName=request.user))
    args1 = request.user.activearea_set.all()
    args2 = AppUser.objects.get(user=request.user)
    args3 = UserContributionModel.objects.get(user=request.user)
    args = {
        "name": args2.user,
        "address": args2.address,
        "mob": args2.mob,
        "email": request.user.email,
        "rating": args3.contribution,
        "workCompleted": args3.workCompleted,
    }
    li = []
    li2 = []
    for x in args1:
        if(x.completed == False):
            li.append({
                "lat": x.lat,
                "lon": x.lon,
                "timestamp": x.timestamp,
                "id": x.pk,
            })
        else:
            li2.append({
                "lat": x.lat,
                "lon": x.lon,
                "timestamp": x.timestamp,
                "id": x.pk
            })

    args["imagesActive"] = li
    args["imagesCompleted"] = li2
    # print(args)

    return render(request, 'NGOProfile.html', {"list": args})


def UsersLeaderboard(request):
    li = UserContributionModel.objects.order_by('-contribution')
    l1 = []
    print(li)
    for x in li:
        if(x.user.groups.all()[0].name == "AppUsers"):
            l1.append(x)
    l1 = l1[:100]
    print(l1)
    return render(request, 'LeaderBoard.html', {"list": l1})


def NGOLeaderboard(request):
    li = UserContributionModel.objects.order_by('-contribution')
    l1 = []
    print(li)

    for x in li:
        if(x.user.groups.all()[0].name == "NGO"):
            l1.append(x)
    l1 = l1[:100]
    print(l1)
    return render(request, 'LeaderBoard.html', {"list": l1})


def compute_distance(x, y, u, v):

    slat = radians(float(x))
    slon = radians(float(y))
    elat = radians(float(u))
    elon = radians(float(v))

    dist = 1000 * 6371.01 * \
        acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist


@allowed_users(allowed_roles=['Government'])
def UpdateRating(request):
    if(request.method == "POST"):
        id = request.POST.get("id")
        rating = request.POST.get("rating")
        obj = User.objects.get(pk=id)
        uc = UserContributionModel(user=obj)
        uc += rating
        uc.save()
        return HttpResponse(200)


@allowed_users(allowed_roles=['Government'])
def GetFieldHistory(request):
    if(request.method == "GET"):
        id = request.GET.get("id")
        model = UserContributionModel.objects.get(pk=id)
        model.fieldhistory_set.all()

    # Get field history for particular ngo


def RunDaily(request):

    #########################################
    # The images which dont have parents assign them parent if they belongs
    # to some active area

    li = ActiveImages.objects.filter(area=None)
    for obj in li:
        print(obj.pk)
        # If there is
        err = 0.1
        l = ActiveArea.objects.filter(Q(completed=False) &
                                      Q(lat__lte=(obj.lat+err)) & Q(lat__gte=(obj.lat-err)) & Q(lon__lte=(obj.lon+err)) & Q(lon__gte=(obj.lon-err)))
        if(len(l) > 0):
            print(obj.pk, "Assigned to Some Area")
            elem = l[0]
            # Modify This object
            elem.index = elem.index+35+10*obj.animals
            elem.save()
            obj.area = elem
            obj.save()

        # elem.
    print("1st part done\n")
    lat, lon, ind, keys = GetUnAssignedIndexes()
    print("2nd part done\n")

    #########################################
    for i in range(len(lat)):
        try:
            o1 = ActiveArea.objects.create(
                lat=lat[i],
                lon=lon[i],
                index=ind[i],
            )
            for j in range(len(keys[i])):
                obj = ActiveImages.objects.get(pk=keys[i][j])
                obj.area = o1
                obj.save()
            print(o1.activeimages_set.all())
            print("Work Completed\n")
        except Exception as e:
            print("Some Error Occured")
            print(e)

    #####################################################

    # After Working with area grouping Update leaderboards
