from rest_framework import routers
from vendor import views

router = routers.SimpleRouter()

router.register("popsicles", views.PopsicleViewSet)
router.register("machines", views.MachineViewSet)
router.register("locations", views.LocationViewSet)
router.register("transactions", views.TransactionViewSet)
router.register("users", views.UserViewSet)
