import os
import pathlib

from dotenv import load_dotenv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection


from . import config


settings = config.get_settings()
# load_dotenv()    # load env variables
ASTRA_DB_CLIENT_ID = settings.db_client_id     # os.environ.get("ASTRA_DB_CLIENT_ID")  #
ASTRA_DB_CLIENT_SECRET = settings.db_client_secret  # os.environ.get("ASTRA_DB_CLIENT_SECRET")

BASE_DIR = pathlib.Path(__file__).parent  #pathlib чтобы жрал connect.zip без ignored/

CLUSTER_BUNDLE = str(BASE_DIR / "ignored" / 'connect.zip')


def get_cluster():
    cloud_config = {
        'secure_connect_bundle': CLUSTER_BUNDLE,
        'init-query-timeout': 500,
        'connect_timeout': 500,
        'set-keyspace-timeout': 500
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)  # registring the connection
    set_default_connection(str(session))
    return session

# class Connection:
#     def __init__(self):
#         self.secure_connect_bundle=CLUSTER_BUNDLE
#         self.path_to_creds=''
#         self.cluster = Cluster(
#             cloud={
#                 'secure_connect_bundle': self.secure_connect_bundle,
#                 'init-query-timeout': 10,
#                 'connect_timeout': 10,
#                 'set-keyspace-timeout': 10
#             },
#             auth_provider=PlainTextAuthProvider(ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
#         )
#         self.session = self.cluster.connect(KEYSPACE)
#     def close(self):
#         self.cluster.shutdown()
#         self.session.shutdown()

# session = get_session()
# row = session.execute("select release_version from system.local").one()
# if row:
#     print(row[0])
# else:
#     print("An error occurred.")