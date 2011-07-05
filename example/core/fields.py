
from django.db.models import CharField
from random import Random
try:
    import uuid
except ImportError:
    from django.utils import uuid



class UUIDVersionError(Exception):
    """Exception for UUIDVersion problems
    """
    pass

#class CodeField(CharField):
class CodeField(CharField):
    """ Codefield for django supports random codes of different lengths
    """
    
    def __init__(self, verbose_name=None, name=None, auto=True, max_length=6, **kwargs):
        if auto:
            kwargs['blank'] = True
            kwargs['editable'] = kwargs.get('editable', False)
        self.auto = auto
        
        CharField.__init__(self, verbose_name, name, max_length = max_length, **kwargs)
        
    def generate_code(self, code_length=6, alternate_hands=False):
        """Generate the actual code. Returns the code
        """
        rng = Random()
        
        righthand = '23456QWERTASDFGZXCVBqwertasdfgzxcvb~!@#$%^`'
        lefthand = '789YUPHJKNMyuphjknm&*()-=_+[]\\{}|;\':",./<>?'
        allchars = righthand + lefthand
        
        code = ""
        for i in range(code_length):
            if not alternate_hands:
                code += rng.choice(allchars)
            else:
                if i%2:
                    code += rng.choice(lefthand)
                else:
                    code += rng.choice(righthand)
    
        return code

      
    def pre_save(self, model_instance, add):
        
        value = getattr(model_instance, self.attname)
        
        if self.auto and add and not len(value):

            value = unicode(self.generate_code(code_length = self.max_length))
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(CodeField, self).pre_save(
                model_instance,
                add)
            if self.auto and not value:
                value = unicode(self.generate_code(code_length = self.max_length))
                setattr(model_instance, self.attname, value)
        return value
      

class UUIDField(CharField):
    """ UUIDField for Django, supports all uuid versions which are natively
        suported by the uuid python module.
    """
#
    def __init__(self, verbose_name=None, name=None, auto=True, version=1, node=None, clock_seq=None, namespace=None, **kwargs):
        kwargs['max_length'] = 36
        if auto:
            kwargs['blank'] = True
            kwargs['editable'] = kwargs.get('editable', False)
        self.version = version
        if version==1:
            self.node, self.clock_seq = node, clock_seq
        elif version==3 or version==5:
            self.namespace, self.name = namespace, name
        self.auto = auto
        CharField.__init__(self, verbose_name, name, **kwargs)

    def get_internal_type(self):
        return CharField.__name__

    def create_uuid(self):
        if not self.version or self.version==4:
            return uuid.uuid4()
        elif self.version==1:
            return uuid.uuid1(self.node, self.clock_seq)
        elif self.version==2:
            raise UUIDVersionError("UUID version 2 is not supported.")
        elif self.version==3:
            return uuid.uuid3(self.namespace, self.name)
        elif self.version==5:
            return uuid.uuid5(self.namespace, self.name)
        else:
            raise UUIDVersionError("UUID version %s is not valid." % self.version)

    def pre_save(self, model_instance, add):
        if self.auto and add:
            value = unicode(self.create_uuid())
            setattr(model_instance, self.attname, value)
            return value
        else:
            value = super(UUIDField, self).pre_save(
                model_instance,
                add)
            if self.auto and not value:
                value = unicode(self.create_uuid())
                setattr(model_instance, self.attname, value)
        return value
      
try:
  import south
  from south import modelsinspector
except ImportError:
  south = None
  pass

if south:
  modelsinspector.add_introspection_rules([
    (
      [UUIDField],
      [],
      {
        'verbose_name': ['verbose_name', {'default': None}],
        'name': ['name', {'default': None}],
        'version': ['version', {'default': 1}],
        'node': ['node', {'default': None}],
        'clock_seq': ['clock_seq', {'default': None}],
        #'namespace': ['namespace', {'default': None}],
      },
    )],
    ["^core\.fields\.UUIDField"])
  
  modelsinspector.add_introspection_rules([
    (
      [CodeField],
      [],
      {
        'verbose_name': ['verbose_name', {'default': None}],
        'name': ['name', {'default': None}],
        'auto': ['auto', {'default': True}],
        'max_length': ['max_length', {'default': 6}]
        #'namespace': ['namespace', {'default': None}],
      },
    )],
    ["^core\.fields\.CodeField"])
  
