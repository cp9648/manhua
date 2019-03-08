# 导入引擎创建函数

# 销毁引擎
from sqlalchemy import create_engine
# 导入语句处理函数
from sqlalchemy.sql.expression import text

# 不单独加载每个函数，只引入模块，后续按需调用
from sqlalchemy.sql import expression as sse

# 导入元数据、表类
from sqlalchemy import MetaData, Table
# 导入数据类型
from sqlalchemy import Integer, Float, Text, String, TIMESTAMP, DateTime
# 导入列类和关联
from sqlalchemy import Column, ForeignKey

# 引擎
# uri = 'sqlite:///:memory:'
# SQLAlchemy连接URI
uri = 'mysql+pymysql://root:root@127.0.0.1:3306/scrapyDB?charset=utf8'

# 引擎
engine = create_engine(uri)


def scrapyDB():
    # 元信息
    meta = MetaData(bind=engine)
    # 定义用户表
    tb_detailed = Table(
        'detailed',
        meta,
        Column('id', Integer, autoincrement=True, primary_key=True, comment='主键ID'),
        Column('name', String(20), nullable=False, unique=True, comment='书籍名称'),
        Column('state', String(32), nullable=False, comment='状态'),
        Column('author', String(20), nullable=False, comment='作者'),
        Column('_type', String(20), nullable=False, comment='类型'),
        Column('_update', String(20), nullable=False, comment='修改时间'),
        extend_existing=True,
        comment='书籍表'
    )
    # 定义交易表
    tb_chapter = Table(
        'chapter',
        meta,
        Column('id', Integer, autoincrement=True, primary_key=True, comment='主键ID'),
        Column('name', String(20), ForeignKey('detailed.name'), nullable=False, comment='书籍名称'),
        Column('chapter', String(20), nullable=False, comment='章节名'),
        Column('content', Text, nullable=False, comment='详细图片'),
        extend_existing=True,
        comment='详细内容表'
    )
    # 创建表
    meta.create_all(tables=meta.sorted_tables)

# 销毁引擎
engine.dispose()
