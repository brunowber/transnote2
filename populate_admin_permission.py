# coding: utf-8
import os

import datetime
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detrans.settings')


django.setup()


def populate():
    add_permissoes("permissao_geral", "permissao_geral")
    add_sistema("TRANSNOTE", "SISTEMA TRANSNOTE", "")
    add_admin(1, "pmj", "pmj", "Prefeitura de Joinville")


def add_permissoes(name, codename):
    from global_permissions.models import GlobalPermission
    GlobalPermission.objects.get_or_create(name=name, codename=codename)[0]


def add_sistema(sigla, nome, logo):
    from detransapp.models.sistema import Sistema
    Sistema.objects.get_or_create(sigla=sigla, nome_completo=nome, logo=logo, data=datetime.datetime.now())[0]


def add_admin(identificacao, user, password, first):
    from detransapp.models import Agente
    try:
        agente = Agente.objects.get_or_create(username=user, identificacao=identificacao, first_name=first)[0]
        agente.set_password(password)
        agente.user_permissions.add(True)
        agente.is_staff = True
        agente.is_superuser = True
        agente.save()
    except django.db.utils.IntegrityError:
        print ("Admin já foi criado")


if __name__ == '__main__':
    print("Starting population script...")
    populate()
