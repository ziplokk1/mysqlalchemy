class MysqlError(Exception):
    """
    Error class for errors returned by a Mysql Server.

    See https://dev.mysql.com/doc/refman/5.5/en/error-messages-server.html
    """
    code = None
    def __init__(self, message):
        super(MysqlError, self).__init__(message)
        self.message = message

    def __repr__(self):
        return '<{} code={} message={}>'.format(self.__class__.__name__, self.code, self.message)


class TableAccessDeniedError(MysqlError):
    code = 1142


class LockWaitTimeoutError(MysqlError):
    code = 1205


class LockDeadlockError(MysqlError):
    code = 1213


_errors = {
    TableAccessDeniedError.code: TableAccessDeniedError,
    LockWaitTimeoutError.code: LockWaitTimeoutError,
    LockDeadlockError.code: LockDeadlockError,
}


def get_error(code):
    """
    Get a MysqlError object from an error code.

    :param code: MySql specific error code. See: https://dev.mysql.com/doc/refman/5.7/en/error-messages-server.html.
    :return: MysqlError object. (Not instance).
    """
    return _errors.get(code)
