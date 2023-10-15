from django.urls import path
from . import views
## when we use ModelViewSet we should implement urls with routers
from rest_framework_nested import routers as nested
from rest_framework import routers 


nestedRouter = nested.DefaultRouter()
router = routers.SimpleRouter()

router.register('profile',views.MemberProfileView,basename='profile')
router.register('workspace',views.WorkspaceView,basename='workspace')
router.register('home',views.HomeAccountView,basename='home')
router.register('test',views.WorkspaceRoleView,basename='test')

urlpatterns = router.urls