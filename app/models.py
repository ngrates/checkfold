from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    __tablename__ = 'user_dimension'

    # Data Fields
    user_key: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Relationship to SessionsFact
    sessions = so.relationship('SessionsFact', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Room(db.Model):
    __tablename__ = 'room_dimension'

    # Data Fields
    room_key: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    room_name: so.Mapped[str] = so.mapped_column(sa.String(255))
    country: so.Mapped[str] = so.mapped_column(sa.String(100))
    country_code: so.Mapped[str] = so.mapped_column(sa.String(3))
    state_province: so.Mapped[str] = so.mapped_column(sa.String(100))
    state_province_code: so.Mapped[str] = so.mapped_column(sa.String(20))
    city: so.Mapped[str] = so.mapped_column(sa.String(255))
    postal_code: so.Mapped[str] = so.mapped_column(sa.String(20))
    address_line1: so.Mapped[str] = so.mapped_column(sa.String(255))
    address_line2: so.Mapped[str] = so.mapped_column(sa.String(255))

    # Relationship to PokerTable
    poker_tables = so.relationship('PokerTable', back_populates='room')


class PokerTable(db.Model):
    __tablename__ = 'poker_table_dimension'

    # Data Fields
    table_key: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    room_key: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('room_dimension.room_key'))
    max_seats: so.Mapped[int] = so.mapped_column(sa.Integer)
    game_type: so.Mapped[str] = so.mapped_column(sa.String(50))
    limit_type: so.Mapped[str] = so.mapped_column(sa.String(50))
    small_blind: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    big_blind: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    min_buy_in: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    max_buy_in: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    dealer_ante: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))

    # Relationships
    room = so.relationship('Room', back_populates='poker_tables')
    sessions = so.relationship('SessionsFact', back_populates='poker_table')


class Date(db.Model):
    __tablename__ = 'date_dimension'

    # Data Fields
    date_key: so.Mapped[int] = so.mapped_column(sa.SmallInteger, primary_key=True)
    full_date: so.Mapped[sa.Date] = so.mapped_column(sa.Date)
    day_of_week: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    day_num_in_month: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    day_num_overall: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    day_name: so.Mapped[str] = so.mapped_column(sa.String(9))
    day_abbrev: so.Mapped[str] = so.mapped_column(sa.CHAR(3))
    weekday_flag: so.Mapped[str] = so.mapped_column(sa.CHAR(1))
    week_num_in_year: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    week_num_overall: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    week_begin_date: so.Mapped[sa.Date] = so.mapped_column(sa.Date)
    week_begin_date_key: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    month: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    month_num_overall: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    month_name: so.Mapped[str] = so.mapped_column(sa.String(9))
    month_abbrev: so.Mapped[str] = so.mapped_column(sa.CHAR(3))
    quarter: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    year: so.Mapped[int] = so.mapped_column(sa.SmallInteger)
    yearmo: so.Mapped[int] = so.mapped_column(sa.Integer)
    last_day_in_month_flag: so.Mapped[str] = so.mapped_column(sa.CHAR(1))
    same_day_year_ago_date: so.Mapped[sa.Date] = so.mapped_column(sa.Date)

    # Relationship to SessionsFact
    sessions = so.relationship('SessionsFact', back_populates='date')


class Time(db.Model):
    __tablename__ = 'time_dimension'

    # Data Fields
    time_key: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    hour: so.Mapped[int] = so.mapped_column(sa.Integer)
    minute: so.Mapped[int] = so.mapped_column(sa.Integer)
    am_pm: so.Mapped[str] = so.mapped_column(sa.String(2))
    time_of_day: so.Mapped[str] = so.mapped_column(sa.String(20))

    # Relationship to SessionsFact
    sessions = so.relationship('SessionsFact', back_populates='time')


class SessionsFact(db.Model):
    __tablename__ = 'sessions_fact'

    # Data Fields
    user_key: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user_dimension.user_key'), primary_key=True, autoincrement=False)
    table_key: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('poker_table_dimension.table_key'), primary_key=True, autoincrement=False)
    date_key: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('date_dimension.date_key'), primary_key=True, autoincrement=False)
    time_key: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('time_dimension.time_key'), primary_key=True, autoincrement=False)
    buy_in: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    cash_out: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    duration_hours: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    drink_money: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    tips: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))
    bonus_money: so.Mapped[sa.Numeric] = so.mapped_column(sa.Numeric(10, 2))

    # Relationships
    user = so.relationship('User', back_populates='sessions')
    poker_table = so.relationship('PokerTable', back_populates='sessions')
    date = so.relationship('Date', back_populates='sessions')
    time = so.relationship('Time', back_populates='sessions')
