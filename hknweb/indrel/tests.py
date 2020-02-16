from django.test import TestCase

from .models import Company, Contact, CompanyLocation

import random
import string

NUM_CONTACT_VALUES = 4
CONTACT_VALUES_NAMES = ['name', 'title', 'phone', 'email']

NUM_COMPANYLOCATION_VALUES = 4
COMPANYLOCATION_VALUES_NAMES = ['address', 'city', 'state', 'zipcode']

NUM_COMPANY_VALUES = 1
COMPANY_VALUES_NAMES = ['company_name']

class ContactTests(TestCase):

    def test_basic_functionality(self):
        contact, args = createContact()
        for name in CONTACT_VALUES_NAMES:
            self.assertEqual(eval('contact.%s' % name), args[name])

class CompanyLocationTests(TestCase):

    def test_basic_functionality(self):
        companyLocation, args = createCompanyLocation()
        for name in COMPANYLOCATION_VALUES_NAMES:
            self.assertEqual(eval('companyLocation.%s' % name), args[name])

class CompanyTests(TestCase):

    def test_basic_functionality(self):
        company, args = createCompany()
        for name in COMPANY_VALUES_NAMES:
            self.assertEqual(eval('company.%s' % name), args[name])

    def test_company_repr_equality(self):
        shared_name = randomString()
        shared_custom_args = {'company_name' : shared_name}
        c1, c2 = createCompany(dict(shared_custom_args)), createCompany(dict(shared_custom_args))
        self.assertEqual(repr(c1), repr(c2))

def randomString(length : int = 10) -> str:
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

def createObject(names : list, object_class, custom_args : dict = {}):
    """
    Creates an object_class object with input fields from custom args
    and random values for the remaining fields.

    Parameters
    ----------
    names : list
        Names of values of the object to create.
    object_class : class
        Class to create. 
    custom_args : dict
        Custom keyword args.

    Returns
    -------
    object : object_class
        Created object_class with specified values.
    args : dict
        The values used to create the object.

    """
    args = {name : randomString() for name in names}
    for key, value in custom_args.items():
        args[key] = value
    return object_class(**args), args

def createCompanyLocation(custom_args : dict = {}) -> CompanyLocation:
    """
    Creates a CompanyLocation with input fields from custom args
    and random values for the remaining fields.

    Parameters
    ----------
    custom_args : dict
        Custom keyword args.

    Returns
    -------
    companyLocation : CompanyLocation
        Created CompanyLocation with specified values.
    args : dict
        The values used to create the CompanyLocation.

    """
    if 'zipcode' not in custom_args:
        custom_args['zipcode'] = int(random.random() * 10e6)
    return createObject(COMPANYLOCATION_VALUES_NAMES, CompanyLocation, custom_args)

def createContact(custom_args : dict = {}) -> Contact:
    """
    Creates a Contact with input fields from custom args
    and random values for the remaining fields.

    Parameters
    ----------
    custom_args : dict
        Custom keyword args.

    Returns
    -------
    contact : Contact
        Created Contact with specified values.
    args : dict
        The values used to create the Contact.

    """
    if 'email' not in custom_args:
        custom_args['email'] = randomString() + '@gmail.com'
    return createObject(CONTACT_VALUES_NAMES, Contact, custom_args)

def createCompany(custom_args : dict = {}) -> Company:
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
    # if 'locations' not in custom_args:
    #     custom_args['locations'] = [createCompanyLocation() for _ in range(3)]
    # if 'contacts' not in custom_args:
    #     custom_args['contacts'] = [createContact() for _ in range(3)]
    return createObject(COMPANY_VALUES_NAMES, Company, custom_args)


