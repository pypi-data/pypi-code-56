# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:30:43 2019

@author: yuanq
"""
import sys
sys.path.append(r'../')
import modUtils3 as util
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Table, Column, String, Integer, BigInteger, ForeignKey, \
                        DateTime, Boolean, Float, create_engine

# Base
Base = declarative_base()

# Associative Tables
email_pricing_request = Table('tbl_email_pricing_requests', Base.metadata,
                              Column('pricing_request_id',
                                     BigInteger, 
                                     ForeignKey('tbl_pricing_requests.pricing_request_id'),
                                     primary_key=True),
                              Column('email_id',
                                     BigInteger, 
                                     ForeignKey('tbl_emails.email_id'),
                                     primary_key=True))
                                         
pricing_request_underlying = Table('tbl_pricing_request_underlyings', Base.metadata,
                                   Column('pricing_request_id',
                                          BigInteger, 
                                          ForeignKey('tbl_pricing_requests.pricing_request_id'),
                                          primary_key=True),
                                   Column('underlying_id',
                                          BigInteger, 
                                          ForeignKey('tbl_underlyings.underlying_id'),
                                          primary_key=True))

class Email(Base):
    __tablename__ = 'tbl_emails'
    email_id = Column(BigInteger, primary_key=True)
    mailbox_address = Column(BigInteger)
    entry_id = Column(String)
    store_id = Column(BigInteger)
    conversation_id = Column(String)
    conversation_index = Column(String)
    conversation_topic = Column(String)
    subject = Column(String)
    from_ = Column('from', String, key='from_')
    to = Column(String)
    cc = Column(String)
    html_body = Column(String)
    sent_on = Column(DateTime)
    received_on = Column(DateTime)
    has_attachment = Column(Boolean)
    pricing_request = relationship('PricingRequest',
                                   secondary=email_pricing_request,
                                   back_populates='email')
        
    def __repr__(self):
        return '<Email(email_id={int_email_id}, mailbox_address={int_mailbox_address}, \
                entry_id={str_entry_id}, store_id={int_store_id}, \
                conversation_id={str_conversation_id}, conversation_index={str_conversation_index}, \
                conversation_topic={str_conversation_topic}, subject={str_subject}, \
                from={str_from}, to={str_to}, cc={str_cc}, html_body={str_html_body}, \
                sent_on={dte_sent_on}, received_on={dte_received_on}, \
                has_attachment={bln_has_attachement})>'.format(int_email_id=self.email_id,
                int_mailbox_address=self.mailbox_address, str_entry_id=self.entry_id,
                int_store_id=self.store_id, str_conversation_id=self.conversation_id,
                str_conversation_index=self.conversation_index, str_conversation_topic=self.conversation_topic,
                str_subject=self.subject, str_from=self.from_, str_to=self.to, 
                str_cc=self.cc, str_html_body=self.html_body, dte_sent_on=self.sent_on,
                dte_received_on=self.received_on, bln_has_attachment=self.has_attachment)

class PricingRequest(Base):
    __tablename__ = 'tbl_pricing_requests'
    pricing_request_id = Column(BigInteger, primary_key=True)
    product_id = Column(Integer, ForeignKey('tbl_product_settings.product_id'))
    product_setting = relationship('ProductSetting', back_populates='pricing_request')
    reference_number = Column(BigInteger)
    issue_delay = Column(Integer)
    tenor = Column(Integer)
    tenor_type_id = Column(Integer, ForeignKey('tbl_tenor_types.tenor_type_id'))
    tenor_type = relationship('TenorType', back_populates='pricing_request')
    currency_id = Column(Integer, ForeignKey('tbl_currencies.currency_id'))
    currency = relationship('Currency', back_populates='pricing_request')
    email = relationship('Email',
                         secondary=email_pricing_request,
                         back_populates='pricing_request')
    underlying = relationship('Underlying',
                              secondary=pricing_request_underlying,
                              back_populates='pricing_request')
    order = relationship('Order', back_populates='pricing_request')
    
    def __repr__(self):
        return '<PricingRequest(pricing_request_id={int_pricing_request_id}, \
                product_id={int_product_id}, reference_number={int_reference_number}, \
                issue_delay={int_issue_delay}, tenor={int_tenor}, tenor_type_id={int_tenor_type_id}, \
                currency_id={int_currency_id})>'.format(int_pricing_request_id=self.pricing_request_id,
                int_product_id=self.product_id, int_reference_number=self.reference_number,
                int_issue_delay=self.issue_delay, int_tenor=self.tenor, int_tenor_type_id=self.tenor_type_id,
                int_currency_id=self.currency_id)
    
#class EmailPricingRequest(Base):
#    __tablename__ = 'tbl_email_pricing_requests'
#    pricing_request_id = Column(BigInteger, 
#                                ForeignKey('tbl_pricing_requests.pricing_request_id'),
#                                primary_key=True)
#    email_id = Column(BigInteger, 
#                      ForeignKey('tbl_emails.email_id'),
#                      primary_key=True)
#    
#    
#    
#    def __repr__(self):
#        return '<EmailPricingRequest(pricing_request_id={int_pricing_request_id}, \
#                email_id={int_email_id})>'.format(int_pricing_request_id=self.pricing_request_id,
#                int_email_id=self.email_id)
        
class Order(Base):
    __tablename__ = 'tbl_orders'
    order_id = Column(BigInteger, primary_key=True)
    notional = Column(Float)
    sales_fee = Column(Float)
    yield_to_client = Column(Float)
    structuring_fee = Column(Float)
    pnl = Column(Float)
    strategy = Column(String)
    trade_number = Column(Integer, unique=True)
    contract_number = Column(Integer)
    package_number = Column(Integer)
    pricing_request_id = Column(BigInteger,ForeignKey('tbl_pricing_requests.pricing_request_id'))
    pricing_request = relationship('PricingRequest', back_populates='order')
    fixing_type_id = Column(Integer, ForeignKey('tbl_fixing_types.fixing_type_id'))
    fixing_type = relationship('FixingType', back_populates='order')
    
    def __repr__(self):
        return '<Order(order_id={int_order_id}, notional={dbl_notional}, \
                sales_fee={dbl_sales_fee}, yield_to_client={dbl_yield_to_client}, \
                structuring_fee={dbl_structuring_fee}, pnl={dbl_pnl}, \
                strategy={str_strategy}, trade_number={int_trade_number}, \
                contract_number={int_contract_number}, package_number={int_package_number}, \
                pricing_request_id={int_pricing_request_id}, fixing_type_id={int_fixing_type_id})>'.format(
                int_order_id=self.order_id, dbl_notional=self.notional, dbl_sales_fee=self.sales_fee,
                dbl_yield_to_client=self.yield_to_client, dbl_structuring_fee=self.structuring_fee,
                dbl_pnl=self.pnl, str_strategy=self.strategy, int_trade_number=self.trade_number,
                int_contract_number=self.contract_number, int_package_number=self.package_number,
                int_pricing_request_id=self.pricing_request_id, int_fixing_type_id=self.fixing_type_id)



class ObservationFrequency(Base):
    __tablename__ = 'tbl_observation_frequencies'
    observation_frequency_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    def __repr__(self):
        return '<ObservationFrequency(observation_frequency_id={int_observation_frequency_id}, \
                name={str_name})>'.format(int_observation_frequency_id=self.observation_frequency_id,
                str_name=self.name)

class UserSetting(Base):
    __tablename__ = 'tbl_user_settings'
    user_id = Column(Integer, primary_key=True)
    email_address = Column(String, unique=True)
    windows_login = Column(String, unique=True)
    group = Column(String)
    salutation = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    has_autopricer_rights = Column(Boolean)
    group_id = Column(BigInteger, ForeignKey('tbl_group_settings.group_id'))
    group_setting = relationship('GroupSetting', back_populates='user_setting')
    
    def __repr__(self):
        return '<UserSetting(user_id={int_user_id}, email_address={str_email_address},\
                windows_login={str_windows_login}, group={str_group}, \
                salutation={str_salutation}, first_name={str_first_name}, \
                middle_name={str_middle_name}, last_name={str_last_name}, \
                has_autopricer_rights = {bln_has_autopricer_rights}, \
                group_id={int_group_id})>'.format(int_user_id=self.user_id,
                str_email_address=self.email_address, str_windows_login=self.windows_login,
                str_group=self.group, str_salutation=self.salutation,
                str_first_name=self.first_name, str_middle_name=self.middle_name,
                str_last_name=self.last_name, bln_has_autopricer_rights=self.has_autopricer_rights,
                int_group_id=self.group_id)

class GroupSetting(Base):
    __tablename__ = 'tbl_group_settings'
    group_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    product = Column(String)
    header_mapping = Column(String)
    salutation = Column(String)
    user_setting = relationship('UserSetting', back_populates='group_setting')
    product_id = Column(BigInteger, ForeignKey('tbl_product_settings.product_id'))
    product_setting = relationship('ProductSetting', back_populates='group_setting')
    
    def __repr__(self):
        return '<GroupSetting(group_id={int_group_id}, name={str_name}, product={str_product}, \
                header_mapping={str_header_mapping}, salutation={str_salutation}, \
                product_id={int_product_id})>'.format(int_group_id=self.group_id, 
                str_name=self.name, str_product=self.product, str_header_mapping=self.header_mapping,
                str_salutation=self.salutation, int_product_id=self.product_id)
        
class ProductSetting(Base):
    __tablename__ = 'tbl_product_settings'
    product_id = Column(Integer, primary_key=True)
    external_name = Column(String)
    internal_name = Column(String)
    internal_header = Column(String)
    pricing_request = relationship('PricingRequest', back_populates='product_setting')
    group_setting = relationship('GroupSetting', back_populates='product_setting')
    
    def __repr__(self):
        return '<ProductSetting(product_id={int_product_id}, \
                external_name={str_external_name}, internal_name={str_internal_name}, \
                internal_header={str_internal_header})>'.format(int_product_id=self.product_id,
                str_external_name=self.external_name, str_internal_name=self.internal_name,
                str_internal_header=self.internal_header)
        
class GeneralSetting(Base):
    __tablename__ = 'tbl_general_settings'
    general_id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    value = Column(String)
    
    def __repr__(self):
        return '<GeneralSetting(general_id={int_general_id}, key={str_key}, \
                value={str_value})>'.format(int_general_id=self.general_id, 
                str_key=self.key, str_value=self.value)
        
#class PricingRequestUnderlying(Base):
#    __tablename__ = 'tbl_pricing_request_underlyings'
#    pricing_request_id = Column(BigInteger, 
#                                           ForeignKey('tbl_pricing_requests.pricing_request_id'), 
#                                           primary_key=True)
#    underlying_id = Column(BigInteger, 
#                                      ForeignKey('tbl_underlyings.underlying_id'),
#                                      primary_key=True)
#    
#    def __repr__(self):
#        return '<PricingRequestUnderlying(pricing_request_id={int_pricing_request_id}, \
#                underlying_id={int_underlying_id})>'.format(int_pricing_request_id=self.pricing_request_id,
#                int_underlying_id=self.underlying_id)
        
class TenorType(Base):
    __tablename__ = 'tbl_tenor_types'
    tenor_type_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    pricing_request = relationship('PricingRequest', back_populates='tenor_type')
    
    def __repr__(self):
        return '<TenorType(tenor_type_id={int_tenor_type_id}, name={str_name})>'.format(
                int_tenor_type_id=self.tenor_type_id, str_name=self.name)

class FixingType(Base):
    __tablename__ = 'tbl_fixing_types'
    fixing_type_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    order = relationship('Order', back_populates='fixing_type')
    
    def __repr__(self):
        return '<FixingType(fixing_type_id={int_fixing_type_id}, name={str_name})>'.format(
                int_fixing_type_id=self.fixing_type_id, str_name=self.name)
        
class ETOExpiry(Base):
    __tablename__ = 'tbl_ETO_expiries'
    eto_expiry_id = Column(BigInteger, primary_key=True)
    expiry_date = Column(DateTime)
    underlying_id = Column(BigInteger, ForeignKey('tbl_underlyings.underlying_id'))
    underlying = relationship('Underlying', back_populates='eto_expiry')    
    underlying_volatility = relationship('UnderlyingVolatility', back_populates='eto_expiry')
    
    def __repr__(self):
        return '<ETOExpiry(eto_expiry_id={int_eto_expiry_id}, expiry_date=dte_expiry_date, \
                underlying_id={int_underlying_id})>'.format(int_eto_expiry_id=self.eto_expiry_id,
                dte_expiry_date=self.expiry_date, int_underlying_id=self.underlying_id)

class Underlying(Base):
    __tablename__ = 'tbl_underlyings'
    underlying_id = Column(BigInteger, primary_key=True)
    symbol = Column(String, unique=True)
    name = Column(String)
    web_address = Column(String)
    isin = Column(String, unique=True)
    description = Column(String)
    lot_size = Column(Integer)
    exchange_id = Column(Integer, ForeignKey('tbl_exchanges.exchange_id'))
    exchange = relationship('Exchange', back_populates='underlying')
    currency_id = Column(Integer, ForeignKey('tbl_currencies.currency_id'))
    currency = relationship('Currency', back_populates='underlying')
    underlying_type_id = Column(BigInteger, ForeignKey('tbl_underlying_types.underlying_type_id'))
    underlying_type = relationship('UnderlyingType', back_populates='underlying')
    asset_class_id = Column(Integer,ForeignKey('tbl_asset_classes.asset_class_id'))
    asset_class = relationship('AssetClass', back_populates='underlying')
    pricing_request = relationship('PricingRequest',
                                   secondary=pricing_request_underlying,
                                   back_populates='underlying')
    underlying_price = relationship('UnderlyingPrice', back_populates='underlying')
    eto_expiry = relationship('ETOExpiry', back_populates='underlying')
    underlying_volatility = relationship('UnderlyingVolatility', back_populates='underlying')
    
    def __repr__(self):
        return '<Underlying(underlying_id={int_underlying_id}, symbol={str_symbol}, \
                name={str_name}, web_address={str_web_address}, isin={str_isin}, \
                description={str_description}, lot_size={int_lot_size}, \
                exchange_id={int_exchange_id}, currency_id={int_currency_id}, \
                underlying_type_id={int_underlying_type_id}, asset_class_id={int_asset_class_id})>'.format(
                int_underlying_id=self.underlying_id, str_symbol=self.symbol,
                str_name=self.name, str_web_address=self.web_address, str_isin=self.isin,
                str_description=self.description, int_lot_size=self.lot_size,
                int_exchange_id=self.exchange_id, int_currency_id=self.currency_id,
                int_underlying_type_id=self.underlying_type_id, int_asset_class_id=self.asset_class_id)

class Exchange(Base):
    __tablename__ = 'tbl_exchanges'
    exchange_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    code = Column(String)
    market = Column(String)
    underlying = relationship('Underlying', back_populates='exchange')
    
    def __repr__(self):
        return '<Exchange(exchange_id={int_exchange_id}, name={str_name}, \
                code={str_code}, market={str_market})>'.format(int_exchange_id=self.exchange_id,
                str_name=self.name, str_code=self.code, str_market=self.market)
        
class Currency(Base):
    __tablename__ = 'tbl_currencies'
    currency_id = Column(Integer, primary_key=True)
    currency = Column(String, unique=True)
    pricing_request = relationship('PricingRequest', back_populates='currency')
    underlying = relationship('Underlying', back_populates='currency')
    
    def __repr__(self):
        return '<Currency(currency_id={int_currency_id}, currency={str_currency})>'.format(
                int_currency_id=self.currency_id, str_currency=self.currency)
        
class UnderlyingType(Base):
    __tablename__ = 'tbl_underlying_types'
    underlying_type_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    underlying = relationship('Underlying', back_populates='underlying_type')
    
    def __repr__(self):
        return '<UnderlyingType(underlying_type_id={int_underlying_type_id}, \
                name={str_name})>'.format(int_underlying_type_id=self.underlying_type_id,
                str_name=self.name)
        
class AssetClass(Base):
    __tablename__ = 'tbl_asset_classes'
    asset_class_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    underlying = relationship('Underlying', back_populates='asset_class')
    
    def __repr__(self):
        return '<AssetClass(asset_class_id={int_asset_class_id}, name={str_name})>'.format(
                int_asset_class_id=self.asset_class_id, str_name=self.name)
        
class UnderlyingPrice(Base):
    __tablename__ = 'tbl_underlying_prices'
    underlying_price_id = Column(BigInteger, primary_key=True)
    trade_date = Column(DateTime)
    open_ = Column('open', Float,key='open_')
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    bid = Column(Float)
    ask = Column(Float)
    volume = Column(Float)
    underlying_id = Column(BigInteger, ForeignKey('tbl_underlyings.underlying_id'))
    underlying = relationship('Underlying', back_populates='underlying_price')
    
    def __repr__(self):
        return '<UnderlyingPrice(underlying_price_id={int_underlying_price_id}, \
                trade_date={dte_trade_date}, open={dbl_open}, high={dbl_high}, \
                low={dbl_low}, close={dbl_close}, bid={dbl_bid}, ask={dbl_ask}, \
                volume = {dbl_volume}, underlying_id={int_underlying_id})>'.format(
                int_underlying_price_id=self.underlying_price_id, dte_trade_date=self.trade_date,
                dbl_open=self.open_, dbl_high=self.high, dbl_low=self.low, dbl_close=self.close,
                dbl_bid=self.bid, dbl_ask=self.ask, dbl_volume=self.volume,
                int_underlying_id=self.underlying_id)
        
class OptionType(Base):
    __tablename__ = 'tbl_option_types'
    option_type_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    underlying_volatility = relationship('UnderlyingVolatility', back_populates='option_type')
    
    def __repr__(self):
        return '<OptionType(option_type_id={int_option_type_id}, name={str_name})>'.format(
                int_option_type_id=self.option_type_id, str_name=self.name)

class UnderlyingVolatility(Base):
    __tablename__ = 'tbl_underlying_volatilities'
    underying_volatility_id = Column(BigInteger, primary_key=True)
    trade_date = Column(DateTime)
    strike = Column(Float)
    open_ = Column('open', Float, key='open_')
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    bid = Column(Float)
    ask = Column(Float)
    volume = Column(Float)
    open_interest = Column(Integer)
    tenor_type_id = Column(Integer)
    option_type_id = Column(Integer, ForeignKey('tbl_option_types.option_type_id'))
    option_type = relationship('OptionType', back_populates='underlying_volatility')
    eto_expiry_id = Column(BigInteger, ForeignKey('tbl_ETO_expiries.eto_expiry_id'))
    eto_expiry = relationship('ETOExpiry', back_populates='underlying_volatility')
    underlying_id = Column(BigInteger, ForeignKey('tbl_underlyings.underlying_id'))
    underlying = relationship('Underlying', back_populates='underlying_volatility')
    
    def __repr__(self):
        return '<UnderlyingVolatility(underlying_volatility_id={int_underlying_volatility_id}, \
                trade_date={dte_trade_date}, strike={dbl_strike}, open={dbl_open}, \
                high={dbl_high}, low={dbl_low}, close={dbl_close}, bid={dbl_bid}, \
                ask={dbl_ask}, volume = {dbl_volume}, open_interest={int_open_interest}, \
                tenor_type_id={int_tenor_type_id}, option_type_id={int_option_type_id}, \
                eto_expiry_id={int_eto_expiry_id}, underlying_id={int_underlying_id})>'.format(
                int_underlying_volatility_id=self.underying_volatility_id, dte_trade_date=self.trade_date,
                dbl_strike=self.strike, dbl_open=self.open_, dbl_high=self.high, 
                dbl_low=self.low, dbl_close=self.close, dbl_bid=self.bid, dbl_ask=self.ask, 
                dbl_volume=self.volume, int_open_interest=self.open_interest,
                int_tenor_type_id=self.tenor_type_id, int_option_type_id=self.option_type_id,
                int_eto_expiry_id=self.eto_expiry_id, int_underlying_id=self.underlying_id)
        
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


if __name__ == '__main__':
    str_conn = 'postgresql+psycopg2://postgres:HelloWorld$1@localhost:5432/DataAnalytics'
    engine = create_engine(str_conn, echo=True)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    currency = Currency(currency='USD')
    session.add(currency)
    session.commit()
    