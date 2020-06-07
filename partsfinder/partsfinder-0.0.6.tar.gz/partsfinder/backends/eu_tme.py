#!/usr/bin/env python3

import structlog
import requests
from requests_toolbelt import sessions
from urllib.parse import urljoin
import js2py
from bs4 import BeautifulSoup
from partsfinder.datamodel import ParamSpace, Parameter, Value
import re
import pint
from collections import defaultdict
from money import Money

class EuTmeSession(sessions.BaseUrlSession):
    def __init__(self, **kwargs):
        self.log = structlog.get_logger()
        self.baseurl = kwargs.get('baseurl', 'https://www.tme.eu/')
        self.lang = kwargs.get('lang', 'en')
        self._cats = None
        super(self.__class__, self).__init__( base_url=urljoin(self.baseurl, '/{}/'.format(self.lang)) )

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        # The TME backend is unauthenticated so it doesn't need to shutdown a 
        # session.
        pass

    @property
    def categories(self):
        if self._cats is None:
            # Fetch categories
            cat_js = self.get('catalogue/categories.js').text
            ctx = js2py.EvalJs({})
            ctx.execute(cat_js)
            self._cats = ctx.categories.to_dict()
            self.log.info('categories loaded', cat_count=len(self._cats))

        return self._cats

    def build_parameter_space(self, cat):
        
        log = self.log.bind(cat_id=cat['id'], cat_name=cat['meta']['name'])
        cat_url = cat['meta']['url']

        log.info('fetching parameters', url=cat_url)

        cat_resp = self.get(cat_url)
        soup = BeautifulSoup(cat_resp.text, features="html.parser")

        #
        # TODO: Get a list of fields which can be used for sorting from
        #     <div class="products-sort__container" id="productsSort">
        #

        param_space = ParamSpace()

        param_selector = soup.find('select', id='select_id_parameter')
        if param_selector is None: # No parameters defined for this category
            return param_space

        # Build a list of all parameters for this category
        param_units = {}
        for param_unit_option in param_selector.find_all('option'):
            param_id = param_unit_option['value']
            
            # Chop off part counts and units
            txt = param_unit_option.get_text()
            m = re.match('(.+)\s+\[[0-9]+\](\s+\[.+\])?', txt)
            param_name = m.group(1)

            param = Parameter(id=param_id, name=param_name)
            param_space[param_id] = param

            log = log.bind(p_id=param_id, p_name=param_name)
            log.debug('new parameter')

            # Get the specified parameter unit
            param.unit = None
            m = re.match('.+\s+\[[0-9]+\]\s+\[(.+)\]', param_unit_option.get_text())
            if m:
                try:
                    param.unit = param_space.ureg.parse_expression(m.group(1))
                except pint.errors.UndefinedUnitError:
                    log.error("cannot parse unit description", description=m.group(1))

            log.debug('specified unit', specified_unit=param.unit)
        
        # Fetch the value space for each parameter
        for param_div in soup.find('div', id='parameters').find_all('div', class_="parameter_"):
            param_id = param_div.find('input', attrs={'name': 'not_hidden[]'})['value']
            
            #print("-----")
            #print('PARAM id={} title={}'.format(param_id, param_name))
            param = param_space[param_id]

            # First gather only the raw value texts
            values_div = param_div.find('div', class_='parameter_box').find('div', id='select_list_{}'.format(param.id))
            for value_label in values_div.find_all('label'):
                value_id = value_label.find('input', type='checkbox')['value']

                # Remove the parts count from the value text
                value_text = re.sub('\[\d+\]$', '', value_label.get_text(strip=True)).replace(',','.')

                log.debug("value", v_id=value_id, v_raw=value_text)
                param.values[value_id] = Value(id=value_id, raw=value_text, ureg=param_space.ureg)

            if param.unit is not None:
                if all( map(lambda value: param.validate_value_text(value.raw), param.values.values()) ):
                    for v in param.values.values():
                        v.unit = param.unit

            log.info('parameter analyzed', v_count=len(param.values))

        log.info('param space built', p_count=len(param_space))
        return param_space

    def lookup_parts(self, cat, param_space, **kwargs):
        """Lookup a list of parts based on a constrained parameter space."""
        log = self.log.bind(cat_id=cat['id'])

        # Now that all the constraints have been applied perform the lookup
        mapped_params = ';'.join( [ p.queryp for p in param_space.constrained_params])

        log.info('looking up parts', mapped_params=mapped_params, url=cat['meta']['url'])

        lookup_params = {
            'mapped_params': mapped_params,
        }
        if 'item_limit' in kwargs:
            lookup_params.update(dict(limit=kwargs['item_limit']))

        lookup_params.update({
            's_field': '1000014',
            's_order': 'asc',
        })

        parts_resp = self.get(cat['meta']['url'], params=lookup_params)
        soup = BeautifulSoup(parts_resp.text, features="html.parser")

        parts_found = {}
        product_rows = soup.select('tr.product-row')
        log.info('parsing part list', part_count=len(product_rows))

        for row in product_rows:
            manuf_a = row.find('a', attrs={'data-gtm-event-action': "producer_link"})
            manuf_name = manuf_a.get_text(strip=True)
            data_product_id = manuf_a['data-product-id']

            symbol = row.find('input', attrs={'name': 'symbols[]'}).get('value')
            description = row.find('span', class_='product-row__symbol-row').find_next('div', class_='product-row__name-cell-sub-row').get_text(strip=True)
            moq = int(row.find(class_='M_{}'.format(data_product_id)).get_text(strip=True))
            multiplier = int(row.find(class_='W_{}'.format(data_product_id)).get_text(strip=True))

            parts_found[symbol] = dict(manuf_name=manuf_name, symbol=symbol, moq=moq, multiplier=multiplier,
                    description=description, selectors={
                        'pricing': 'div.C_{}'.format(data_product_id),
                        'stock': 'div.S_{}'.format(data_product_id)
                    })

        return parts_found
    
    def lookup_pricing(self, parts):
        """Lookup pricing and stock levels."""
        log = self.log

        symbol_list = [ part['symbol'] for part in parts.values() ]

        log.info('fetching pricing information', symbol_count=len(symbol_list))

        pricing_resp = self.post('/_ajax/Catalogue/_getStocks_catalogue.js', 
            data={ 'symbols[]': symbol_list, 'onlyStocks': 0, 'currency': 'USD' },
            headers={ 'X-Requested-With': 'XMLHttpRequest' }
        )

        #print("---")
        #print("Pricing data")
        #print(pricing_resp.text)

        class Blackhole(object):

            def __getattr__(self, prop):
                return Blackhole()

            def __call__(self, *args):
                return Blackhole()


        class HtmlCapture(object):
            def __init__(self, snippets, key):
                self.snippets = snippets
                self.key = key

            def __getattr__(self, prop):
                if prop == "html":
                    return lambda html: self.snippets.update({self.key: html})
                else:
                    return Blackhole()


        class jQueryInterceptHtml(object):
            def __init__(self, **kwargs):
                self.selectors = kwargs.get('selectors', [])
                self.snippets = kwargs['snippets']

            def __call__(self, selector):
                if selector in self.selectors:
                    return HtmlCapture(self.snippets, selector)
                else:
                    return Blackhole()

        selectors = []
        selectors.extend([ p['selectors']['stock'] for p in parts.values() ])
        selectors.extend([ p['selectors']['pricing'] for p in parts.values() ])

        snippets = {}
        pricing_data = defaultdict(lambda: dict(pricing=None, stock=None))
        
        log.debug("parsing pricing javascript", selectors=selectors)

        ctx = js2py.EvalJs({ '$': jQueryInterceptHtml(selectors=selectors, snippets=snippets) })
        ctx.execute(pricing_resp.text)

        log.debug("html snippets extracted", snippet_count=len(snippets))
        for part in parts.values():
            selectors = part['selectors']

            pricing_html = snippets.get(selectors['pricing'], None)
            if pricing_html is not None:
                soup = BeautifulSoup(pricing_html, features="html.parser")

                pricing_div = soup.find('div', class_="katalog ceny")
                if pricing_div is None: # Skip if pricing data is not available for this part
                    continue

                # First c-price-table entry is a header, skip it
                pricing_div = pricing_div.find_all('div', class_="c-price-table", recursive=False)[1]

                amount_levels = [ int(div.get_text(strip=True).replace('+','')) for div in pricing_div.find_all('div', class_="prices_range_amount") ]

                # First div is the MOQ levels that we parsed above
                unit_prices = [ Money(amount=div.get_text(strip=True), currency='USD') for div in pricing_div.find_all('div', recursive=False)[1].find_all('div', class_='c-price-table__cell') ]

                pricing = dict(zip(amount_levels, unit_prices))
                pricing_data[part['symbol']]['pricing'] = pricing

                log.debug('found pricing data', symbol=part['symbol'], pricing=pricing)

            stock_html = snippets.get(selectors['stock'], None)
            if stock_html is not None:
                soup = BeautifulSoup(stock_html, features="html.parser")
                stock = int( soup.find(class_='stock_number').get_text(strip=True) )
                pricing_data[part['symbol']]['stock'] = stock

                log.debug('found stock data', symbol=part['symbol'], stock=stock)

        return pricing_data
