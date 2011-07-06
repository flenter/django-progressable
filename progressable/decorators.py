try:
    from functools import update_wrapper, warps
except ImportError:
    from django.utils.functional import update_wrapper, wraps #Python 2.4 fallback

from inspect import getmodule
    
from django.utils.hashcompat import md5_constructor as md5
from django.core.cache import cache

class BlockingError(Exception):
    pass



def make_method_blocking(expires = 60 * 5, retry = True, register_params=[]):
    """Checks for a value in the cache to see if the current method is already
    called.
    
    .. note::
       Caching is required and should be shared by all processes.
       
    .. note::
       the lock_id is based on a hash of the args and kwargs and the namespace,
       method name. So a different set of arguments is enough to 'unblock'
       
    .. note::
       returns without doing much when the view_func is locked
    """

    def my_decorator(view_func):
        print view_func
        @wraps(view_func)
        def wrapper(self, *args, **kwargs):
            current_class = self.__class__
            blocking_id = getmodule(current_class).__name__ + '.' + current_class.__name__
    
            method = u""
    
            print kwargs
            for param in register_params:
                method += unicode(param) + u"=" + unicode(kwargs[param])
    
            digest = md5(method).hexdigest()
    
            lock_id = "%s-lock-%s" % (blocking_id, digest)
            print method
    
            acquire_lock = lambda : cache.add(lock_id, 'true', expires)
    
            release_lock = lambda : cache.delete(lock_id)
    
            if acquire_lock():
                print lock_id, "Lock acquired"
                value = cache.get(lock_id)
                try:
                    value = view_func(self, *args, **kwargs)
                except Exception, e:
                    print e
                finally:
                    release_lock()
                    print lock_id, "lock released"
                    return value
            else:
                print lock_id, "Locked!!!!!!!!!!!!!!!!"
                try:
                    raise BlockingError("Already running %s " % method)
                except BlockingError, e:
                    if retry:
                        self.retry(exc=e)
    
                    raise e
    
    
    
        return wrapper

    return my_decorator
