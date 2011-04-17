from django.db import models

class Attribute (models.Model):

    key = models.CharField (max_length=32)
    value = models.CharField (max_length=256)

    def __unicode__(self):
        return "%s: %s" % (self.key, self.value)
