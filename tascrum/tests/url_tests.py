from django.test import SimpleTestCase
from django.urls import reverse,resolve
from tascrum.views import MemberProfileView,WorkspaceView,CreateWorkspaceView,BoardView,CreateBoardView,ListView,CreateListView,\
    CardView,CreateCardView,HomeAccountView


class TestUrls(SimpleTestCase):

    def test_member_profile(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class,MemberProfileView)

