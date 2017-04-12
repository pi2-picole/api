from rest_framework import routers
from vendor import views

router = routers.SimpleRouter()

router.register("popsicles", views.PopsicleViewSet)
