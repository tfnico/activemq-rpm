%define rhel_version 5.9.1
%define rhel_name activemq
%define project_id 7p
%define dpag_prefix /home/dpag%{project_id}
%define dpag_name c0%{project_id}_%{rhel_name}
%define package_prefix %{dpag_prefix}/%{dpag_name}

# y7pbamp:uni7pamq
%define username  y%{project_id}bamq
%define usergroup uni%{project_id}amq
%define userid 536392
%define groupid 536393


#Avoid doing arcane stuff with jars, silly rpm
%define __jar_repack %{nil}

Summary: Apache ActiveMQ
Name: %{dpag_name}
Prefix: %{package_prefix}
Version: 05.09.01
Release: 00
License: ASL 2.0
Group: System Environment/Daemons
URL: http://activemq.apache.org/
Source: http://www.apache.org/dist/activemq/apache-activemq/%{rhel_version}/apache-activemq-%{rhel_version}-bin.tar.gz
#Source1: activemq.init.rh

Requires(pre): /usr/sbin/useradd
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/usermod
Requires: sudo
#Requires: tanukiwrapper >= 3.5.9
Requires: jdk
Provides: %{rhel_name} = %{rhel_version}

Source2: activemq.xml
Source3: activemq.log4j.properties
Source4: activemq.jetty.xml
Source5: activemq.credentials.properties
Source6: activemq.jetty-realm.properties
#Source7: activemq-wrapper.conf
BuildArch: noarch
Source8: postgresql-9.3-1102.jdbc4.jar
Source9: activemq-broker.ks
Source10: activemq.default
Source11: activemq.init
Source12: activemq.sudoers
Patch1: activemq.defaultfile-patch

%define homedir %{package_prefix}%{_prefix}/%{rhel_name}
%define libdir %{homedir}/lib
%define datadir %{package_prefix}/var/cache/%{rhel_name}
%define docsdir %{package_prefix}/usr/share/doc/%{rhel_name}-%{version}

%description
ApacheMQ is a JMS Compliant Messaging System

%pre
getent group %{usergroup} >/dev/null || groupadd -g %{groupid} %{usergroup}
mkdir -p %{package_prefix}
getent passwd %{username} >/dev/null || \
  useradd -u %{userid} -g %{usergroup} -M -s /bin/bash \
    -d %{package_prefix} -c "DPAG PI ActiveMQ" %{username}

# add maintenance group and user
getent group uni7pwar  >/dev/null || groupadd -g 536399 uni7pwar
getent passwd y7pbwar >/dev/null || \
	useradd -u 536398 -g uni7pwar -M -s /bin/bash -d /home/dpag7p -c "DPAG PI Maintenance User" y7pbwar
usermod -a -G %{usergroup} y7pbwar

