from rest_framework import routers
from vendor import views

router = routers.SimpleRouter()

router.register("popsicles", views.PopsicleViewSet)
router.register("machines", views.MachineViewSet)
router.register("stock/removal", views.PopsicleRemovalViewSet)
router.register("stock/entry", views.PopsicleEntryViewSet)
router.register("setup", views.SetupViewSet)
router.register("purchases", views.PurchaseViewSet)
router.register("users", views.UserViewSet)
