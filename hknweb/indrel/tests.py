from django.test import TestCase

from .models import Company

from inspect import getargspec
import random
import string

NUM_COMPANY_VALUES = 9
COMPANY_VALUES_NAMES = ['company_name', 'address_1', 'city', 'state',\
                        'zipcode', 'contact_name', 'contact_title', 'contact_phone', 'contact_email']

class CompanyTests(TestCase):

    def test_basic_functionality(self):
        company, args = createCompany()
        for name in COMPANY_VALUES_NAMES:
            self.assertEqual(eval('company.%s' % name), args[name])

    def test_company_repr_equality(self):
        pass

def randomString(length : int = 10):
    """
    Creates a random string of characters of input length.

    Parameters
    ----------
    length : int
        Length of the output random string.

    Returns
    -------
    randstring : str
        Random string of letters of input length.

    """
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def createCompany(custom_args : dict = {}):
    """
    Creates a Company with input fields from custom args
    and random values for the remaining fields.

    Parameters
    ----------
    custom_args : dict
        Custom keyword args.

    Returns
    -------
    company : Company
        Created Company with specified values.
    args : dict
        The values used to create the company.

    """
    args = {name : randomString() for name in COMPANY_VALUES_NAMES}
    args['zipcode'] = int(random.random() * 10e6)
    args['contact_email'] += '@gmail.com'
    for key, value in custom_args.items():
        args[key] = value
    return Company(**args), args


