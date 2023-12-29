from django.urls import path
from . import views
## when we use ModelViewSet we should implement urls with routers
from rest_framework_nested import routers as nested
from rest_framework import routers 


nestedRouter = nested.DefaultRouter()
router = routers.DefaultRouter()

### account info urls
router.register('profile',views.MemberProfileView,basename='profile')
router.register('home',views.HomeAccountView,basename='home')
router.register('change',views.ChangePasswordView,basename='change')
router.register('card-filter',views.CardFilterView,basename='card-filter')

### workspace urls
router.register('workspace',views.WorkspaceView,basename='workspace')
router.register('crworkspace',views.CreateWorkspaceView,basename='crworkspace')
router.register('workspace-members',views.WorkspaceMembersView,basename='workspace-members')

# nestedRouter.register(r'workspaces', views.WorkspaceView, basename='workspaces')
# workspace_router = nested.NestedSimpleRouter(nestedRouter, r'workspaces', lookup='workspace')
# workspace_router.register(r'members', views.WorkspaceMembersView, basename='members')

### board urls
router.register('board',views.BoardViewSet,basename='board')
router.register('board-bgimage',views.BoardImageView,basename='board-bgimage')
router.register('boards-has-start',views.BoardStarView,basename='boards-has-start')
router.register('board-star-update',views.BoardStarUpdate,basename='board-star-update')
router.register('board-invitation-link',views.BoardInvitationLinkView,basename='board-invitation-link')
router.register('starred-boards',views.BoardStarView,basename='starred-boards')
router.register('star',views.BoardStarUpdate,basename='star')
# router.register('board-invitation-link',views.BoardInvitationLinkView,basename='board-invitation-link')
router.register('crboard',views.CreateBoardView,basename='crboard')
router.register('recentlyviewed',views.BoardRecentlyViewedView,basename='recentlyviewed')
router.register('board-labels',views.LabelBoardView,basename='board-labels')
# router.register('meeting',views.MeetingView,basename='meeting')

nestedRouter.register(r'boards', views.BoardViewSet, basename='boards')
meeting_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
meeting_router.register(r'meeting', views.CreateMeetingView, basename='meetings')
# meeting_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
# meeting_router.register(r'meetings', views.MeetingView, basename='meetings')

filter_board_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
filter_board_router.register(r'filter-board', views.BoardfilterView, basename='filter-board')

search_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
search_router.register(r'card-search', views.CardSearchViewSet, basename='card-search')


### invite member to board
router.register('board-member',views.BoardMembersView,basename='board-member')
router.register('invite',views.InviteMemberView,basename='invite')
router.register('user-search',views.FindUserView,basename='user-search')

### list urls
router.register('list',views.ListView,basename='list')
router.register('crlist',views.CreateListView,basename='crlist')


### card details urls
router.register('card',views.CardView,basename='card')
router.register('crcard',views.CreateCardView,basename='crcard')
router.register('checklist',views.CardChecklistView,basename='checklist')
router.register('crchecklist',views.CreateChecklistView,basename='crchecklist')
router.register('critem',views.CreateItemView,basename='critem')
router.register('crlabel',views.CreateLabelView,basename='crlabel')
router.register('crcard-labels',views.LabelCardAssignView,basename='crcard-labels')
router.register('card-labels',views.LabelCardView,basename='card-labels')
router.register('assign',views.CardAssignmentView,basename='assign')
router.register('dnd',views.Internal_DndView,basename='dnd')

### timeline urls
router.register('list-tl',views.ListTimelineView,basename='list-tl')
router.register('member-tl',views.MemberTimelineView,basename='member-tl')
router.register('label-tl',views.LabelTimelineView,basename='label-tl')
timeline1_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
timeline1_router.register(r'start-tl', views.TimelineStartPeriodView, basename='start-tl')
timeline2_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
timeline2_router.register(r'due-tl', views.TimelineDuePeriodView, basename='due-tl')

### burndown
router.register('burndown-chart', views.BurndownChartViewSet, basename='burndown-chart')
router.register('burndown-chart-estimate', views.BurndownChartEstimateViewSet, basename='burndown-chart-estimate')
router.register(r'burndown-chart-sum/(?P<board_id>\d+)', views.BurndownChartSumViewSet, basename='burndown-chart-sum')
router.register(r'burndown-chart-create', views.BurndownCreateView, basename='burndown-chart-create')

###Calender
# router.register('calender',views.CalenderView,basename='calender')
calender_router = nested.NestedSimpleRouter(nestedRouter, r'boards', lookup='board')
calender_router.register(r'calender', views.CalenderView, basename='calender')

###Chatbot
router.register('csvbuild',views.CardCSVViewSet,basename='csvbuild')
router.register('chatbot',views.ChatbotAPIView,basename='chatbot')


urlpatterns = router.urls + nestedRouter.urls + calender_router.urls + meeting_router.urls + search_router.urls + filter_board_router.urls + timeline1_router.urls + timeline2_router.urls


