from ia.utils.feriados_utils import eh_feriado
from ia.utils.pagamentos_utils import (
    perfil_do_dia,
    obter_fase_financeira,
    datas_pagamento_clt,
    eh_feriado_sjc,
)
from ia.utils.textos_utils import normalizar_setor
from ia.utils.datas_utils import (
    converter_data_relativa,
    converter_periodo
)
from ia.utils.clima import obter_clima_para_previsao