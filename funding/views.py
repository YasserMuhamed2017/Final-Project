from decimal import Decimal
import re
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.db.models import Q
from django.db.models import Avg

@csrf_exempt
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return JsonResponse({'message': 'Account deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Create your views here.
def index(request):
    projects = Project.objects.all()
    images = {project.id: CampaignImage.objects.filter(campaign=project) for project in projects}
    return render(request, 'funding/index.html', {'projects': projects, 'images': images})

def homepage(request):
    top_projects = (
        Project.objects.filter(end_time__gt=timezone.now())  
        .annotate(avg_rating=Avg('ratings__value')) 
        .order_by('-avg_rating')[:5]
    )
    latest_projects = Project.objects.order_by('-start_time')[:5]
    categories = Category.objects.all()
    return render(request, 'funding/homepage.html', {'top_projects': top_projects, 'latest_projects': latest_projects, 'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    projects = category.projects.all()
    return render(request, 'funding/detail.html', {
        'category': category,
        'projects': projects
    })

def search_projects(request):
    query = request.GET.get('q', '')
    projects = Project.objects.filter(
        Q(title__icontains=query)
    ).distinct() if query else []
    
    return render(request, 'funding/search_results.html', {
        'projects': projects,
        'query': query
    })

def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    images = CampaignImage.objects.filter(campaign=project)
    comments = project.comments.all().order_by('-created_at')
    can_cancel = project.current_amount < (Decimal('0.25') * project.total_target)
    average_rating = project.average_rating()
    # Fetch similar projects based on tags
    project_tags = project.tags.split(',')  # Split tags into a list
    similar_projects = Project.objects.filter(
        Q(tags__icontains=project_tags[0]),
        ~Q(id=project.id)  # Exclude the current project
    ).distinct()[:4]  # Limit to 4 projects

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            return redirect('project_detail', project_id=project_id)
    else:
        form = CommentForm()
        
    return render(request, 'funding/project_detail.html', {
        'project': project,
        'images': images,
        'comments': comments,
        'form': form,
        'can_cancel': can_cancel,
        'average_rating': average_rating,
        'similar_projects': similar_projects, 
        })

def project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save() 
            for img in images:
                CampaignImage.objects.create(campaign=project, image=img)

            return redirect('home')
        else:
            print(form.errors)
    else:
        form = ProjectForm()
    
    return render(request, 'funding/project.html', {'form': form})


def donate(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.project = project
            donation.user = request.user
            donation.save()

            # Update project's current amount
            project.current_amount += donation.amount
            project.save()
            return redirect('project_detail', project_id=project.id) 
    else:
        form = DonationForm()
    
    return render(request, 'funding/donate.html', {
        'form': form,
        'project': project
    })


@login_required
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.reported:
        messages.info(request, 'This comment has already been reported.')
    else:
        comment.reported = True
        comment.save()
        messages.success(request, 'Comment reported successfully.')
    
    return redirect('project_detail', project_id=comment.project.id)

@login_required
def report_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.reported:
        messages.info(request, 'This project has already been reported.')
    else:
        project.reported = True
        project.save()
        messages.success(request, 'Project reported successfully.')

    return redirect('project_detail', project_id=project.id)

@login_required
def rate_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        value = int(request.POST.get('rating', None))
        print(f"Rating value received: {value}")
    
        # Check if the user has already rated the project
        rating, created = Rating.objects.get_or_create(project=project, user=request.user)
        rating.value = value
        rating.save()
        if created:
            messages.success(request, 'Thank you for rating this project!')
        else:
            messages.success(request, 'Your rating has been updated.')
    return redirect('project_detail', project_id=project.id)

@login_required
def cancel_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Ensure the logged-in user is the project creator
    if request.user != project.user:
        messages.error(request, "You are not authorized to cancel this project.")
        return redirect('project_detail', project_id=project.id)

    # Check if the project can be canceled
    if project.can_be_cancelled():
        project.cancelled = True
        project.save()
        messages.success(request, "The project has been canceled successfully.")
    else:
        messages.error(request, "The project cannot be canceled as donations exceed 25% of the target.")

    return redirect('project_detail', project_id=project.id)

def register(request):
    errors = {}
    data = {}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name'] 
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone = request.POST['phone']
        picture = request.FILES.get('picture')

        if not first_name:
            errors['first_name'] = "First name is required."
        else:
            data['first_name'] = first_name
        
        if not last_name:
            errors['last_name'] = "Last name is required."
        else:
            data['last_name'] = last_name

        if not email:
            errors['email'] = "Email is required."
        elif "@" not in email or "." not in email:
            errors['email'] = "Enter a valid email address."
        elif UserProfile.objects.filter(email=email).exists():
            errors['email'] = "Email already exists."
        else:
            data['email'] = email

        if not password:
            errors['password'] = "Password is required."
        else:
            data['password'] = password
        
        if not confirm_password:
            errors['confirm_password'] = "Confirm password is required."
        elif confirm_password != password:
            errors['confirm_password'] = "Passwords do not match."
        else:
            data['confirm_password'] = confirm_password

        egyptian_phone_pattern = r"^01[0125]\d{8}$"
        
        check_phone_number = UserProfile.objects.filter(phone=phone).exists()

        if not phone:
            errors['phone'] = "Phone is required."
        elif not re.match(egyptian_phone_pattern, phone):
            errors['phone'] = "Enter a valid phone number. Must be Egyptian phone number"
        elif check_phone_number:
            errors['phone'] = "Phone number already exists."
        else:
            data['phone'] = phone

        if not picture:
            errors['picture'] = "Profile picture is required."
        else:
            data['picture'] = picture

        print(picture)
        if errors:
            return render(request, 'funding/register.html', {'errors': errors, 'data': data})
        else:
            user = UserProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password), 
            phone=phone,
            picture=picture
        )
            
            # Generate token for email verification
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Build activation URL
            domain = get_current_site(request).domain
            activation_link = f"http://{domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"

            # Send activation email
            send_mail(
                "Activate Your Account",
                f"Click the link to activate your account: {activation_link}",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('login')
    return render(request, 'funding/register.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True  # Activate user
        user.save()
        return HttpResponse("Your account has been activated! You can now log in.")
    else:
        return HttpResponse("Activation link is invalid or expired.")
    
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user (use `email` if AUTH_USER_MODEL is set)
        user = authenticate(request, username=email, password=password)
        print(user)

        email_exist = UserProfile.objects.filter(email=email, is_active=False).exists()

        if user is not None and user.is_active:
                auth_login(request, user)
                return redirect('/')  # Redirect to home page after login
        elif email_exist:
            return render(request, "funding/login.html", 
            {
                "message": "Your account is not activated. Please check your email."
            })
        else:
            return render(request, "funding/login.html", 
            {
                "message": "Invalid email or password."
            })

    return render(request, 'funding/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

def profile(request):
    projects = Project.objects.filter(user=request.user)
    donations = Donation.objects.filter(user=request.user)
    return render(request, 'funding/profile.html', {'projects': projects, 'donations': donations})

def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        picture = request.FILES.get('picture')
        user = UserProfile.objects.get(email=email)
        facebook_profile = request.POST.get('facebook_profile')
        birth_date = request.POST.get('birth_date')
        country = request.POST.get('country')

        if facebook_profile:
            user.facebook_profile = facebook_profile
        if birth_date:
            user.birth_date = birth_date
        if country:
            user.country = country
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if phone:
            user.phone = phone
        if picture:
            user.picture = picture
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    return render(request, 'funding/update_profile.html')

def delete_profile(request):
    if request.method == 'POST':
        user = UserProfile.objects.get(email=request.user.email)
        user.delete()
        messages.success(request, "Profile deleted successfully.")
        return redirect('register')
    return render(request, 'funding/login.html')