from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when

class SaltProvides(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:salt}-relation-{joined,changed}')
    def changed(self):
        if self.get_local('address') is None:
            self.set_state('{relation_name}.unconfigured')
        rmtMinion = self.get_remote('minion')
        lclMinion = self.get_local('minion')
        if rmtMinion is not lclMinion:
            self.set_state('{relation_name}.newminion')
            self.set_local('minion',rmtMinion)

    @hook('{provides:salt}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')

    @property
    def minion(self):
        return self.get_remote('minion')

    def configure(self,address,port):
        relation_info = {
            'address': address,
            'port': port
             }
        self.set_remote(**relation_info)
        self.set_local(**relation_info)
        self.remove_state('{relation_name}.unconfigured')


