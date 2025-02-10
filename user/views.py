from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser 
from .models import CustomUser as User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            
            email_subject = "Account Created Successfully!"
            email_recipient = form.cleaned_data["email"]

            html_message = render_to_string("emails/account-created-successfully-email.html")
            plain_message = strip_tags(html_message)

            messageObj = EmailMultiAlternatives(
                subject=email_subject,
                body=plain_message,
                from_email=None,
                to=[email_recipient]
            )

            messageObj.attach_alternative(html_message, "text/html")
            messageObj.send()

            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})



class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            
            # Authenticate using the custom email backend
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("webpages-home")
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
    else:
        form = LoginForm()
        
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, "profile.html", {"user": request.user, "form": form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'  # Custom template
    email_template_name = 'accounts/password_reset_email.html'  # Email template
    # subject_template_name = 'accounts/password_reset_subject.txt'  # Email subject
    success_url = reverse_lazy('password_reset_done')  # Redirect after form submission

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     email = form.cleaned_data['email']
    #     # send_mail(
    #     #     'Password Reset Request',
    #     #     'Click the link below to reset your password:',
    #     #     'noreply@yourdomain.com',
    #     #     [email],
    #     #     fail_silently=False,
    #     # )
    #     return response

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')  # Redirect after setting a new password
