from datetime import date, timedelta


def obter_periodo_mes_anterior():
    """
    Retorna o primeiro e o último dia do mês anterior.

    Exemplo:
        ("01/06/2025", "30/06/2025")
    """

    hoje = date.today()

    primeiro_dia_mes_atual = hoje.replace(day=1)

    ultimo_dia_mes_anterior = primeiro_dia_mes_atual - timedelta(days=1)

    primeiro_dia_mes_anterior = ultimo_dia_mes_anterior.replace(day=1)

    data_inicial = primeiro_dia_mes_anterior.strftime("%d/%m/%Y")
    data_final = ultimo_dia_mes_anterior.strftime("%d/%m/%Y")

    return data_inicial, data_final