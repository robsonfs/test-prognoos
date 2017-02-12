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
        self._months = []

    def __len__(self):
        return len(self._subs)

    def add(self, sub):
        if sub in self._subs:
            return False
        self._subs.append(sub)
        return True

    def get_total_subs(self, period=None):
        if period:
            pass
            # retorna a quantidade de usuários ativos no mês anterior
        return len(self._subs)

    def get_total_cancelations(self, period=None):
        cancelations = [x for x in self._subs if x.date_canceled]
        if period:
            filtered = filter(
                lambda x: self.get_period(x.date_canceled) == period, cancelations
            )
            return len([x for x in filtered])
        return len(cancelations)

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

    def load_months(self):
        months = set()
        for sub in self._subs:
            if sub.date_canceled:
                months.add(self.get_period(sub.date_canceled))
            months.add(self.get_period(sub.payment_date))
        months = list(months)
        months.sort()
        self._months.clear()
        self._months.extend(months)
        return len(months)
