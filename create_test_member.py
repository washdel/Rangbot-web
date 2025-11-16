"""
Script untuk membuat test member dan device untuk testing dashboard
Jalankan dengan: python manage.py shell < create_test_member.py
atau: python manage.py shell
lalu copy-paste isi script ini
"""

from main.models import Member, RangBotDevice, Notification, DetectionHistory
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta

# Create test member
member, created = Member.objects.get_or_create(
    member_id='RB-00001',
    defaults={
        'username': 'testuser',
        'full_name': 'Test User',
        'email': 'test@rangbot.id',
        'phone': '081234567890',
        'password': make_password('test1234'),
    }
)

if created:
    print(f"✓ Member created: {member.member_id} - {member.full_name}")
    print(f"  Username: {member.username}")
    print(f"  Password: test1234")
else:
    print(f"✓ Member already exists: {member.member_id}")

# Create test devices
device1, created1 = RangBotDevice.objects.get_or_create(
    serial_number='RB-DEV-001',
    defaults={
        'member': member,
        'device_name': 'RangBot Blok A',
        'status': 'active',
        'is_active': True,
        'last_data_update': timezone.now() - timedelta(minutes=5),
    }
)

device2, created2 = RangBotDevice.objects.get_or_create(
    serial_number='RB-DEV-002',
    defaults={
        'member': member,
        'device_name': 'RangBot Blok B',
        'status': 'offline',
        'is_active': True,
        'last_data_update': timezone.now() - timedelta(hours=2),
    }
)

if created1:
    print(f"✓ Device created: {device1.device_name}")
if created2:
    print(f"✓ Device created: {device2.device_name}")

# Create test notifications
Notification.objects.get_or_create(
    member=member,
    notification_type='device_added',
    title='Perangkat Ditambahkan',
    message=f'Perangkat {device1.device_name} berhasil ditambahkan.',
    defaults={'is_read': False}
)

Notification.objects.get_or_create(
    member=member,
    notification_type='detection_new',
    title='Deteksi Baru',
    message='Terdeteksi penyakit pada tanaman stroberi di Blok A.',
    defaults={'is_read': False}
)

print(f"\n✓ Test data created successfully!")
print(f"\nLogin dengan:")
print(f"  Username/Email: {member.username} atau {member.email}")
print(f"  ID Member: {member.member_id}")
print(f"  Password: test1234")

