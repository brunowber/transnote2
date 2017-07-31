"""Models para infratores"""

from detransapp.models.pessoa import Pessoa


class Infrator(Pessoa):
    """Classe para models de infratores"""

    def __unicode__(self):
        return self.nome

    class Meta:
        app_label = "detransapp"
