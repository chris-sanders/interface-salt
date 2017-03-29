from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
from charmhelpers.core import hookenv

class SaltProvides(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:salt}-relation-{joined,changed}')
    def changed(self):
        print("Provides realation joined/changed called")
        localMinion = self.get_local('minion')
        remoteMinion = self.get_remote('minion')
        if self.get_local('address') is None:
            self.set_state('{relation_name}.unconfigured')
        if self.get_remote('minion'):
            self.set_state('{relation_name}.newminion')

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
        print("SaltProvides configured")
        self.set_remote(**relation_info)
        self.set_local(**relation_info)
        self.remove_state('{relation_name}.unconfigured')


