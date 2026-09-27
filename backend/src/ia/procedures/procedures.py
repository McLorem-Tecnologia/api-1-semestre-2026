#Atenção esse é o arquivo que é para ser importado para utilizar as procedures
# ex:
#from ia.procedures import procedures

import ia.procedures.vendas_procedures as vendas
import ia.procedures.regras_procedures as regras
import ia.procedures.produtos_procedures as produtos  
import ia.procedures.ingredientes_procedures as ingredientes
import ia.procedures.descarte_procedures as descarte
import ia.procedures.producao_procedures as producao

#como acessar?
# main.py ou telegram_bot.py ou tools/qualquer_arquivo_dspy.py
# import procedures

#Exemplos
# # Você acessa a função chamando o arquivo central > apelido do módulo > função 
# procedures.vendas.buscar_por_nome_produto()
# procedures.vendas.buscar_por_periodo()
# procedures.regras.obter_dia("07/09/2026")
# procedures.regras.obter_mes(2026, 9)
# procedures.produtos.buscar_por_setor("Padaria")

