from django.urls import include, path

v1 = []

urlpatterns = [
    path("v1/", include((v1, "v1"), namespace="v1")),
]
