import json
import speedtest
import sqlite3
import time

def speed():
    ts = int(time.time())

    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.upload()
    s.download()

    results_dict = s.results.dict()
    return {
        'server': '{name} {sponsor}'.format(
            name=results_dict['server']['name'],
            sponsor=results_dict['server']['sponsor'],
        ),
        'ts': ts,
        'ping': int(results_dict['ping']),
        'download': int(results_dict['download']) // 1000000,
        'upload': int(results_dict['upload']) // 1000000,
    }

def main():
    with sqlite3.connect('speedtest.db') as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS RESULTS(
                server TEXT,
                ts INTEGER,
                ping INTEGER,
                download INTEGER,
                upload INTEGER,
                PRIMARY KEY (server, ts)
            )
        """)

        # Start by measuring speedtest
        speedtest_result = speed()

        # Persist results
        connection.execute("""
            INSERT INTO RESULTS VALUES (
                :server,
                :ts,
                :ping,
                :download,
                :upload);
            """, (speedtest_result))

if __name__ == '__main__':
    main()
