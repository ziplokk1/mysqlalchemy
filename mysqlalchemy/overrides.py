from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker as _sessionmaker, Session as _Session

from .errors import get_error


class MysqlSession(_Session):

    def __init__(self, *args, **kwargs):
        super(MysqlSession, self).__init__(*args, **kwargs)

    def _do_method(self, f, *args, **kwargs):
        try:
            return f(*args, **kwargs)
        except OperationalError as err:
            err_code, err_message = err.orig.args
            err_code = int(err_code)
            ErrCls = get_error(err_code)
            if ErrCls:
                raise ErrCls(err_message) from err
            raise

    def execute(self, clause, params=None, mapper=None, bind=None, **kw):
        return self._do_method(super(MysqlSession, self).execute, clause, params=params, mapper=mapper, bind=bind, **kw)

    def commit(self):
        return self._do_method(super(MysqlSession, self).commit)


class sessionmaker(_sessionmaker):
    """
    Just used to type-hint the __call__ method of sessionmaker.

    This class should never be called directly outside of this library.

    :param **local_kw: Keyword arguments to be passed to :func:`sqlalchemy.orm.sessionmaker`.
    :rtype: MysqlSession
    """

    def __call__(self, **local_kw):
        """
        Used only to provide type-hinting.

        :param local_kw:
        :rtype: MysqlSession
        :return:
        """
        return super().__call__(**local_kw)
