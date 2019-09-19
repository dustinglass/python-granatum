from time import time

from dateutil.relativedelta import relativedelta
from lxml.html import fromstring
import requests

from granatum import utils


class Granatum(object):
    '''Used for accessing Granatum.'''

    def __init__(self, email, password):
        '''Creates a logged in Granatum session.

        Parameters
        ----------
        email : str
            E-mail
        password : str
            Senha
        '''
        self.filters = {}
        self._login(email, password)

    def _login(self, email, password):
        '''Executes login workflow.

        Parameters
        ----------
        email : str
            E-mail
        password : str
            Senha
        '''
        self.session = requests.Session()
        response_1 = self.session.get('https://contas.granatum.com.br/')
        self.session.post(
            'https://contas.granatum.com.br/users/sign_in',
            data={
                'authenticity_token': utils.parse_authenticity_token(response_1.text),
                'commit': 'Acessar',
                'user[email]': email,
                'user[password]': password,
                'utf8': '✓',
            },
        )
        self.session.get('https://contas.granatum.com.br/')
        r = self.session.get('https://secure.granatum.com.br/oauth/granatum')
        print(r.text)
        response_2 = self.session.get(
            'https://contas.granatum.com.br/oauth/authorize?client_id=b9e18dcd8bfab8e34fe98f36d8fc8d68637b983bcb63f1bb1f06c1dbd829c276&redirect_uri=https%3A%2F%2Fsecure.granatum.com.br%2Foauth%2Fgranatum%2Fint_callback&scope=public&response_type=code'
        )
        self.session.post(
            'https://secure.granatum.com.br/oauth/callback',
            data={'opauth': utils.parse_opauth(response_2.text)},
        )

    def exportar(self, end_date, start_date, filters={}):
        '''Download the file downloaded after clicking "Exportar" in the "LANCAMENTOS"
        tab.

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
        file object
        '''
        if not bool(self.filters):
            self._attr_filters()
        self._post_filter(utils.build_form(end_date, start_date, filters))
        self._get_carrega_balanco()
        self._post_ajax()
        response = self.session.get(
            'https://secure.granatum.com.br/a/59361/admin/lancamentos/exportar_lancamentos'
        )
        return response.content

    def _attr_filters(self):
        response = self.session.get(
            'https://secure.granatum.com.br/a/59361/admin/lancamentos'
        )
        self.filters['conta_id'] = utils.parse_conta_ids(response.text)
        self.filters['tipo'] = utils.parse_tipos(response.text)
        self.filters['categoria_id'] = utils.parse_categoria_ids(response.text)

    def _post_filter(self, data):
        '''Filter the result set on the website.

        Parameters
        ----------
        data : dict
            Form data
        '''
        self.session.post(
            'https://secure.granatum.com.br/a/59361/admin/filtros/filtrar/filter_name:Lancamentos/',
            data=data,
        )

    def _get_carrega_balanco(self):
        '''Send a necessary server request.'''
        self.session.get(
            'https://secure.granatum.com.br/a/59361/admin/contas/carrega_balanco',
            data={'_': int(time() * 1000.0)},
        )

    def _post_ajax(self):
        '''Send a necessary server request.'''
        self.session.post(
            'https://secure.granatum.com.br/a/59361/admin/lancamentos/index/page:1?ajax'
        )
