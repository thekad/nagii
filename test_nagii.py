#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

from mako import template as mako_template

import nagii

host_template = nagii.NagiosTemplate(name="generic-host",
    max_check_attempts=1, check_period=5,
    contact_groups="nagiosadmin", notification_interval=5,
    notification_period=960)
host_template._set_type('host')

hosts = []

host_group = nagii.HostGroup(hostgroup_name='all-hosts', alias='all you hosts raise your hands like you don''t care')
host_group2 = nagii.HostGroup(hostgroup_name='all-hosts2', alias='and again')
host_group3 = nagii.HostGroup(hostgroup_name='all-hosts3', alias='and again!')
host_group4 = nagii.HostGroup(hostgroup_name='all-hosts4', alias='and again!')

for i in xrange(1, 10):
    hosts.append(nagii.Host(host_template, host_name="host_%d" % i, alias="Host number %d" % i, address="10.1.100.%d" % i))

[ host_group._add_member(_) for _ in hosts ]
[ host_group2._add_member(_) for _ in hosts ]
for _ in hosts:
    _._add_to_group(host_group4)
    _._add_to_group(host_group3)


contact_template = nagii.NagiosTemplate(name='generic-contact',
    service_notifications_enabled=1,
    host_notifications_enabled=1,
    service_notification_period='24x7',
    host_notification_period='24x7',
    service_notification_options='w,u,c',
    host_notification_options='u',
    service_notification_commands='notify-by-email',
    host_notification_commands='host-notify-by-email')
contact_template._set_type('contact')
contact_template._custom_command = 'boo'

contacts = []

contact_group = nagii.ContactGroup(contactgroup_name='operations', alias='operations peoples')
contact_group2 = nagii.ContactGroup(contactgroup_name='unix-admins', alias='unix admin peoples')

contacts.append(nagii.Contact(contact_template, contact_name='motivator', email='motivator@example.com', pager='1234567890@txt.att.net'))
contacts.append(nagii.Contact(contact_template, contact_name='thekad', email='thekad@example.com', pager='1234567890@tmomail.net'))

[ contact_group._add_member(_) for _ in contacts ]
contacts[0]._add_to_group(contact_group2)


for x in [ host_group, host_group2, host_group3, host_template ] + hosts + [ contact_group, contact_group2, contact_template ] + contacts:
    print x._render()

