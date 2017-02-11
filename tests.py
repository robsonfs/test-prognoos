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
