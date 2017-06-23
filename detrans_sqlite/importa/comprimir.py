import gzip
import shutil


def comprimir_detrans_sqlite(arquivo_sqlite_nome):
    with open(arquivo_sqlite_nome, 'rb') as f_in, gzip.open(arquivo_sqlite_nome+'.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)