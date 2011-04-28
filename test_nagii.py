#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

from mako import template as mako_template

import nagii

tpl = """
define ${obj._type} {
%   for k,v in obj._public().items():
    ${"%-40s%s" % (k,v)}
%   endfor
}
"""

host_template = nagii.NagiosTemplate(name="generic-host",
    max_check_attempts=1, check_period=5,
    contact_groups="nagiosadmin", notification_interval=5,
    notification_period=960)
host_template._set_type('host')

hosts = []

host_group = nagii.HostGroup(hostgroup_name='all-hosts', alias='all you hosts raise your hands like you don''t care')

for i in xrange(1, 10):
    hosts.append(nagii.Host(host_template, host_name="host_%d" % i, alias="Host number %d" % i, address="10.1.100.%d" % i))

[ host_group._add_member(_) for _ in hosts ]
tpl = mako_template.Template(tpl)
for x in [ host_group, host_template ] + hosts:
    print tpl.render(obj=x)

