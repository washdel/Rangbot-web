"""
Script untuk update test devices dengan konsep baru RangBot
"""

from main.models import RangBotDevice

# Update device 1
device1 = RangBotDevice.objects.filter(serial_number='RB-DEV-001').first()
if device1:
    device1.device_name = 'RangBot 1'
    device1.covered_blocks = 'A, B'
    device1.save()
    print(f'✓ Device 1 updated: {device1.device_name} - {device1.covered_blocks}')

# Update device 2
device2 = RangBotDevice.objects.filter(serial_number='RB-DEV-002').first()
if device2:
    device2.device_name = 'RangBot 2'
    device2.covered_blocks = 'C, D'
    device2.save()
    print(f'✓ Device 2 updated: {device2.device_name} - {device2.covered_blocks}')

print('✓ All devices updated!')

