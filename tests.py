from unittest import TestCase
from subscriptions import Subscription, Subscriptions

# Criar estrutura de dados para armazenar dados das assinaturas
# Ler arquivo de dados e armazenar na estrutura criada
# Calcular o total de assinaturas para um dado mês
# Determinar todos os meses nos quais houve cancelamentos
# Para cada mês, retornar uma tupla com as seguintes informações:
# (mes_ano, novos_usuarios, total_usuarios, usuarios_ativos, cancelamentos)

class TestSubscriptions(TestCase):

    def test_add_increase_subscritions_list(self):
        sub = Subscription('2015-10-10', '4242', '2015-10-5', 'CANCELADA', 0, 11)
        subs = Subscriptions()
        initial_len = len(subs)
        subs.add(sub)
        final_len = len(subs)
        self.assertEqual(initial_len, final_len + 1)
