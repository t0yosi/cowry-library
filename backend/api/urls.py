from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BookViewSet, BorrowRecordViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'borrowed', BorrowRecordViewSet)

urlpatterns = router.urls
