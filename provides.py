from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
from charmhelpers.core import hookenv
import socket

class SaltProvides(RelationBase):
    scope = scopes.UNIT

    @hook('{provides:salt}-relation-{joined,changed}')
    def changed(self):
        print("Provides realation joined/changed called")
        self.set_state('{relation_name}.available')
        if self.get_local('hostname') is None:
            self.set_state('{relation_name}.unconfigured')
        if self.get_remote('unconfigured'):
            print("Salt master needs to re-run configuration")

    @hook('{provides:salt}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')

    def configure(self):
        relation_info = {
            'hostname': socket.gethostname(),
             }
        print("SaltProvides configured")
        self.set_remote(**relation_info)
        self.set_local(**relation_info)
        self.remove_state('{relation_name}.unconfigured')


