activemq-rpm
================

Spec and sources to build activemq 5.9.1 binary.

Forked from https://github.com/kscherer/activemq-rpm

To build the source and binary rpm, the rpmbuild tool is necessary

    sudo yum install rpm-build

To build in a local dir:

    rpmbuild --define '_topdir '`pwd` -ba SPECS/activemq.spec

To install in different location:

    rpm -i --prefix=/var/dhlnl/activemq activemq-5.9.1-1.el6.noarch.rpm

