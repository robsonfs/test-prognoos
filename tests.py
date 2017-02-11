from unittest import TestCase
from subscriptions import Subscription, Subscriptions

# Criar estrutura de dados para armazenar dados das assinaturas [Done]
# Ler arquivo de dados e armazenar na estrutura criada
# Calcular o total de assinaturas para um dado mês
# Determinar todos os meses nos quais houve cancelamentos
# Para cada mês, retornar uma tupla com as seguintes informações:
# (mes_ano, novos_usuarios, total_usuarios, usuarios_ativos, cancelamentos)

class TestSubscriptions(TestCase):

    def setUp(self):
        self.sub = Subscription('2015-10-10', '4242', '2015-10-5', 'CANCELADA', 0, 11)
        self.subs = Subscriptions()

    def test_add_increase_subscritions_list(self):
        initial_len = len(self.subs)
        self.subs.add(self.sub)
        final_len = len(self.subs)
        self.assertEqual(initial_len, final_len - 1)

    def test_not_add_duplicated_elements(self):
        self.subs.add(self.sub)
        self.assertFalse(self.subs.add(self.sub))

    def test_get_total_subs(self):
        sub1 = Subscription('2015-10-10', '4242', '2015-10-5', 'CANCELADA', 0, 11)
        sub2 = Subscription('2015-10-10', '4243', '2015-10-5', 'CANCELADA', 0, 11)
        sub3 = Subscription('2015-10-10', '4244', '2015-10-5', 'CANCELADA', 0, 11)

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.assertTrue(self.subs.get_total_subs() == 2)
        self.subs.add(sub3)
        self.assertTrue(self.subs.get_total_subs() == 3)

    def test_get_total_cancelations(self):
        sub1 = Subscription('', '4242', '2015-10-5', 'ATIVA', 1, 6)
        sub2 = Subscription('2015-10-10', '4243', '2015-10-5', 'CANCELADA', 0, 11)
        sub3 = Subscription('2015-10-11', '4244', '2015-10-5', 'CANCELADA', 0, 13)

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        cancelations = self.subs.get_total_cancelations()
        self.assertTrue(cancelations == 2)

    def test_get_total_active(self):
        sub1 = Subscription('', '4242', '2015-10-5', 'ATIVA', 1, 6)
        sub2 = Subscription('', '4243', '2015-10-5', 'ATIVA', 1, 6)
        sub3 = Subscription('2015-10-11', '4244', '2015-10-5', 'CANCELADA', 0, 13)

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        active_subs = self.subs.get_total_actives()
        self.assertTrue(active_subs == 2)

    def test_get_total_active_by_month(self):
        sub1 = Subscription('', '4242', '2015-10-30 01:44:28', 'ATIVA', 1, 6)
        sub2 = Subscription('', '4243', '2015-12-15 07:30:01', 'ATIVA', 1, 6)
        sub3 = Subscription('', '4244', '2015-10-30 19:04:28', 'ATIVA', 1, 6)

        self.subs.add(sub1)
        self.subs.add(sub2)
        self.subs.add(sub3)

        active_subs = self.subs.get_total_actives('2015-10')
        self.assertTrue(active_subs == 2)

    def test_get_period(self):
        sub1 = Subscription('', '4242', '2015-10-30 01:44:28', 'ATIVA', 1, 6)
        period = self.subs.get_period(sub1.payment_date)
        self.assertEqual(period, '2015-10')
        sub2 = Subscription(
            '2015-12-15 07:30:01', '4243', '2015-12-15 07:30:01', 'ATIVA', 1, 6
        )
        period = self.subs.get_period(sub2.date_canceled)
        self.assertEqual(period, '2015-12')
