import unittest
from unittest import mock
from subscriptions import Subscription, Subscriptions, Loader

# Criar estrutura de dados para armazenar dados das assinaturas [Done]
# Ler arquivo de dados e armazenar na estrutura criada
# Calcular o total de assinaturas para um dado mês
# Determinar todos os meses nos quais houve cancelamentos
# Para cada mês, retornar uma tupla com as seguintes informações:
# (mes_ano, novos_usuarios, total_usuarios, usuarios_ativos, cancelamentos)

class TestSubscriptions(unittest.TestCase):

    def setUp(self):
        self.sub = Subscription('2015-10-10', '4242', '2015-10-05', 'CANCELADA', '0', '11')
        loader = Loader()
        self.subs = Subscriptions(loader)

    def test_subs_object_has_a_loader(self):
        self.assertIsInstance(self.subs.loader, Loader)

    def test_add_increases_subscritions_list(self):
        initial_len = len(self.subs)
        self.subs.add(self.sub)
        final_len = len(self.subs)
        self.assertEqual(initial_len, final_len - 1)

    def test_not_add_duplicated_elements(self):
        self.subs.add(self.sub)
        self.assertFalse(self.subs.add(self.sub))

    def test_get_total_subs(self):
        sub1 = Subscription('2015-10-10', '4242', '2015-10-05', 'CANCELADA', '0', '11')
        sub2 = Subscription('2015-10-10', '4243', '2015-10-05', 'CANCELADA', '0', '11')
        sub3 = Subscription('2015-10-10', '4244', '2015-10-05', 'CANCELADA', '0', '11')

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.assertEqual(self.subs.get_total_subs(), 2)
        self.subs.add(sub3)
        self.assertEqual(self.subs.get_total_subs(), 3)

    def test_get_total_cancelations(self):
        sub1 = Subscription('', '4242', '2015-10-5', 'ATIVA', '1', '6')
        sub2 = Subscription('2015-10-10', '4243', '2015-10-05', 'CANCELADA', '0', '11')
        sub3 = Subscription('2015-10-11', '4244', '2015-10-05', 'CANCELADA', '0', '13')

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        cancelations = self.subs.get_total_cancelations()
        self.assertTrue(cancelations == 2)

    def test_get_total_active(self):
        sub1 = Subscription('', '4242', '2015-10-05', 'ATIVA', '1', '6')
        sub2 = Subscription('', '4243', '2015-10-05', 'ATIVA', '1', '6')
        sub3 = Subscription('2015-10-11', '4244', '2015-10-05', 'CANCELADA', '0', '13')

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        active_subs = self.subs.get_total_actives()
        self.assertEqual(active_subs, 2)

    def test_get_total_active_by_month(self):
        sub1 = Subscription('', '4242', '2015-10-30 01:44:28', 'ATIVA', '1', '6')
        sub2 = Subscription('', '4243', '2015-12-15 07:30:01', 'ATIVA', '1', '6')
        sub3 = Subscription('', '4244', '2015-10-30 19:04:28', 'ATIVA', '1', '6')

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        active_subs = self.subs.get_total_actives('2015-10')
        self.assertTrue(active_subs == 2)

    def test_get_period(self):
        sub1 = Subscription('', '4242', '2015-10-30 01:44:28', 'ATIVA', '1', '6')
        period = self.subs.get_period(sub1.payment_date)
        self.assertEqual(period, '2015-10')
        sub2 = Subscription(
            '2015-12-15 07:30:01', '4243', '2015-12-15 07:30:01', 'ATIVA', '1', '6'
        )
        period = self.subs.get_period(sub2.date_canceled)
        self.assertEqual(period, '2015-12')

    def test_get_total_cancelations_by_month(self):
        sub1 = Subscription('2015-10-30 01:44:28', '4242', '2015-10-04 01:44:28', 'CANCELADA', '0', '11')
        sub2 = Subscription('2015-12-16 01:44:28', '4243', '2015-12-15 07:30:01', 'CANCELADA', '0', '11')
        sub3 = Subscription('2015-10-25 01:44:28', '4244', '2015-10-17 09:55:28', 'CANCELADA', '0', '11')

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        cancelations = self.subs.get_total_cancelations('2015-10')
        self.assertTrue(cancelations == 2)

    def test_get_total_subs_by_month(self):
        subs = [
            Subscription('', '4242', '2015-10-30 01:44:28', 'ATIVA', '1', '6'),
            Subscription('', '4243', '2015-12-15 07:30:01', 'ATIVA', '1', '6'),
            Subscription('', '4244', '2015-10-29 19:04:28', 'ATIVA', '1', '6'),
            Subscription('', '4245', '2015-11-30 19:04:28', 'ATIVA', '1', '6'),
            Subscription('', '4248', '2015-11-27 19:04:28', 'ATIVA', '1', '6'),
            Subscription('', '4246', '2016-01-15 16:04:28', 'ATIVA', '1', '6'),
            Subscription('', '4247', '2016-02-13 18:33:28', 'ATIVA', '1', '6'),
            Subscription('2016-02-15 18:33:28', '4249', '2016-02-13 18:33:28', 'CANCELADA', '0', '13'),
            Subscription('2015-10-15 18:33:28', '4250', '2015-10-13 08:24:00', 'CANCELADA', '0', '13')
        ]

        for sub in subs:
            self.subs.add(sub)

        subs_on_october = self.subs.get_total_subs('2015-10')
        self.assertEqual(subs_on_october, 3)

    def test_load_months(self):
        sub1 = Subscription('2016-03-30 01:44:28', '4242', '2015-02-04 01:44:28', 'CANCELADA', '0', '11')
        sub2 = Subscription('2016-01-16 01:44:28', '4243', '2015-12-15 07:30:01', 'CANCELADA', '0', '11')
        sub3 = Subscription('2015-11-25 01:44:28', '4244', '2015-10-17 09:55:28', 'CANCELADA', '0', '11')

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        months_count = self.subs.load_months()
        self.assertEqual(months_count, 6)
        self.assertEqual(months_count, len(self.subs._months))

    def test_load_months_clear(self):
        self.subs._months.extend(['apenas', 'um', 'teste'])
        sub1 = Subscription('2016-03-30 01:44:28', '4242', '2015-02-04 01:44:28', 'CANCELADA', '0', '11')
        self.subs.add(sub1)
        self.subs.load_months()

        self.assertEqual(['2015-02', '2016-03'], self.subs._months)

    def test_get_new(self):
        subs = [
            Subscription('2016-03-30 01:44:28', '4242', '2015-02-04 01:44:28', 'CANCELADA', '0', '11'),
            Subscription('2016-01-16 01:44:28', '4243', '2015-02-15 07:30:01', 'CANCELADA', '0', '11'),
            Subscription('', '4244', '2015-10-01 09:55:28', 'ATIVA', '1', '11'),
            Subscription('', '4245', '2015-10-17 09:55:28', 'ATIVA', '1', '11'),
            Subscription('', '4246', '2015-10-31 09:55:28', 'ATIVA', '1', '11')
        ]

        for sub in subs:
            self.subs.add(sub)

        amount_2015_02 = self.subs.get_new('2015-02')
        self.assertEqual(amount_2015_02, 2)

        amount_2015_10 = self.subs.get_new('2015-10')
        self.assertEqual(amount_2015_10, 3)

class TestLoader(unittest.TestCase):

    @mock.patch('subscriptions.open')
    def test_loader_from_csv(self, mock_open):
        loader = Loader()
        data = loader.loader_from_csv('any path')
        mock_open.assert_called_with('any path', 'r')
        self.assertIsInstance(data, list)
