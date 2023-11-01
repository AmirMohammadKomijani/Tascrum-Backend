from django.urls import path
from . import views
## when we use ModelViewSet we should implement urls with routers
from rest_framework_nested import routers as nested
from rest_framework import routers 


nestedRouter = nested.DefaultRouter()
router = routers.SimpleRouter()

router.register('profile',views.MemberProfileView,basename='profile')
router.register('workspace',views.WorkspaceView,basename='workspace')
router.register('crworkspace',views.CreateWorkspaceView,basename='crworkspace')
router.register('board',views.BoardView,basename='board')
router.register('board-bgimage',views.BoardImageView,basename='board-bgimage')
router.register('crboard',views.CreateBoardView,basename='crboard')
router.register('board-member',views.BoardMembersView,basename='board-member')
router.register('list',views.ListView,basename='list')
router.register('crlist',views.CreateListView,basename='crlist')
router.register('card',views.CardView,basename='card')
router.register('assign',views.CardAssignmentView,basename='assign')
router.register('crcard',views.CreateCardView,basename='crcard')
router.register('invite',views.InviteMemberView,basename='invite')
router.register('user-search',views.FindUserView,basename='user-search')
router.register('home',views.HomeAccountView,basename='home')
router.register('change',views.ChangePasswordView,basename='change')
# router.register('test',views.WorkspaceRoleView,basename='test')

urlpatterns = router.urls