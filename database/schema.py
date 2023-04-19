from sqlalchemy import MetaData, Table, Column, Integer, String


metadata = MetaData()


test_table = Table(
    'test',
    metadata,
    Column('id', Integer(), primary_key=True),
    Column('name', String(), unique=True)
)