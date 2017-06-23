"""Model para proprietarios"""

from detransapp.models.pessoa import Pessoa


class Proprietario(Pessoa):
    """Classe para model de proprietarios"""

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        app_label = "detransapp"
