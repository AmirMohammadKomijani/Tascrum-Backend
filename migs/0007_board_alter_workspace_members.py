from django.db import migrations,models

def copy_data_from_old_to_new(apps, schema_editor):
    Workspace = apps.get_model('tascrum', 'Workspace')
    WorkspaceMember = apps.get_model('tascrum', 'WorkspaceMember')

    for workspace in Workspace.objects.all():
        for member in workspace.members.all():
            WorkspaceMember.objects.create(workspace=workspace, member=member)

class Migration(migrations.Migration):
    dependencies = [
        ('tascrum', '0006_alter_workspace_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkspaceMember',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('workspace', models.ForeignKey(to='tascrum.Workspace', on_delete=models.CASCADE)),
                ('member', models.ForeignKey(to='tascrum.Member', on_delete=models.CASCADE)),
                ('role', models.CharField(max_length=50)),
            ],
        ),
        migrations.RunPython(copy_data_from_old_to_new),
    ]
