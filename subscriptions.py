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

    def get_total_subs(self):
        return len(self._subs)

    def get_total_cancelations(self):
        return len([x for x in self._subs if x.date_canceled])

    def get_total_actives(self, period=None):
        actives = [x for x in self._subs if x.is_active]
        if period:
            filtered = filter(
                lambda x: self.get_period(x.payment_date) == period, actives
            )
            return len([x for x in filtered])
        return len(actives)

    def get_period(self, date_string):
        return date_string.split(' ')[0][:-3]
