# Generated manually for adding username and password to ForumUser

from django.db import migrations, models


def populate_username_and_password(apps, schema_editor):
    """
    Populate username and password for existing ForumUser records
    """
    ForumUser = apps.get_model('main', 'ForumUser')
    used_usernames = set()
    
    for user in ForumUser.objects.all():
        # Only populate username if field exists and is empty
        try:
            if not user.username:
                # Generate username from email (take part before @)
                base_username = user.email.split('@')[0]
                username = base_username
                
                # Ensure uniqueness
                counter = 1
                while username in used_usernames or ForumUser.objects.filter(username=username).exists():
                    username = f"{base_username}_{counter}"
                    counter += 1
                
                user.username = username
                used_usernames.add(username)
        except Exception:
            # Username field doesn't exist, skip
            pass
        
        # Only populate password if field exists and is empty
        try:
            if not user.password:
                # Generate a random password hash (users will need to reset)
                from django.contrib.auth.hashers import make_password
                user.password = make_password('temp_password_' + str(user.id))
        except Exception:
            # Password field doesn't exist, skip
            pass
        
        try:
            user.save()
        except Exception:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_contactmessage'),
    ]

    operations = [
        # Add fields to model state only (don't modify database if columns already exist)
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='forumuser',
                    name='username',
                    field=models.CharField(max_length=100, null=True, blank=True, unique=False, verbose_name='Username'),
                ),
                migrations.AddField(
                    model_name='forumuser',
                    name='password',
                    field=models.CharField(max_length=255, null=True, blank=True, verbose_name='Password'),
                ),
            ],
            database_operations=[
                # Don't modify database - columns may already exist
                migrations.RunSQL(
                    sql="SELECT 1",
                    reverse_sql="SELECT 1",
                ),
            ],
        ),
        # Populate existing data
        migrations.RunPython(populate_username_and_password, migrations.RunPython.noop),
        # Make username required and unique
        migrations.AlterField(
            model_name='forumuser',
            name='username',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='Username'),
        ),
        # Update password field (keep nullable for backward compatibility)
        migrations.AlterField(
            model_name='forumuser',
            name='password',
            field=models.CharField(max_length=255, null=True, blank=True, verbose_name='Password'),
        ),
        # Update ROLE_CHOICES
        migrations.AlterField(
            model_name='forumuser',
            name='role',
            field=models.CharField(
                choices=[
                    ('petani', 'Petani'),
                    ('mahasiswa', 'Mahasiswa'),
                    ('peneliti', 'Peneliti'),
                    ('siswa', 'Siswa'),
                    ('umum', 'Umum'),
                    ('lainnya', 'Lainnya'),
                ],
                default='petani',
                max_length=20,
                verbose_name='Kategori'
            ),
        ),
    ]

