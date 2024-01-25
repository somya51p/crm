from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
from .managers import UserManager

from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'admin'),
        ('user', 'user'),
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    Login_Options = (
        ("Google" , 'Google'),
        ("Facebook" , 'Facebook'),
        ("GitHub" , 'GitHub'),
    )
    

    email = models.EmailField(_('email address'), null=False, blank=False,unique=True)
    username = models.CharField(_('username'), null=True, blank=True, default='', max_length=50)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
   # country_code = models.CharField(_('Contact phone number'), max_length=13, unique=True)
    mobile = models.CharField(_('Contact phone number'), max_length=13)
    birth_date = models.DateField(null=True)
    role = models.CharField(max_length=20, blank=True, choices=USER_TYPES, default='')
    login_type = models.CharField(max_length=20, blank=True, choices=Login_Options, default='')
    gender = models.CharField(max_length=20, blank=True, choices=GENDER, default='')
    objects = UserManager()
    groups = models.ManyToManyField(Group,verbose_name=_('groups'),blank=True,help_text=_('The groups this user belongs to.'),related_name='vyoga_user' )
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, help_text=_('Specific permissions for this user.'),related_name='vyoga_user_permission' )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_balance(self):
        if self.wallet:
            return self.wallet.wallet_amount

    def is_balance_sufficient(self, purchase_amount):
        '''
        Check if user have sufficient balance in wallet.
        '''
        if self.wallet.wallet_amount < purchase_amount:
            return False
        return True

    def is_reward_sufficient(self, purchase_amount):
        '''
        Check if user have sufficient balance in wallet.
        '''
        if self.rewardpoint.reward_amount < purchase_amount:
            return False
        return True

    def deduct_balance(self, purchase_amount,  description, additional_details):
        '''
        Deduct balance from user's wallet.
        '''
        escription = description
        self.wallet.wallet_amount = float("{:.2f}".format(self.wallet.wallet_amount - purchase_amount))
        self.wallet.save()
        return self.wallet.create_wallet_history(purchase_amount, escription, additional_details)

    def deduct_rewards(self, purchase_amount,  description, additional_details):
        '''
        Deduct balance from user's wallet.
        '''
        self.rewardpoint.reward_amount = self.rewardpoint.reward_amount - purchase_amount
        self.rewardpoint.save()
        return self.rewardpoint.create_reward_history(purchase_amount, description, additional_details)

    def add_balance(self, amount, txnid,description = 'Wallet Recharge'):
        '''
        Deduct balance from user's wallet.
        '''
        self.wallet.wallet_amount = self.wallet.wallet_amount + float(amount)
        self.wallet.save()
        return self.wallet.create_wallet_history(amount, description, txnid, 'Credit')
    
    def get_all_address(self):
        addresses = self.user_address.filter(is_active = True)
        if addresses:
            return addresses
        else:
            return False


class UserAddress(models.Model):
    user =  models.ForeignKey(User, default='', null=True,blank=True, related_name='user_address',on_delete=models.CASCADE)
    phone_no =  models.CharField(max_length=12,null=True,blank=True, default='')
    house_no =  models.CharField(max_length=100,null=True,blank=True, default='')
    locality =  models.CharField(max_length=100,null=True,blank=True, default='')
    lat =  models.CharField(max_length=100,null=True,blank=True, default='')
    lng =  models.CharField(max_length=100,null=True,blank=True, default='')
    landmark =  models.CharField(max_length=100,null=True,blank=True, default='')
    district =  models.CharField(max_length=100,null=True,blank=True, default='')
    state =  models.CharField(max_length=100,null=True,blank=True, default='')
    country =  models.CharField(max_length=100,null=True,blank=True, default='')
    pincode =  models.CharField(max_length=6,null=True,blank=True, default='')
    full_address =  models.TextField(null=True,blank=True, default='')
    created_date =  models.DateTimeField( auto_now_add=True)
    is_active =  models.BooleanField(_('active'), default=True)

    def __str__(self):
        return str(self.full_address) + "( "+str(self.user) + ")"