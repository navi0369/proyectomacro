import libsql_experimental as libsql
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()
url = os.getenv("TURSO_DATABASE_URL")
auth_token = os.getenv("TURSO_AUTH_TOKEN")
conn = libsql.connect("db/proyectomacro.db", sync_url=url, auth_token=auth_token)
cursor = conn.cursor()
conn.sync()