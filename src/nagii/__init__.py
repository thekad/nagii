#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8
#
# Nagii python modelling library for Nagios
# Copyright 2011, Jorge Gallegos <kad@blegh.net>

VERSION='0.1.1'


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
        public and custom attributes for this object.
        Something like dir() but awesomer
        """
        public = []

        for _ in dir(self):
            if not _.startswith('_'):
                public.append((_, getattr(self, _)))
            elif _.startswith('_custom'):
                public.append((_[7:], getattr(self, _)))

        return dict(public)

    def _get_required(self):
        """
        Helper method to get the list of required
        fields, nothing fancy
        """
        return self._required

    def _add_member(self, *args, **kwargs):
        """
        Helper method to add members to this group
        """
        raise NotImplementedError

    def _add_to_group(self, *args, **kwargs):
        """
        Helper method to add groups to this object
        """
        raise NotImplementedError

    def _add_custom(self, var, val):
        """
        Helper method to add custom variables to this object
        """
        var = "_custom" + var
        setattr(self,var,val)

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
    register = 0

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
        if 'members' in kwargs.keys():
            raise ValueError('You don''t add members as keywords, '
                'you use the _add_member(obj) method')
        NagiosObject.__init__(self, *args, **kwargs)

    def _add_member(self, member):
        assert isinstance(member, self._member_class), \
            'Member "%s" is not a "%s"' % (member, self._member_class)
        if member not in self._members:
            setattr(self, '_members', self._members + [ member ])
            setattr(self, 'members', ','.join(sorted([ _._name for _ in self._members ])))

    def _get_members(self):
        return _members


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
    _servicegroups = []

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.service_description

    def _add_to_group(self, servicegroup):
        if servicegroup not in self._servicegroups:
            setattr(self, '_servicegroups',
                self._servicegroups + [ servicegroup ])
            setattr(self, 'servicegroups',
                ','.join(sorted([ _._name for _ in self._servicegroups ])))


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
    _hostgroups = []

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.host_name

    def _add_to_group(self, hostgroup):
        if hostgroup not in self._hostgroups:
            setattr(self, '_hostgroups',
                self._hostgroups + [ hostgroup ])
            setattr(self, 'hostgroups',
                ','.join(sorted([ _._name for _ in self._hostgroups ])))


class Contact(NagiosObject):
    """
    Nagios contact object
    """

    _required = [
        'contact_name',
        'host_notifications_enabled',
        'service_notifications_enabled',
        'host_notification_period',
        'service_notification_period',
        'host_notification_options',
        'service_notification_options',
        'host_notification_commands',
        'service_notification_commands',
    ]
    _type = 'contact'
    _contactgroups = []

    def __init__(self, *args, **kwargs):
        NagiosObject.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.contact_name

    def _add_to_group(self, contactgroup):
        if contactgroup not in self._contactgroups:
            setattr(self, '_contactgroups',
                self._contactgroups + [ contactgroup ])
            setattr(self, 'contactgroups',
                ','.join(sorted([ _._name for _ in self._contactgroups ])))


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


class ContactGroup(NagiosGroup):
    """
    Contact group object
    """

    _required = [
        'contactgroup_name',
        'alias',
    ]
    _type = 'contactgroup'
    _member_class = Contact

    def __init__(self, *args, **kwargs):
        NagiosGroup.__init__(self, *args, **kwargs)

    def _set_name(self):
        self._name = self.contactgroup_name


