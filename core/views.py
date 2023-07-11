from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from core.models import Url
from django.urls import reverse
from core.forms import UrlForm, PinForm

class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data["url"]
        hashed_url = form.cleaned_data.get("hashed_url")
        existing_url = Url.objects.filter(hashed_url=hashed_url).first()

        if hashed_url and existing_url:
            form.add_error("hashed_url", "This custom hash is already taken!")
            return render(request, self.template_name, {"form": form})

        obj = Url.objects.create(url=url, hashed_url=hashed_url)
        if obj:
            if hashed_url:
                pin = obj.pin
            else:
                pin = ""

            # Check if a PIN needs to be generated and saved
            if not hashed_url and not pin:
                obj.pin = ""  # Set pin to an empty string

            obj.save()

            return render(
                request,
                self.template_name,
                {"form": form, "short_url": obj.get_full_short_url(), "pin": pin},
            )

        return render(request, self.template_name, {"form": form})


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        hashed_url = self.kwargs.get('hashed_url')
        try:
            if hashed_url:
                url = Url.objects.get(hashed_url=hashed_url)
            else:
                short_url = request.path[1:]  # Remove the leading slash
                url = Url.objects.get(hashed_url=short_url)

            return redirect(url.url)
        except Url.DoesNotExist:
            raise Http404("URL does not exist")

class RetrieveView(View):
    template_name = "retrieve.html"

    def get(self, request, *args, **kwargs):
        form = PinForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = PinForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data["pin"]
            url = Url.objects.filter(pin=pin).first()
            if url:
                return render(request, self.template_name, {"url": url})
            else:
                form.add_error("pin", "Invalid PIN")
        return render(request, self.template_name, {"form": form})


class EditView(View):
    template_name = "edit.html"

    def get(self, request, *args, **kwargs):
        hashed_url = kwargs["hashed_url"]
        url = get_object_or_404(Url, hashed_url=hashed_url)
        form = UrlForm(initial={"url": url.url})
        return render(request, self.template_name, {"form": form, "hashed_url": hashed_url})

    def post(self, request, *args, **kwargs):
        hashed_url = kwargs["hashed_url"]
        url = get_object_or_404(Url, hashed_url=hashed_url)
        form = UrlForm(request.POST)
        if form.is_valid():
            url.url = form.cleaned_data["url"]
            url.save()
            return redirect("home_page")
        return render(request, self.template_name, {"form": form, "hashed_url": hashed_url})


class URLListView(View):
    template_name = "url_list.html"

    def get(self, request, *args, **kwargs):
        urls = Url.objects.all()
        return render(request, self.template_name, {"urls": urls})
