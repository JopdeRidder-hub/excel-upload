from rest_framework import routers

from users.viewset import UserViewSet

router = routers.SimpleRouter()
router.register(r"users", UserViewSet)

urlpatterns = router.urls
