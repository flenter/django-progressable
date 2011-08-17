from redisco import models

from uuid import uuid4

class UUIDField(models.Attribute):
    def __init__(self,
                 name=None,
                 indexed=True,
                 required=False,
                 validator=None,
                 unique=False,
                 default=None):

        if not default:
            default = uuid4

        super(UUIDField, self).__init__(name=name, indexed = indexed, required=required, validator = validator, unique = unique, default = default)

#from stdnet import orm
#
#class UUIDField2(orm.SymbolField):
#    def __init__(self, default=None, unique=True, *args, **kwargs):
#        if not default:
#            default = uuid4
#        super(UUIDField2, self).__init__(default=default, unique=unique, *args, **kwargs)
