import time
from typing import Dict, Any
class LocalThreatCache:
    def __init__(self):
        self.blacklist_vpas = {'scammer@okaxis', 'fakecbi@ybl', 'digitalarrest@paytm'}
    def verify_vpa(self, vpa: str, amount: float, mcc: str) -> Dict[str, Any]:
        vpa_clean = vpa.lower().strip()
        if vpa_clean in self.blacklist_vpas:
            return {'safe': False, 'reason': 'VPA found in known cybercrime blacklist.'}
        is_zero_day = vpa_clean.startswith('new') or 'fraud' in vpa_clean
        suspicious_mcc = mcc in ['9999', '6012', '7995']
        high_velocity = amount > 50000
        is_threat = is_zero_day or suspicious_mcc or (high_velocity and vpa_clean.endswith('@ybl'))
        return {
            'vpa': vpa_clean,
            'safe': not is_threat,
            'risk_level': 'HIGH' if is_threat else 'LOW',
            'heuristics': {
                'zero_day_vpa': is_zero_day,
                'suspicious_mcc': suspicious_mcc,
                'high_amount_velocity': high_velocity
            },
            'recommendation': 'Block transaction immediately and report to 1930.' if is_threat else 'Transaction appears normal.'
        }
