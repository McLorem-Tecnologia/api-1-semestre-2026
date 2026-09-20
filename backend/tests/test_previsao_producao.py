import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ia.config import _eh_pedido_de_producao, _eh_pedido_historico_producao
from ia.tools.utils import historico_producao_por_setor, previsao_producao_por_setor


class TestPrevisaoProducao(unittest.TestCase):
    def test_previsao_por_setor_retorna_resumo_valido(self):
        resultado = previsao_producao_por_setor("30/09/2026")

        self.assertIsInstance(resultado, str)
        self.assertIn("Setor", resultado)
        self.assertIn("Total estimado", resultado)
        self.assertGreater(len(resultado.splitlines()), 5)

    def test_consulta_historica_nao_eh_previsao(self):
        frase = "Quero saber os produtos que foram feitos totais no setor da peixaria"
        self.assertFalse(_eh_pedido_de_producao(frase))
        self.assertTrue(_eh_pedido_historico_producao(frase))

    def test_historico_por_setor_retorna_totais_reais(self):
        resultado = historico_producao_por_setor("Peixaria")
        self.assertIsInstance(resultado, str)
        self.assertIn("Histórico de produção", resultado)
        self.assertIn("Total histórico", resultado)


if __name__ == "__main__":
    unittest.main()
