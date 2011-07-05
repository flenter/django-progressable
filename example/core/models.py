from django.db import models

from django.utils.translation import ugettext_lazy as _

from datetime import datetime

PUBLISH_STATE_DRAFT = 'draft'
PUBLISH_STATE_PUBLISHED = 'published'
PUBLISH_STATE_FOR_REVIEW = 'for_review'

PUBLISH_STATES = ( 
    (PUBLISH_STATE_DRAFT, _('draft')), 
    (PUBLISH_STATE_PUBLISHED,_('published')), 
    (PUBLISH_STATE_FOR_REVIEW,_('for review')), 
) 
 
class LiveManager(models.Manager):
    """Live manager, checks for publish_date and state.
    
    .. note::
       it is not a failsafe way of retrieving data that is published. Keep using
       common sense while developing!
    """

    def get_or_create(self, *args, **kwargs):
        commit = kwargs.get("commit", 'default_is_true')
        if commit == 'default_is_true':
            commit = True
        else:
            del kwargs['commit']
            
        if commit == False:
            try:
                return (self.get(**kwargs), False)
            except self.model.DoesNotExist:
                return (self.model(**dict((k, v) \
                    for (k, v) in kwargs.items() if '__' not in k)), True)
        return super(LiveManager, self).get_or_create(*args, **kwargs)
        
    def filter(self, *args, **kwargs):
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED
        kwargs['publish_date__lte'] = datetime.now() 
    
        return super(LiveManager, self).filter(*args, **kwargs) 
        
    def all(self, *args, **kwargs): 
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED 
        kwargs['publish_date__lte'] = datetime.now() 
        return self.filter(*args, **kwargs)
        
        
    def count(self, *args, **kwargs): 
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED 
        kwargs['publish_date__lte'] = datetime.now() 
        return self.filter(*args, **kwargs).count() 
        
    def get(self, *args, **kwargs): 
        kwargs['publish_state'] = PUBLISH_STATE_PUBLISHED 
        kwargs['publish_date__lte'] = datetime.now() 
 
        return super(LiveManager, self).get(*args, **kwargs) 
    
class PublishItem(models.Model): 
    """Basic model for publish/unpublish and date related stuff 
    """ 
    publish_state = models.CharField(
        choices=PUBLISH_STATES,
        max_length=50,
        default=PUBLISH_STATE_PUBLISHED,
        verbose_name=_('publish state')
    )
    
    publish_date  = models.DateTimeField(
        default=datetime.now(),
        verbose_name=_('publish date')
    )
    date_created  = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date created')
    )
    
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date modified')
    ) 
        
    def __init__(self, *args, **kwargs): 
        super(PublishItem, self).__init__(*args, **kwargs) 
        if not self.id: 
             self.publish_date = datetime.now() 
        
    def is_published(self):
        """returns true if the status == published and the datetime.now
        is >= publish_date
        """
        if(
            self.publish_date < datetime.now() and
            self.publish_state == PUBLISH_STATE_PUBLISHED):
            
            return True 
        return False 
 
    is_published.boolean = True 
 
    class Meta(): 
        abstract = True 
 
    objects       = models.Manager() 
    pubjects      = LiveManager() 
