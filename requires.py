from charms.reactive import RelationBase
from charms.reactive import scopes
from charms.reactive import hook
from charms.reactive import when
import socket
#from charms.reactive import remove_state

class SaltRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:salt}-relation-{joined,changed}')
    def changed(self):
        conv = self.conversation()
        print("Requires relation joined/changed called")
        if conv.get_remote('address'):
            conv.set_state('{relation_name}.changed')

    @hook('{requires:salt}-relation-{departed}')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.available')

    @property
    def address(self):
        return self.get_remote('address')
        #conv = self.conversation()
        #return conv.get_remote('hostname')

    def minion_ready(self):
        #conv = self.conversation()
        print("salt-minion is ready")
        self.set_remote("minion",socket.getfqdn())

