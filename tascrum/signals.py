from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member,BurndownChart,MemberBoardRole

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_for_new_user(sender, **kwargs):
  if kwargs['created']:
    Member.objects.create(user=kwargs['instance'])

@receiver(post_save, sender=MemberBoardRole)
def update_burndown_chart(sender, instance, created, **kwargs):
    if created:
        dates = instance.board.burndown_charts.values_list('date', flat=True).distinct()
        for date in dates:
            BurndownChart.objects.create(board=instance.board, member=instance.member, date=date, done=0, estimate=0)