from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages

# from django.urls import reverse_lazy
from django.views.generic import View
from .forms import RegistrationForm, LoginForm

# from django.template.loader import render_to_string
from .utils import account_activation_token

# for sending email faster
import threading

# importing app models
from user_profiles.models import Profile


# getting the user model
User = get_user_model()


# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email) -> None:
        self.email = email
        threading.Thread.__init__(self)

    def run(self) -> None:
        self.email.send()


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        context = {"form": form}
        return render(request, "accounts/signup.html", context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        context = {"form": form}

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            # print(f"{email} & {password}")

            if not User.objects.filter(email=email).exists():
                return self._create_new_user(
                    request, first_name, last_name, email, password
                )
        return render(request, "accounts/signup.html", context)

    def _create_new_user(self, request, first_name, last_name, email, password):
        """
        Create a new user if user is not registered.
        """
        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, email=email
        )
        user.set_password(password)
        user.save()

        # creating and saving profile instance
        profile = Profile.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            user=user,
            email=user.email,
        )
        profile.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        current_site = get_current_site(request)

        # link or path is used for specifying which url will be used
        # after the user clicks the activation link
        link = reverse(
            "activate",
            kwargs={"uidb64": uid, "token": token},
        )
        activate_url = f"http://{current_site.domain}{link}"

        email_body = (
            "Hi "
            + user.email
            + f", We just need to verify your email address before you can access {current_site.domain}\n"
            + f"Verify your email address: {activate_url} \n"
            + "Thanks! – The Out of Business team"
        )

        email_subject = "Activate your account"
        email = EmailMessage(
            email_subject,
            email_body,
            # sender
            "forangela100@gmail.com",
            # receivers
            # we can send mail to multiple recipients
            # that's why using a list of email addresses
            [email],
        )
        # email.send(fail_silently=False)

        EmailThread(email).start()

        messages.info(request, "Please verify your email address.")
        return redirect("login")
        # return render(request, "accounts/activation_notice.html")


def verification(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        User.DoesNotExist,
        DjangoUnicodeDecodeError,
    ):
        user = None

    if user is None or not account_activation_token.check_token(user, token):
        # invalid link
        return render(request, "accounts/invalid.html")
    user.profile.email_verified = True
    user.profile.save()
    return redirect("login")


def login_view(request):  # sourcery skip: extract-method
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect("projects")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            if not user:
                messages.error(request, "Email or Password is invalid.")
                context = {"form": form}
                return render(request, "accounts/login.html", context)

            if not user.profile.email_verified:
                messages.info(request, "Please verify your email address")
                return redirect("login")

            if user.last_login is None:
                messages.info(request, "You have been logged in.")
                login(request, user)
                return redirect("edit_user_account")

            login(request, user)
            messages.info(request, "You have been logged in.")
            return redirect("projects")

        else:
            messages.error(request, "Email or Password is invalid.")

    context = {"form": form}

    return render(request, "accounts/login.html", context)


def logout_request(request):
    logout(request)
    return redirect("projects")
