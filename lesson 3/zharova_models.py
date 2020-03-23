from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)
    comment_cnt = Column(Integer, nullable=False)
    writer_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship('Writer', back_populates='post')
    comment = relationship('Comment', back_populates='post')

    def __init__(self, title, url, comment_cnt, writer_id):
        self.title = title
        self.url = url
        self.comment_cnt = comment_cnt
        self.writer_id = writer_id



class Writer(Base):
    __tablename__ = 'writer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=False, nullable=False)
    url = Column(String, unique=True, nullable=False)
    post = relationship('Post', back_populates='writer')
    comment = relationship('Comment', back_populates='writer')

    def __init__(self, name, url):
        self.name = name
        self.url = url

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='comment')
    writer_id = Column(Integer, ForeignKey('writer.id'))
    writer = relationship('Writer', back_populates='comment')

    def __init__(self, post_id, writer_id):
        self.post_id = post_id
        self.writer_id = writer_id


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.session import Session

    engine = create_engine('sqlite:///gb_blog.db')
    Base.metadata.create_all(engine)
    session_db = sessionmaker(bind=engine)

    session = session_db()

    post = Post('Первый пост2')
    session.add(post)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

    print(1)

    pass
