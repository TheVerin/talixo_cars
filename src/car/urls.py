from rest_framework.routers import SimpleRouter

from car.views import CarViewSet

router = SimpleRouter()
router.register("", CarViewSet)
urlpatterns = router.urls
