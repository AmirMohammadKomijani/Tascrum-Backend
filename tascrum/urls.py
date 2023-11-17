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
router.register('starred-boards',views.BoardStarView,basename='starred-boards')
router.register('star',views.BoardStarUpdate,basename='star')
router.register('board-invitation-link',views.BoardInvitationLinkView,basename='board-invitation-link')
router.register('crboard',views.CreateBoardView,basename='crboard')
router.register('recentlyviewed',views.BoardRecentlyViewedView,basename='recentlyviewed')
router.register('board-member',views.BoardMembersView,basename='board-member')
router.register('list',views.ListView,basename='list')
router.register('crlist',views.CreateListView,basename='crlist')
router.register('card',views.CardView,basename='card')
router.register('critem',views.CreateItemView,basename='critem')
router.register('checklist',views.CardChecklistView,basename='checklist')
router.register('crchecklist',views.CreateChecklistView,basename='crchecklist')
router.register('crlabel',views.CreateLabelView,basename='crlabel')
router.register('label',views.LabelBoardView,basename='label')
router.register('assign',views.CardAssignmentView,basename='assign')
router.register('crcard',views.CreateCardView,basename='crcard')
router.register('invite',views.InviteMemberView,basename='invite')
router.register('user-search',views.FindUserView,basename='user-search')
router.register('home',views.HomeAccountView,basename='home')
router.register('change',views.ChangePasswordView,basename='change')
router.register('dnd',views.Internal_DndView,basename='dnd')
# router.register('burndown',views.CreateBurndownChartView,basename='burndown')
# router.register('test',views.WorkspaceRoleView,basename='test')

urlpatterns = router.urls