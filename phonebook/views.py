from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from . import forms
from .models import PhoneBook
from django.urls import reverse_lazy
from django.utils import timezone
import logging
#import weasyprint
from django.http import HttpRequest, HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import generics, viewsets
from . import serializer
from . import permisssion
from rest_framework.exceptions import NotAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


logger = logging.getLogger(__name__)



@method_decorator(csrf_exempt, name="dispatch")
class CreateProfile(LoginRequiredMixin, generic.View):
    def post(self, *args, **kwargs):
        if "recent" not in self.request.session.keys():
            self.request.session["recent"] = {
                # recent : view name
            }
        self.request.session["recent"].update(
            {str(timezone.now()): "CreateProfileView"})
        self.request.session.save()
        form = forms.NewContactForm(data=self.request.POST)
        if form.is_valid():
            form.save(commit=False).user = self.request.user
            contact = form.save()
            logger.info(f"contact {contact.phone_number} created")
            return JsonResponse(
                data={
                    "success": True,
                    "pk": contact.pk,
                    "first_name": contact.first_name,
                    "last_name": contact.last_name,
                    "phone_number": contact.phone_number,
                    "user": contact.user,
                },
                status=201,
            )
        else:
            return JsonResponse(
                data={
                    "success": False,
                },
                status=400,
            )


@method_decorator(csrf_exempt, name="dispatch")
class index(LoginRequiredMixin, generic.ListView):
    """
    Show the add entry form page
    """

    extra_context = {"form": forms.NewContactForm()}
    paginate_by = 2
    template_name = "phonebook/index.html"

    def get(self, *args, **kwargs):
        if "recent" not in self.request.session.keys():
            self.request.session["recent"] = {
                # recent : view name
            }
        self.request.session["recent"][str(timezone.now())] = "indexView"
        self.request.session.save()
        print(settings.STATIC_ROOT)
        print(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
        return super().get(*args, **kwargs)

    def get_queryset(self):
        return PhoneBook.objects.filter(user=self.request.user)


class search(LoginRequiredMixin, generic.TemplateView):
    """
    Show the search form page
    """

    template_name = "phonebook/search.html"


class find(generic.View):
    """
    Finds a phonebook entry
    """

    @method_decorator(login_required)
    def get(self, *args, **kwargs):
        print("test")
        phone_number = self.request.GET.get("phone", None)
        mode = self.request.GET.get("mode", None)
        if not phone_number:
            return JsonResponse({"success": False, "error": "No number specified."}, status=400)
        if mode == "1":
            qs = PhoneBook.objects.filter(
                phone_number=phone_number, user=self.request.user)
        if mode == "2":
            qs = PhoneBook.objects.filter(
                phone_number__startswith=phone_number, user=self.request.user)
        if mode == "3":
            qs = PhoneBook.objects.filter(
                phone_number__endswith=phone_number, user=self.request.user)
        if mode == "4":
            qs = PhoneBook.objects.filter(
                phone_number__contains=phone_number, user=self.request.user)
        if "recent" not in self.request.session.keys():
            self.request.session["recent"] = {
                # recent : view name
            }
        self.request.session["recent"][str(timezone.now())] = "findView"
        self.request.session.save()
        logger.info(f"search for user")
        return JsonResponse({"results": list(qs.values()), "count": qs.count()})



class Register(generic.CreateView):
    form_class = forms.UserRegisterForm
    template_name = "phonebook/register.html"

    def get(self, *args, **kwargs):
        if "recent" not in self.request.session.keys():
            self.request.session["recent"] = {
                # recent : view name
            }
        self.request.session["recent"][str(timezone.now())] = "RegisterView"
        self.request.session.save()
        return super().get(*args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect("login")


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    model = PhoneBook
    form_class = forms.NewContactForm
    template_name = "phonebook/editprofile.html"
    success_url = reverse_lazy("index")

    def get(self, *args, **kwargs):
        if "recent" not in self.request.session.keys():
            self.request.session["recent"] = {
                # recent : view name
            }
        self.request.session["recent"][str(timezone.now())] = "editView"
        self.request.session.save()
        return super().get(*args, **kwargs)


class Recent(LoginRequiredMixin, generic.View):
    template_name = "phonebook/recent.html"

    def get(self, *args, **kwargs):
        print(list(self.request.session.get("recent", []).values())[-5:][::-1])

        return render(
            self.request,
            "phonebook/recent.html",
            context={"recent": list(self.request.session.get(
                "recent", []).values())[-5:][::-1]},
        )


class PrintContact(generic.ListView):
    def get_queryset(self):
        return PhoneBook.objects.filter(user=self.request.user)



class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        mode = request.GET.get("mode", None)
        if mode == '1':  # exact
            return ['=phone_number']
        elif mode == '2':  # starts__with
            return ['^phone_number']
        elif mode == '3':
            return ['$phone_number']
        elif mode == '4':  # contain
            return ['phone_number']
        return super(CustomSearchFilter, self).get_search_fields(view, request)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = PhoneBook.objects.all()
    serializer_class = serializer.PhonebookSerializer
    permission_classes = [permisssion.IsContactOwner]
    filter_backends = [CustomSearchFilter]
    search_fields = ['phone_number']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise NotAuthenticated('you have to login first')
        else:
            return PhoneBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
