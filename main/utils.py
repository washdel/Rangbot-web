"""
Utility functions untuk sistem admin
"""

from django.utils import timezone
from .models import PurchaseOrder, RangBotDevice


def generate_member_id():
    """
    Generate Member ID dengan format: MBR-YYYY-NNNNN
    Contoh: MBR-2025-00492
    """
    year = timezone.now().year
    
    # Cari Member ID terakhir yang sudah dibuat
    last_order = PurchaseOrder.objects.filter(
        member_id__isnull=False,
        member_id__startswith=f'MBR-{year}'
    ).order_by('-id').first()
    
    if last_order and last_order.member_id:
        # Extract number from last Member ID
        try:
            last_num = int(last_order.member_id.split('-')[-1])
            new_num = last_num + 1
        except (ValueError, IndexError):
            new_num = 1
    else:
        new_num = 1
    
    return f"MBR-{year}-{str(new_num).zfill(5)}"


def generate_serial_number(sequence):
    """
    Generate Serial Number dengan format: RBT-SN-01-XXXXX
    Contoh: RBT-SN-01-88401, RBT-SN-01-88402, ...
    
    Args:
        sequence: Nomor urut (1, 2, 3, ...)
    
    Returns:
        Serial number string
    """
    base_num = 88400  # Starting number
    serial_num = base_num + sequence
    return f"RBT-SN-01-{serial_num}"


def get_next_serial_sequence():
    """
    Mendapatkan sequence number berikutnya untuk serial number
    Berdasarkan serial number terakhir yang ada
    """
    last_device = RangBotDevice.objects.order_by('-id').first()
    
    if last_device and last_device.serial_number:
        try:
            # Extract number from serial number (format: RBT-SN-01-88401)
            parts = last_device.serial_number.split('-')
            if len(parts) >= 4:
                last_num = int(parts[-1])
                base_num = 88400
                sequence = last_num - base_num + 1
                return sequence
        except (ValueError, IndexError):
            pass
    
    return 1

