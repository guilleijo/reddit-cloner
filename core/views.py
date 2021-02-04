from django.views import generic, View
from django.shortcuts import render

from .reddit import Reddit, RedditException
from .forms import ContactForm
from .utils import send_contact_email


class LandingPageView(View):
    template_name = "landing.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            send_contact_email(form.cleaned_data)
            context = {
                "success": "Message sent!",
                "message": "Thanks for reaching out.",
                "button": "Go back",
            }
            return render(request, "core/success.html", context)

        return render(request, self.template_name, {"form": form, "scroll": True})


class Step1View(generic.TemplateView):
    template_name = "core/step_1.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reddit = Reddit()
        reddit_url = reddit.get_reddit_url("step-1")

        context["reddit_url"] = reddit_url
        context["request"] = self.request
        return context


def step_4(request):
    state = request.GET.get("state")
    subreddits = state.split("-")

    reddit = Reddit()
    reddit.subscribe_to_subreddits(subreddits)

    context = {
        "success": "Success!",
        "message": "You have been subscribed to your old subreddits.",
        "button": " Done!",
    }

    return render(request, "core/success.html", context)


def reddit_callback(request):
    error = request.GET.get("error")
    if error is not None:
        return render(request, "error.html", {"error": error})

    code = request.GET.get("code")
    state = request.GET.get("state")

    reddit = Reddit()
    try:
        error = reddit.authorize_user(code)
    except RedditException as e:
        return render(request, "error.html", {"error": e})

    if state == "step-1":
        subreddits = reddit.get_subreddits_list()
        reddit_url = reddit.get_reddit_url(subreddits, format_state=True)
        template_name = "core/step_2.html"
        context = {
            "subreddits": subreddits,
            "reddit_url": reddit_url,
        }
    else:
        subreddits = state.split("-")
        template_name = "core/step_3.html"
        context = {
            "subreddits": subreddits,
            "code": code,
            "state": state,
        }

    return render(request, template_name, context)
