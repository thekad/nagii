#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

VERSION='0.1'


class NagiosObject(object):
    """
    The base object that all the rest of the objects inherit from
    """

    _required = []
    _name = ''
    _parent = None
    _type = None

    def __init__(self, *args, **kwargs):
#       If we send the parent object, _must_ be the
#       first unnamed item
        if args:
            self._parent = args[0]
            kwargs['use'] = self._parent.name
#       Set attributes
        for k,v in kwargs.items():
            setattr(self, k, v)

        self._validate_attributes()
        self._set_name()

    def _validate_attributes(self):
        """
        Validates the required list (self._required)
        against the actual object (possibly inherited)
        values of this object
        """
        for required in self._required:
            req = set(required.split('|'))
            fail = True
            for r in req:
                try:
                    x = getattr(self, r)
                    if x is not None:
                        fail = False
                        break
                except AttributeError:
                    pass
            if fail:
                reason = 'Failed at "%s"' % required
                raise AttributeError('The object is incomplete: %s' % reason)

    def _set_name(self):
        """
        Sets the name string for this object,
        should be overloaded in all child objects
        """
        pass

    def _public(self):
        """
        Returns a dictionary with the (what I consider)
        public attributes for this object. Something
        like dir() but awesomer
        """
        p = [(_, getattr(self, _)) for _ in dir(self) if not _.startswith('_')]
        return dict(p)

    @classmethod
    def _get_required(self):
        """
        Helper method to get the list of required
        fields, nothing fancy
        """
        return self._required

    def __getattr__(self, attr):
        """
        So this is kinda tricky. This method only
        gets called when __getattribute__ fails,
        that is, if the method doesn't exist in this
        object's scope. However if set a parent
        object, we should try and return the parent
        object's value
        """
        if self._parent:
            return getattr(self._parent, attr)
        else:
            raise AttributeError


class NagiosTemplate(NagiosObject):
    """
    A simple nagios template object, only thing required
    should be the name of this object
    """

    _required = [ 'name' ]

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _set_type(self, stype):
        self._type = stype


class NagiosGroup(NagiosObject):
    """
    Base nagios group object, improves upon 
    NagiosObject by adding member adding support
    """

    _members = []
    _member_class = NagiosObject

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _add_member(self, member):
        assert isinstance(member, self._member_class), \
            'Member "%s" is not a "%s"' % (member, self._member_class)
        if member not in self._members:
            self._members.append(member)

    def _get_members(self):
        pass


class Service(NagiosObject):
    """
    Nagios service object
    """

    _required = [
        'host_name|hostgroup_name',
        'service_description',
        'check_command',
        'max_check_attempts',
        'check_interval',
        'retry_interval',
        'check_period',
        'notification_interval',
        'notification_period',
        'contacts|contact_groups',
    ]
    _type = 'service'

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.service_description


class Host(NagiosObject):
    """
    Nagios host object
    """

    _required = [
        'host_name',
        'alias',
        'address',
        'max_check_attempts',
        'check_period',
        'contacts|contact_groups',
        'notification_interval',
        'notification_period',
    ]
    _type = 'host'

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.host_name


class ServiceGroup(NagiosGroup):
    """
    Service group object
    """

    _required = [
        'servicegroup_name',
        'alias',
    ]
    _type = 'servicegroup'
    _member_class = Service

    def __init__(self, *args, **kwargs):
        NagiosGroup.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.servicegroup_name


class HostGroup(NagiosGroup):
    """
    Host group object
    """

    _required = [
        'hostgroup_name',
        'alias',
    ]
    _type = 'hostgroup'
    _member_class = Host

    def __init__(self, *args, **kwargs):
        NagiosGroup.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.hostgroup_name

