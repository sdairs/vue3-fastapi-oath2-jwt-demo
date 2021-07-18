import re
import sys
from getpass import getpass
from os.path import expanduser
from urllib.parse import parse_qs, urlparse

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, ProgrammingError


def build_engine(connection_string):
    """
    Creates a SQLAlchemy database engine.

    This won't connect to the cluster until engine.connect is called.
    """
    return create_engine(connection_string, echo=False)


def show_databases(engine):
    """
    Runs the SHOW DATABASES command.

    Returns
    -------
    Databases (sqlalchemy.engine.result.ResultProxy)
    """
    return engine.execute("SHOW DATABASES")


def print_error_text(error):
    """
    Shows the original error text for the user.
    """
    print("  Error text: {}".format(error))


def check_for_hostname_error(error):
    """
    Checks if hostname isn't resolving to an IP address.
    """
    print("Checking hostname.")
    if 'could not translate host name' in str(error):
        print("  ... Hostname is not resolving to an ip address.")
        print("  The most likely reason is that your hostname is incorrect.")
        print_error_text(error)
        return True

    print("  ... No issue found.")
    return False


def check_for_timeout(error):
    """
    Determines if an error is from a timeout & gives advice if so.
    """
    print("Checking for connection timeout.")
    if (('Operation timed out' in str(error))
            or ('timeout expired' in str(error))):
        print("  ... the connection timed out.")
        print("  This can happen for a variety of reasons, but it's possible "
              "that CockroachCloud hasn't authorized your IP address. Start "
              "by logging into your CockroachCloud account and verifying that "
              "your IP address is authorized.")
        print_error_text(error)
        return True
    print("  ... No issue found.")
    return False


def check_for_login(error):
    """
    Check error; if username or password is the issue, print advice.
    """
    print("Checking username and password combination.")
    if 'password authentication failed' in str(error):
        print("  Username/password combination is invalid.")
        print("  Try checking your username and password. "
              "One or both are likely incorrect.")
        print_error_text(error)
        return True
    print("  ... No issue found.")
    return False


def check_for_crt(error):
    """
    Check error; if lack of .crt is the issue, print advice.
    """
    print("Checking for location of `.crt` file.")
    if ('root certificate file' in str(error)
            and 'does not exist' in str(error)):
        print("  .crt file not found. Please verify that the `--cert-dir` "
              "parameter points to the right location, and that the `--ca` "
              "parameter is the name of the file.")
        print_error_text(error)
        return True
    print("  ... No issue found.")
    return False


def check_for_refused_connection(error):
    """
    Check error; if refused connection is the issue, print advice.
    """
    print("Checking for a refused connection.")
    if 'Connection refused' in str(error):
        print("  ... connection refused.")
        print("  This often occurs when your IP address is not allowlisted in "
              "CockroachCloud.")
        print_error_text(error)
        return True
    print("  ... No issue found.")
    return False


def check_crt_validity(error):
    """
    Check error; if invalid .crt file is the issue, print advice.
    """
    print("Checking the `.crt` file's validity.")
    if 'could not read' in str(error) and 'wrong tag' in str(error):
        print(".crt file found, but file is corrupted.")
        print("Please download a new .crt file from your CockroachCloud "
              "account.")
        print_error_text(error)
        return True

    if 'certificate verify failed' in str(error):
        print("`.crt` file found, but the certificate is not valid.")
        print("Please point to the correct CA or download a new .crt file "
              "from your CockroachCloud account.")
        print_error_text(error)
        return True

    print("  ... CA cert file appears to be valid.")
    return False


def check_for_database_existence_error(error):
    """
    Check error; if invalid database is the issue, print advice.
    """
    print("Checking for database existence.")
    expected_pattern = re.compile('database ".*" does not exist')
    if expected_pattern.search(str(error)):
        print("It looks like the database you're attempting to connect to "
              "doesn't exist.")
        print("One suggestion would be to try to log in to the `defaultdb` "
              "database using `/defaultdb` after the port.")
        print_error_text(error)
        return True

    print("  ... database appears to be valid.")
    return False


def show_unexpected_error(error):
    """
    Directs students on what to do if an unexpected error was caught.
    """
    print("Unexpected error occurred. Please email the text of this "
          "error to university@cockroachlabs.com")
    print_error_text(error)


