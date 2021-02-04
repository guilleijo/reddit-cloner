from django.urls import path

from .views import LandingPageView, reddit_callback, Step1View, step_4


urlpatterns = [
    path('', LandingPageView.as_view(), name='landing_page'),
    path('step-1/', Step1View.as_view(), name='step_1'),
    path('step-4/', step_4, name='step_4'),
    path('callback/', reddit_callback, name='callback'),
]