%prep
%setup -q -n apache-activemq-%{rhel_version}
%patch1 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
install --directory ${RPM_BUILD_ROOT}
install --directory ${RPM_BUILD_ROOT}%{package_prefix}%{_bindir}
install --directory ${RPM_BUILD_ROOT}%{homedir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/bin
install --directory ${RPM_BUILD_ROOT}%{docsdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/webapps
install --directory ${RPM_BUILD_ROOT}%{datadir}
install --directory ${RPM_BUILD_ROOT}%{datadir}/data
install --directory ${RPM_BUILD_ROOT}%{package_prefix}%{_localstatedir}/log/%{rhel_name}
install --directory ${RPM_BUILD_ROOT}%{package_prefix}%{_localstatedir}/run/%{rhel_name}
install --directory ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}
install --directory ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/default
install --directory ${RPM_BUILD_ROOT}%{_initrddir}
install --directory ${RPM_BUILD_ROOT}%{_sysconfdir}/sudoers.d
install --directory ${RPM_BUILD_ROOT}%{homedir}/tmp

# Config files
install %{SOURCE2} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/activemq.xml
install %{SOURCE3} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/log4j.properties
install %{SOURCE4} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/jetty.xml
install %{SOURCE5} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/credentials.properties
install %{SOURCE6} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/jetty-realm.properties
#install %{SOURCE7} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/activemq-wrapper.conf


# lib file for postgresql jdbc driver
install %{SOURCE8} ${RPM_BUILD_ROOT}%{libdir}

# SSL Server certificate
install %{SOURCE9} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/%{rhel_name}/activemq-broker.ks

# ActiveMQ default file
install %{SOURCE10} ${RPM_BUILD_ROOT}%{package_prefix}%{_sysconfdir}/default/activemq

# startup script
#install bin/activemq ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
install -m 755 %{SOURCE11} ${RPM_BUILD_ROOT}%{_initrddir}/%{rhel_name}

install -m 600 %{SOURCE12} ${RPM_BUILD_ROOT}%{_sysconfdir}/sudoers.d/activemq

# Bin and doc dirs
install *.txt ${RPM_BUILD_ROOT}%{docdir}
#install *.html ${RPM_BUILD_ROOT}%{package_prefix}/docs
#cp -r docs ${RPM_BUILD_ROOT}%{package_prefix}/docs


#Install our custom launcher script:
install bin/activemq.jar  ${RPM_BUILD_ROOT}%{homedir}/bin
install bin/activemq-admin ${RPM_BUILD_ROOT}%{homedir}/bin
install bin/activemq  ${RPM_BUILD_ROOT}%{homedir}/bin
%{__ln_s} %{homedir}/bin/activemq-admin ${RPM_BUILD_ROOT}%{package_prefix}%{_bindir}
%{__ln_s} %{package_prefix}%{_sysconfdir} ${RPM_BUILD_ROOT}%{homedir}%{_sysconfdir}

# Runtime directory
cp -r lib/* ${RPM_BUILD_ROOT}%{libdir}
cp -r webapps/admin ${RPM_BUILD_ROOT}%{homedir}/webapps

%post
# install activemq (but don't activate)
/sbin/chkconfig --add %{rhel_name}

%preun
#if [ $1 = 0 ]; then
#    [ -f %{package_prefix}/var/lock/subsys/%{rhel_name} ] && %{_initrddir}/%{rhel_name} stop
#    [ -f %{_initrddir}/%{name} ] && /sbin/chkconfig --del %{name}
#fi
/sbin/chkconfig --del %{rhel_name}

%postun
/bin/find %{package_prefix} -depth -type d -exec rmdir --ignore-fail-on-non-empty {} \;

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%attr(755,root,root) %{package_prefix}%{_bindir}/activemq-admin
%{homedir}
%docdir %{docsdir}
%{docsdir}
%attr(775,%{username},%{usergroup}) %dir %{package_prefix}%{_localstatedir}/log/%{rhel_name}
%attr(775,%{username},%{usergroup}) %dir %{package_prefix}%{_localstatedir}/run/%{rhel_name}
%attr(755,%{username},%{usergroup}) %dir %{datadir}/data
%attr(750,%{username},%{usergroup}) %dir %{homedir}/tmp
%config %{package_prefix}%{_sysconfdir}/%{rhel_name}/activemq.xml
#%config %{package_prefix}%{_sysconfdir}/%{rhel_name}/activemq-wrapper.conf
%config %attr(640,root,%{usergroup}) %{package_prefix}%{_sysconfdir}/%{rhel_name}/credentials.properties
%config %{package_prefix}%{_sysconfdir}/%{rhel_name}/jetty.xml
%config %{package_prefix}%{_sysconfdir}/%{rhel_name}/jetty-realm.properties
%config %{package_prefix}%{_sysconfdir}/%{rhel_name}/log4j.properties
%config %{package_prefix}%{_sysconfdir}/%{rhel_name}/activemq-broker.ks
%config %{package_prefix}%{_sysconfdir}/default/activemq
%{_initrddir}/%{rhel_name}
%{_sysconfdir}/sudoers.d/activemq

%changelog
* Tue Sep 09 2014 Thomas Ferris Nicolaisen * <thomas.nicolaisen@viaboxx.de> - 05.09.01-00
- Update to activemq 5.9.1
- Made relocatable
- Remove tanukiwrapper dependency (launch as standalone dist)

* Thu Jun 28 2012 Matthaus Litteken <matthaus@puppetlabs.com> - 5.6.0-2.pe
- Update activemq.jetty.xml to 5.6.0 for changed classnames

* Thu Jun 21 2012 Moses Mendoza <moses@puppetlabs.com> - 5.6.0-1.pe
- Update activemq to version 5.6.0

* Wed Mar 21 2012 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-7.pe
- Ensure admin interface is only listening on localhost

* Thu Oct 27 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-6.5.pe
- Update ActiveMQ configuration

* Thu Oct 27 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-6.4.pe
- Don't explicitly depend on java

* Thu Sep 15 2011 Matthaus Litteken <matthaus@puppetlabs.com> - 5.5.0-6.3.pe
- Init script fixed to recreate /var/run/activemq as needed.

* Thu Sep 15 2011 Matthaus Litteken <matthaus@puppetlabs.com> - 5.5.0-6.2.pe
- Init script fixed to give user a shell.

* Thu Sep 15 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-5.1.pe
- Init script typo fixed

* Wed Sep 07 2011 Michael Stahnke <stahnma@puppetlabs.com> - 5.5.0-5.pe
- Useradd no longer specifies a uid

* Fri Aug 19 2011 Matthaus Litteken <matthaus@puppetlabs.com> 5.5.0-4.pe
- Updated group and permissions on datadir. Bumped release to 4.

* Thu Aug 18 2011 Matthaus Litteken <matthaus@puppetlabs.com> 5.5.0-3
- Bumped release to 3 for PE 1.2.

* Thu May 12 2011 Ken Barber <ken@puppetlabs.com> 5.5.0-2
- Updated to 5.5.0. Adapted to PE.

* Sat Jan 16 2010 R.I.Pienaar <rip@devco.net> 5.3.0-1
- Adjusted for ActiveMQ 5.3.0

* Wed Oct 29 2008 James Casey <james.casey@cern.ch> 5.2.0-2
- fixed defattr on subpackages

* Tue Sep 02 2008 James Casey <james.casey@cern.ch> 5.2.0-1
- Upgraded to activemq 5.2.0

* Tue Sep 02 2008 James Casey <james.casey@cern.ch> 5.1.0-7
- Added separate logging of messages whenever the logging interceptor is enabled in the config file
- removed BrokerRegistry messages casued by REST API
- now we don't log messages to stdout (so no duplicates in wrapper log).
- upped the number and size of the rolling logs

* Fri Aug 29 2008 James Casey <james.casey@cern.ch> 5.1.0-6
- make ServiceData be correct LDIF

* Wed Aug 27 2008 James Casey <james.casey@cern.ch> 5.1.0-5
- changed glue path from mds-vo-name=local to =resource

* Tue Aug 05 2008 James Casey <james.casey@cern.ch> 5.1.0-4
- fixed up info-provider to give both REST and STOMP endpoints

* Mon Aug 04 2008 James Casey <james.casey@cern.ch> 5.1.0-3
- reverted out APP_NAME change to ActiveMQ from init.d since it
  causes too many problems
* Mon Aug 04 2008 James Casey <james.casey@cern.ch> 5.1.0-2
- Added info-provider
- removed mysql as a requirement

* Thu Mar 20 2008 Daniel RODRIGUES <daniel.rodrigues@cern.ch> - 5.1-SNAPSHOT-1
- Changed to version 5.1 SNAPSHOT of 18 Mar, fizing AMQ Message Store
- small fixes to makefile

* Fri Dec 14 2007 James CASEY <james.casey@cern.ch> - 5.0.0-3rc4
- Added apache config file to forward requests to Jetty

* Thu Dec 13 2007 James CASEY <james.casey@cern.ch> - 5.0.0-2rc4
- fixed /usr/bin symlink
- added useJmx to the default config

* Thu Dec 13 2007 James CASEY <james.casey@cern.ch> - 5.0.0-RC4.1
- Moved to RC4 of the 5.0.0 release candidates

* Mon Dec 10 2007 James CASEY <james.casey@cern.ch> - 5.0-SNAPSHOT-7
- added symlink in /usr/bin for activemq-admin

* Mon Nov 26 2007 James CASEY <james.casey@cern.ch> - 5.0-SNAPSHOT-6
- fix bug with group name setting in init.d script

* Mon  Nov 26 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-5
- fix typos in config file for activemq

* Mon Nov 26 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-4
- add support for lib64 version of tanukiwrapper in config
- turned off mysql persistence in the "default" config

* Wed Oct 17 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-2
- more re-org to mirror how tomcat is installed.
- support for running as activemq user

* Tue Oct 16 2007 James CASEY <jamesc@lxb6118.cern.ch> - 5.0-SNAPSHOT-1
- Initial Version
