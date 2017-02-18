import csv
from collections import namedtuple

Subscription = namedtuple(
    'Subscription',
    [
        'date_canceled', 'id_subs_details', 'payment_date', 'status',
        'is_active', 'reason_canceled'
    ]
)

class Subscriptions:

    def __init__(self, loader):
        self._subs = []
        self._months = []
        self.loader = loader

    def __len__(self):
        return len(self._subs)

    def add(self, sub):
        if sub.__class__.__name__ != 'Subscription':
            raise ValueError("Invalid argument")

        if sub in self._subs:
            return False
        self._subs.append(sub)
        return True

    def get_total_subs(self, period):
        if period == self._months[0]:
            return self.get_new(period)
        index = self._months.index(period)
        prev_month = self._months[index - 1]
        return (self.get_total_subs(prev_month) + self.get_new(period)) -\
        self.get_total_cancelations(prev_month)

    def get_total_cancelations(self, period=None):
        cancelations = [x for x in self._subs if x.date_canceled]
        if period:
            filtered = filter(
                lambda x: self.get_period(x.date_canceled) == period, cancelations
            )
            return len([x for x in filtered])
        return len(cancelations)

    def get_total_actives(self, period):
        return self.get_total_subs(period) - self.get_total_cancelations(period)

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

    def get_new(self, month):
        return len(
            [x for x in self._subs if self.get_period(x.payment_date) == month]
        )

    def populate_from_csv(self, csv_path):
        lines = self.loader.loader_from_csv(csv_path)
        for line in lines:
            self.add(Subscription(*line))
        self.load_months()
        return len(lines)

class Loader:

    def loader_from_csv(self, csv_path, mode='r'):
        rows = []
        with open(csv_path, mode) as dataset:
            dataset_reader = csv.DictReader(dataset)
            for row in dataset_reader:
                rows.append(
                    [
                        row['date_canceled'], row['id_subs_details'],
                        row['payment_date'], row['status'], row['is_active'],
                        row['reason_canceled']
                    ]
                )
        return rows

class Results:

    def __init__(self, subscriptions):
        self.subscriptions = subscriptions

    def show_results(self, data_provider):
        self.subscriptions.populate_from_csv(data_provider)
        print("Ano-Mês\tNovos\tTotal\tAtivos\tCancelamentos")
        for month in self.subscriptions._months:
            print(
                "%s\t%s\t%s\t%s\t%s"%(
                    month, self.subscriptions.get_new(month),
                    self.subscriptions.get_total_subs(month),
                    self.subscriptions.get_total_actives(month),
                    self.subscriptions.get_total_cancelations(month)
                )
            )
