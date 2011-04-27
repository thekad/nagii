#!/usr/bin/env python
#
# -*- mode: python; sh-basic-offset: 4; indent-tabs-mode: nil; coding: utf-8 -*-
# vim: tabstop=4 softtabstop=4 expandtab shiftwidth=4 fileencoding=utf-8

import nagii

template = nagii.Host(host_name="", alias="Foo Host",
    address="10.1.100.1", max_check_attempts=1, check_period=5,
    contact_groups="nagiosadmin", notification_interval=5,
    notification_period=960)

host = nagii.Host(template, host_name="foo_host", alias="Stoopid")

print template.max_check_attempts
print host.alias
print host.contact_groups
print template._public()
print host._public()

