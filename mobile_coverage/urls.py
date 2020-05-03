from django.urls import path

from mobile_coverage.views import MobileCoverageView

urlpatterns = [
    path("coverage", MobileCoverageView.as_view()),
]
