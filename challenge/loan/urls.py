from rest_framework import routers

from challenge.loan.views import CreateLoanViewSet

router = routers.SimpleRouter()
router.register('loan', CreateLoanViewSet)
urlpatterns = router.urls

app_name = 'loan'
