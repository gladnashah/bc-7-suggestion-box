from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comments = Table('comments', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', Text),
    Column('body_html', Text),
    Column('timestamp', DateTime, default=ColumnDefault(<function <lambda> at 0x0000000003CC1EB8>)),
    Column('disabled', Boolean),
    Column('author_id', Integer),
    Column('post_id', Integer),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=140)),
    Column('body', String(length=140)),
    Column('body_html', Text),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comments'].create()
    post_meta.tables['posts'].columns['body_html'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comments'].drop()
    post_meta.tables['posts'].columns['body_html'].drop()
