from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from core.models import Url
from core.forms import UrlForm



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
        else:
            obj = Url.objects.create(url=url, hashed_url=hashed_url)
            if obj:
                return render(
                    request,
                    self.template_name,
                    {"form": form, "short_url": obj.get_full_short_url()},
                )

        return render(request, self.template_name, {"form": form})

class RedirectView(View):
    def get(self, request, *args, **kwargs):
        hashed_url = self.kwargs.get('hashed_url')
        url = Url.objects.get(hashed_url=hashed_url)
        return redirect(url.url)