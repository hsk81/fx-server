from django.db import models
from django.contrib import auth

class STAMP (models.Model):

    insert_date = models.DateTimeField (auto_now_add = True)
    update_date = models.DateTimeField (auto_now = True)
    delete_date = models.DateTimeField (null = True)

    def __unicode__ (self):
        return "%s" % self.insert_date

class ADDRESS (models.Model):

    class Meta:

        verbose_name_plural = 'addresses'

    line1 = models.CharField (max_length = 256)
    line2 = models.CharField (max_length = 256, blank = True, default = '')
    zip = models.CharField (max_length = 256)
    city = models.CharField (max_length = 256)
    country = models.CharField (max_length = 256)

    def full_address (self, show_blank_line2 = False):

        if show_blank_line2:
            return "%s\n%s\n%s %s\n%s" % (
                self.line1, self.line2, self.zip, self.city, self.country
            )
        else:
            return (self.line2 != "") and (
                "%s\n%s\n%s %s\n%s" % (
                    self.line1, self.line2, self.zip, self.city, self.country
                )
            ) or (
                "%s\n%s %s\n%s" % (
                    self.line1, self.zip, self.city, self.country
                )
            )

    def short_address (self, show_blank_line2 = False):

        if show_blank_line2:
            return "%s\n%s\n%s %s" % (
                self.line1, self.line2, self.zip, self.city
            )
        else:
            return (self.line2 != "") and (
                "%s\n%s\n%s %s" % (self.line1, self.line2, self.zip, self.city)
            ) or (
                "%s\n%s %s" % (self.line1, self.zip, self.city)
            )


    def __unicode__ (self):
        return self.short_address ()

class ACCOUNT (models.Model):

    stamp = models.ForeignKey (STAMP)
    user = models.ForeignKey ('USER', related_name = 'accounts')
    
    def __unicode__ (self):
        return "%s" % self.user

class USER (auth.models.User):

    address = models.ForeignKey (ADDRESS)
    phone = models.CharField (max_length = 256)
    profile = models.CharField (max_length = 256, blank = True, default = '')

    def account (self, account_id):
        return self.accounts.get (id = account_id)

    def full_name (self):        
        return "%s %s" % (self.first_name, self.last_name)

    def __unicode__ (self):
        return self.full_name ()
