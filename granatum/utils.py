from lxml.html import fromstring


def parse_authenticity_token(text):
    return fromstring(text).xpath('//input[@name="authenticity_token"]/@value')[0]


def parse_opauth(text):
    return fromstring(text).xpath('//input[@name="opauth"]/@value')[0]


def parse_conta_ids(text):
    result = {}
    root = fromstring(text)
    for input, label in zip(
        root.xpath('//input[@name="data[Lancamento][conta_id][]"]'),
        root.xpath('//label[@name="data[Lancamento][conta_id][]"]'),
    ):
        if input.xpath('./@name')[0] != 'selectAll':
            result[label.xpath('./text()')[0]] = input.xpath('./@value')[0]
    return result


def parse_tipos(text):
    result = {}
    for label in fromstring(text).xpath(
        '//div[@id="filtro-tipo"]//div[@class="checkbox"]/label'
    ):
        result[label.xpath('./text()')[0]] = label.xpath('./input/@value')[0]
    return result


def parse_categoria_ids(text):
    result = {}
    root = fromstring(text)
    for input, label in zip(
        root.xpath('//input[@name="data[Lancamento][categoria_id][]"]'),
        root.xpath('//label[@name="data[Lancamento][categoria_id][]"]'),
    ):
        result[label.xpath('./text()')[0]] = input.xpath('./@value')[0]
    return result


def build_form(end_date, start_date, filters):
    '''Construct the form data used to filter site results.

    Parameters
    ----------
    end_date : date
        "De"
    start_date : date
        "Ate"
    filters : optional, dict of lists
        Supported keys are "tipo" and "categorias"

    Return
    ------
    list of tuples
    '''
    data = [
        ('_method', 'POST'),
        ('data[Lancamento][regime]', '1'),
        ('data[Lancamento][atalhoCalendario]', 'diario'),
        ('data[Lancamento][startDate]', start_date.strftime('%d/%m/%Y')),
        ('data[Lancamento][endDate]', end_date.strftime('%d/%m/%Y')),
        ('data[Lancamento][conta_id]', ''),
        ('data[Lancamento][centro_custo_lucro_id]', ''),
        ('data[Lancamento][busca]', ''),
        ('data[Lancamento][tipo]', ''),
        ('data[Lancamento][categoria_id]', ''),
        ('data[Lancamento][forma_pagamento_id]', ''),
        ('data[Lancamento][tipo_custo_nivel_producao_id]', ''),
        ('data[Lancamento][tipo_custo_apropriacao_produto_id]', ''),
        ('data[Lancamento][tipo_documento_id]', ''),
        ('data[Lancamento][cliente_id]', ''),
        ('data[Lancamento][fornecedor_id]', ''),
        ('data[Lancamento][tag_id]', ''),
        ('data[Lancamento][wgi_usuario_id]', ''),
    ]
    for key, values in filters.items():
        for value in values:
            data.append(('data[Lancamento][{}][]'.format(key), value))
    return data
