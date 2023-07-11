from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
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

        url = form.cleaned_data.get("url")
        obj = Url.objects.create(url=url)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url()}
        )

class RedirectView(View):
    def get(self, request, *args, **kwargs):
        hashed_url = self.kwargs.get('hashed_url')
        url = Url.objects.get(hashed_url=hashed_url)
        return redirect(url.url)