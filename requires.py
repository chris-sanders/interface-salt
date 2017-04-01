from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
import socket

class SaltRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:salt}-relation-{joined,changed}')
    def changed(self):
        if self.get_remote('address'):
            self.set_state('{relation_name}.changed')

    @hook('{requires:salt}-relation-{departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')

    @property
    def address(self):
        return self.get_remote('address')

    def minion_ready(self):
        self.set_remote("minion",socket.getfqdn())

