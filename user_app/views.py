# user_app/views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.validators import validate_email, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from user_app.models import Profile
from datetime import datetime, date
from django.template.loader import render_to_string
from PIL import Image
import os

class LoginRequiredMixin:
    @classmethod
    def as_view(cls, **kwargs):
        view = super().as_view(**kwargs)
        return login_required(view, login_url='/login/')  # Specify your login URL here

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')  # Redirect to login page if user is not authenticated
        return super().dispatch(request, *args, **kwargs)


class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name, {'success': False})

    def post(self, request):
        success = False
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.POST.get("email")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        phone = request.POST.get("phone")
        date_of_birth_str = request.POST.get("date_of_birth")

        # Validate form data
        if not all([username, password, confirm_password, email, firstname, lastname, phone, date_of_birth_str]):
            messages.warning(request, 'Please fill in complete information')
        else:
            if len(username) < 5 or len(username) > 20:
                messages.warning(request, 'Username must be between 5 and 20 characters long')
            elif len(password) < 8 or len(password) > 20:
                messages.warning(request, 'Password must be between 8 and 20 characters long')
            else:
                try:
                    validate_email(email)

                    if password != confirm_password:
                        messages.warning(request, 'Password and Confirm Password do not match')
                    else:
                        if User.objects.filter(username=username).exists():
                            messages.warning(request, 'Username already registered')
                        elif User.objects.filter(email=email).exists():
                            messages.warning(request, 'Email already registered')
                        else:
                            try:
                                date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
                                if RegisterView.calculate_age(date_of_birth) < 11:
                                    messages.warning(request, 'You must be at least 11 years old to register')
                                else:
                                    user = User.objects.create_user(
                                        username=username,
                                        password=password,
                                        email=email,
                                        first_name=firstname,
                                        last_name=lastname
                                    )
                                    profile, created = Profile.objects.get_or_create(user=user)
                                    profile.phone_number = phone
                                    profile.date_of_birth = date_of_birth
                                    profile.save()

                                    self.send_registration_confirmation_email(request, email)

                                    messages.success(request, 'Created successfully')
                                    success = True
                            except ValueError:
                                messages.warning(request, 'Invalid date format')
                except ValidationError:
                    messages.warning(request, 'Invalid email address')

        return render(request, self.template_name, {'success': success})

    @staticmethod
    def calculate_age(birth_date):
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def send_registration_confirmation_email(self, request, email):
        subject = 'Registration Confirmation'
        message = render_to_string('email/email_template.html')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        html_message = render_to_string('email/email_template.html')

        try:
            send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=False)
            messages.success(request, 'Registration email sent successfully')
            return True
        except BadHeaderError:
            messages.error(request, 'Invalid header found in email')
            return False
        except Exception as e:
            messages.error(request, f'Failed to send registration email: {str(e)}')
            return False


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not all([username, password]):
            messages.warning(request, 'Please fill in complete information')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            try:
                user = User.objects.get(username=username)
                messages.warning(request, 'Incorrect password')
            except User.DoesNotExist:
                messages.warning(request, 'Account not found')

            return redirect('/login/')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login/')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=request.user)
            return redirect('edit_profile')

        return render(request, self.template_name, {'profile': profile})


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'edit_profile.html'

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect('/')

        return render(request, self.template_name, {'profile': profile})

    def post(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect('/')

        profile.bio = request.POST.get('bio')
        profile.phone_number = request.POST.get('phone_number')

        date_of_birth_str = request.POST.get('date_of_birth')
        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
                if RegisterView.calculate_age(date_of_birth) < 11:
                    messages.warning(request, 'You must be at least 11 years old to register')
                    return redirect('edit_profile')
                profile.date_of_birth = date_of_birth
            except ValueError:
                messages.warning(request, 'Invalid date format')
                return redirect('edit_profile')

        if request.FILES.get('profile_image'):
            profile_image = request.FILES['profile_image']

            # Check if the uploaded image is not in WebP format
            try:
                image = Image.open(profile_image)
                if image.format.upper() not in ['JPEG', 'JPG', 'PNG', 'GIF']:
                    converted_image = image.convert("RGB")
                    profile_image.name = f'{profile.user.username}_profile_image.webp'  # Rename the image file
                    converted_image.save(profile_image, 'WEBP')
            except Exception as e:
                messages.error(request, f'Failed to convert image to WebP: {str(e)}')
                return redirect('edit_profile')

            if profile.profile_image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, str(profile.profile_image))
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            profile.profile_image = profile_image

        profile.save()

        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('profile')


class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'change_password.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, 'Current password is incorrect')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match')
        elif len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters long')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('profile')

        return render(request, self.template_name)



'''@login_required
@csrf_protect
def contact_support(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        subject = request.POST.get('subject', '')  # Get the selected subject

        # Validate the message and subject
        if not message or not subject:
            return HttpResponseForbidden('Please provide both a message and a subject before sending.')

        # Additional security check if the user is authenticated
        if request.user.is_authenticated:
            from_email = request.user.email
            user_email = request.user.email
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            user_email = 'N/A'

        # Concatenate subject with prefix
        full_subject = f'Support Request: {subject}'

        # Set the support email address from settings
        to_email = [settings.SUPPORT_EMAIL]

        # Render HTML email template with the message
        html_message = render_to_string('email/support_request_template.html', {'message': message, 'user_email': user_email})

        try:
            # Send the email
            send_mail(full_subject, message, from_email, to_email, html_message=html_message, fail_silently=False)
            messages.success(request, 'Your support request has been sent successfully.')
            return redirect('profile')  # Redirect to profile page after sending the email
        except BadHeaderError:
            return HttpResponseForbidden('Invalid header found.')
        except Exception as e:
            messages.error(request, f'An error occurred while sending the support request: {e}')
            return redirect('profile')  # Redirect to profile page if an error occurs
    else:
        return HttpResponseForbidden('Invalid request method.')  # Return an error response if request method is not POST'''

'''@login_required
def notification_settings(request):
    profile = request.user.profile  # Get the user's profile
    if request.method == 'POST':
        receive_notification = request.POST.get('receive_notification', False)
        
        # Convert the string value to a boolean
        receive_notification = receive_notification == 'on'

        profile.receive_notification = receive_notification
        profile.save()

        if receive_notification:
            messages.success(request, 'Notifications are now turned on.')
        else:
            messages.success(request, 'Notifications are now turned off.')

        return redirect('profile')
    else:
        return render(request, 'notification_settings.html', {'profile': profile})
'''