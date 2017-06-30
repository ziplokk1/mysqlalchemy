import os

from sqlalchemy import create_engine

from .overrides import sessionmaker, MysqlSession


class Transaction(object):
    """
    Context manager for database connection.
    """

    def __init__(self, _Class):
        """
        :type _Class: sessionmaker
        :param _Class:
        """
        self.Class = _Class
        self.instance = None

    def __enter__(self):
        self.instance = self.Class()
        return self.instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.instance.close()
        self.instance = None


class Connection(object):
    """
    Context manager for a repeated connection to mysql.

    Used to minimize calls to create_engine and sessionmaker.

    :Example:

    >>> # Connection with no connect_args.
    >>> connection = Connection(url='mysql://database.mysite.com/schema', user='user', passwd='password', charset='utf8')

    :Example:

    >>> # Connection with connect_args.
    >>> connection = Connection(url='mysql://database.mysite.com/schema', connect_args={'user': 'user', 'passwd': 'password', 'charset': 'utf8'})

    :Example:

    >>> # Connection with new env
    >>> # For this to work you need to set the following environment variables:
    >>> # DB_URL=mysql://database.mysite.com/schema
    >>> # DB_USER=user
    >>> # DB_PASS=password
    >>> connection = Connection()

    :Example:

    >>> # Connection with existing env
    >>> connection = Connection(env_db_url='CUSTOM_DB_URL_ENV', env_db_user='CUSTOM_DB_USER_ENV', env_db_pass='CUSTOM_DB_PASS_ENV')

    :Example:

    >>> # After connection variable has been set...
    >>> with connection() as cnxn:
    ...     rows = cnxn.execute("SELECT * FROM some_table;").fetchall()
    >>> # with parameters
    >>> with connection() as cnxn:
    ...     rows = cnxn.execute("SELECT * FROM some_table WHERE field = :p;", {'p': 'value'}).fetchall()

    :param **kwargs: Keyword arguments to be passed to the connect_args param in :func:`create_engine`.
        Note: If connect_args is not passed into kwargs, then the kwargs itself becomes the connect_args.
    """

    def __init__(self, **kwargs):
        # Get environment variables for database connection.
        env_db_url = kwargs.pop('env_db_url', 'DB_URL')
        env_db_user = kwargs.pop('env_db_user', 'DB_USER')
        env_db_pass = kwargs.pop('env_db_pass', 'DB_PASS')

        # If `url` was not passed into kwargs
        # and the environment variable supplied by env_db_url was not found
        # and DB_URL environment variable is not set...
        db_url = os.getenv(env_db_url) or kwargs.get('url', None)
        # remove url from kwargs since if the DB_URL env was set and URL was still supplied, then
        # the url argument will remain in kwargs and mess up the kwargs being passed to create_engine
        kwargs.pop('url', None)

        if not db_url:
            raise ValueError('Param `url` is required if param `env_db_url` is not supplied and \'DB_URL\' environment variable is not set.')

        db_user = os.getenv(env_db_user)
        db_pass = os.getenv(env_db_pass)

        echo = kwargs.pop('echo', False)

        # If using connect_args to establish connection.
        if kwargs.get('connect_args'):
            connect_args = kwargs.pop('connect_args')
        else:
            connect_args = kwargs
            kwargs = {}

        # Update connect args to use the environment variables if they exist.
        connect_args['user'] = db_user or connect_args.get('user')
        connect_args['passwd'] = db_pass or connect_args.get('passwd')
        kwargs = {'echo': echo, 'connect_args': connect_args}

        engine = create_engine(db_url, **kwargs)
        Session = sessionmaker(engine, class_=MysqlSession)
        self.context_manager = Transaction(Session)

    def __call__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :rtype: Transaction
        :return:
        """
        return self.context_manager
