from collections import namedtuple

Subscription = namedtuple(
    'Subscription',
    [
        'date_canceled', 'id_subs_details', 'payment_date', 'status',
        'is_active', 'reason_canceled'
    ]
)

class Subscriptions:

    def __init__(self):
        self._subs = []

    def __len__(self):
        return len(self._subs)

    def add(self, sub):
        if sub in self._subs:
            return False
        self._subs.append(sub)
        return True
