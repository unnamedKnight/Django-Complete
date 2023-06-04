from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# from django.urls import reverse_lazy
from django.views.generic import View
from .forms import RegistrationForm, LoginFrom

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
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            print(f"{email} & {password}")

            if not User.objects.filter(email=email).exists():
                return self._create_new_user(email, password, request)
        return render(request, "accounts/signup.html", context)

    def _create_new_user(self, email, password, request):
        """
        Create a new user if user is not registered.
        """
        user = User.objects.create_user(email=email)
        user.set_password(password)
        user.save()

        # creating and saving profile instance
        profile = Profile.objects.create(user=user, email=user.email)
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

        return redirect("projects")


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
    user.is_active = True
    user.save()
    return redirect("projects")



def login_view(request):
    form = LoginFrom()
    context = {"form": form}

    return render(request, "accounts/login.html", context)