def test_connection(engine):
    """
    Examines connection error to determine the likely cause.
    """
    try:
        engine.connect()
        return True
    except OperationalError as error:
        print("Caught an error while checking the connection. Investigating.")
        if check_for_timeout(error):
            sys.exit()
        elif check_for_hostname_error(error):
            sys.exit()
        elif check_for_refused_connection(error):
            sys.exit()
        elif check_for_crt(error):
            sys.exit()
        elif check_crt_validity(error):
            sys.exit()
        elif check_for_login(error):
            sys.exit()
        else:
            show_unexpected_error(error)
    except ProgrammingError as error:
        if check_for_database_existence_error(error):
            sys.exit()
    except Exception as error:
        raise Exception("Reached a point in the code that should never have "
                        "been touched. Please email "
                        "university@cockroachlabs.com.\n\n"
                        "Error code is 2019-05-27-1.\n "
                        "Original error text:\n\n----------{}".format(error))


def get_database(url):
    """
    Parses the database from the url.

    This is done because `defaultdb` is the database given by the url string,
        but often a script will require a database name that is linked to its
        purpose. This script gives the user a chance to change it.
    """
    parsed_url = urlparse(url)
    database = parsed_url.path[1:]  # '/dbname' -> 'dbname'
    if database == 'defaultdb':
        input_db = input("WARNING: Your database is listed as defaultdb. "
                         "Please input another (such as `movr` if this was a "
                         "mistake. (hit enter to keep it as `defaultdb`).\n")
        if input_db == '':
            return database
        return input_db

    return database


def build_sqla_connection_string(cockroach_cloud_url, timeout=10):
    """
    Builds a connection string for a SQLAlchemy engine from the CC url.
    """
    cloud_parse = urlparse(cockroach_cloud_url)
    if (
            cloud_parse.scheme not in ('postgres', 'postgresql', 'cockroachdb')
            and cloud_parse.scheme != 'postgresql'):
        raise ValueError(("Was expecting connection string to start with "
                          "'postgres://' but instead found {}://"
                          ).format(cloud_parse.scheme))

    scheme = 'cockroachdb'
    username = cloud_parse.username
    password = prevalidate_password(cloud_parse.password)
    hostname = cloud_parse.hostname
    port = cloud_parse.port
    database = get_database(cockroach_cloud_url)
    querystring = build_querystring(cloud_parse.query, connect_timeout=timeout)

    sqla_url = ('{scheme}://{username}:{password}@{hostname}:{port}/'
                '{database}?{querystring}'
                ).format(scheme=scheme, username=username, password=password,
                         hostname=hostname, port=port, database=database,
                         querystring=querystring)

    return sqla_url


def build_querystring(query, connect_timeout=10):
    """
    Cleans the querystring for SQLAlchemy from the cockroach sql querystring.

    This has to be done because (1) CockroachCloud sometimes gives
        '<certs_dir>' as a string literal, and because we want to help with ~/,
        which sqlalchemy doesn't know how to parse.
    """
    for field, value in parse_qs(query).items():
        if len(value) > 1:
            raise ValueError(("Querystring contains duplicate values:"
                              "{field}: {value}\n"
                              "Please assign only one value for each "
                              "querystring parameter.").format(field=field,
                                                               value=value))
    if '<certs_dir>' in query:  # they didn't set it locally
        print("String literal '<certs_dir>' found for .crt directory.")
        query = query.replace('<certs_dir>', get_certs_dir())

    if '~' in query:  # SQLAlchemy doesn't know how to work with this.
        query = query.replace('~', expanduser('~'))

    return query + '&connect_timeout={}'.format(connect_timeout)


def get_password():
    """
    Prompts user to input password on the command line.
    """
    return getpass(prompt='  Input Password: ', stream=None)


def get_certs_dir():
    """
    Propmts user for directory of .crt file

    Note that both absolute and relative paths are allowed.
    """
    return input("  Input directory where the .ca cert is located: ")


def prevalidate_password(password):
    """
    Parses password & asks user to re-input if it looks fishy.
    """
    if password is None:
        return get_password()
    if password == '<password>':
        print("String literal '<password>' found in connection string.")
        return get_password()

    return password


def main():
    """Connects, tests the connection, and runs `SHOW DATABASES`."""

    connection_string = build_sqla_connection_string(opts['--url'],
                                                     timeout=opts['--timeout'])

    print("Connection string: {}".format(connection_string))
    engine = build_engine(connection_string=connection_string)
    test_connection(engine)

    print("Testing connection by running a `SHOW DATABASES` command.")
    for database in show_databases(engine):
        print("   " + database[0])


if __name__ == '__main__':
    main()

