from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import *
from .threads import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from .forms import CandiateForm


@login_required(login_url='/accounts/login/')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def candiateSignUp(request):
    try:
        flag=False
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            web_address= request.POST.get('web_address')
            cover_letter=request.POST.get('cover_letter')
            attachment=request.FILES.get('attachment')
            do_you_like_working=request.POST.get('do_you_like_working')
            if do_you_like_working== "Yes":
                flag=True

            try:
                if Candidate.objects.filter(email=email).first():
                    messages.info(request, 'This account already exist. Try logging in.')
                    return redirect('../login')
                else:
                    new_customer = Candidate.objects.create(email=email, name=name,web_address=web_address,cover_letter=cover_letter,attachment=attachment,do_you_like_working=flag)
                    new_customer.set_password(password)
                    thread_obj = send_verification_otp(email)
                    thread_obj.start()
                    new_customer.save()
                    messages.info(request, 'We have sent you a verification OTP.\nPlease check your mail.')
                    return redirect('../verify')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        form = CandiateForm()
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/signup.html")


def candiateVerify(request):
    try:
        if request.method == 'POST':
            otp = request.POST.get('otp')
            try:
                if not cache.get(otp):
                    messages.info(request, 'Invalid OTP')
                else:
                    customer_obj = Candidate.objects.get(email = cache.get(otp))
                    if customer_obj:
                        if customer_obj.is_verified:
                            messages.info(request, 'Your profile is already verified.')
                            return redirect('/login')
                        else :
                            customer_obj.is_verified = True
                            customer_obj.save()
                            messages.info(request, 'Your account has been verified. Please Log In')
                            return redirect('../login')
            except Exception as e:
                print(e)
    except Exception as e :
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/verify.html")


def candiateLogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try :
                customer_obj = Candidate.objects.filter(email=email).first()
                if customer_obj is None:
                    messages.info(request, 'User does not exists. Please Signup')
                    return redirect('/signup')
                if not customer_obj.is_verified:
                    messages.info(request, 'This profile is not verified. Please Check your mail.')
                    return redirect('/login')    
                try:
                    user = authenticate(email=email, password=password)
                    if user is  None:
                        messages.info(request, 'Incorrect Password.')
                        return redirect('/login')
                    login(request, user)
                    messages.info(request, 'Successfully logged in')
                    return redirect('/')
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/login.html")

def reviewersignUp(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:
                if Reviewer.objects.filter(email=email).first():
                    messages.info(request, 'This account already exist. Try logging in.')
                    return redirect('/login')
                else:
                    new_customer = Reviewer.objects.create(email=email, name=name)
                    new_customer.set_password(password)
                    thread_obj = send_verification_otp(email)
                    thread_obj.start()
                    new_customer.save()
                    new_customer.save()
                    messages.info(request, 'We have sent you a verification OTP.\nPlease check your mail.')
                    return redirect('../revier-verify')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/reviewe-signup.html")


def reviwerverify(request):
    try:
        if request.method == 'POST':
            otp = request.POST.get('otp')
            try:
                if not cache.get(otp):
                    messages.info(request, 'Invalid OTP')
                else:
                    customer_obj = Reviewer.objects.get(email = cache.get(otp))
                    if customer_obj:
                        if customer_obj.is_verified:
                            messages.info(request, 'Your profile is already verified.')
                            return redirect('../revier-login')
                        else :
                            customer_obj.is_verified = True
                            customer_obj.save()
                            messages.info(request, 'Your account has been verified. Please Log In')
                            return redirect('../revier-login')
            except Exception as e:
                print(e)
    except Exception as e :
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/reviwer-verify.html")


def reviwerlogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try :
                customer_obj = Reviewer.objects.filter(email=email).first()
                if customer_obj is None:
                    messages.info(request, 'User does not exists. Please Signup')
                    return redirect('/signup')
                if not customer_obj.is_verified:
                    messages.info(request, 'This profile is not verified. Please Check your mail.')
                    return redirect('/revier-login')    
                try:
                    user = authenticate(email=email, password=password)
                    if user is  None:
                        messages.info(request, 'Incorrect Password.')
                        return redirect('/revier-login')
                    login(request, user)
                    messages.info(request, 'Successfully logged in')
                    return redirect('/')
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/login.html")


def index(request):
    user_list = Candidate.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'accounts/user_list.html', { 'users': users })


def candid_details(request, blog_id):
    context = {}
    try:
        blog_obj = Candidate.objects.get(id = blog_id)
        context['other_blogs'] =  Candidate.objects.all().exclude(id=blog_id)
        context['blog_obj'] = blog_obj
        context["blog_id"] = blog_id
        context["blog_cmt"] = CommentsModel.objects.filter(From_coment=blog_obj)
    except Exception as e:
        print(e)
    return render(request, "accounts/user_details.html", context)
    

@login_required(login_url='/login/')
def addComment(request, blog_id):
    try:
        if request.method == 'POST':
            CommentsModel.objects.create(
                to_coment = Reviewer.objects.get(email=request.user),
                From_coment =Candidate.objects.get(id = blog_id),
                comment = request.POST.get('cmt'),
                star=int(request.POST.get('star'))
                )
        print(email=request.user)
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))