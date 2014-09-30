%define rhel_version 5.9.1
%define rhel_name activemq
%define project_id 7p
%define dpag_prefix /home/dpag%{project_id}
%define dpag_name c0%{project_id}_%{rhel_name}
%define package_prefix %{dpag_prefix}/%{dpag_name}

# y7pbamp:uni7pamq
%define username  y%{project_id}bamq
%define usergroup uni%{project_id}amq

%define homedir %{package_prefix}
%define libdir %{package_prefix}/lib
%define datadir %{package_prefix}/data
%define docsdir %{package_prefix}/docs

#Avoid doing arcane stuff with jars, silly rpm
%define __jar_repack %{nil}

Summary: Apache ActiveMQ
Name: %{dpag_name}
Prefix: %{package_prefix}
Version: 05.09.01
Release: 00
License: ASL 2.0
URL: http://activemq.apache.org/
Group: System Environment/Daemons
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch

Requires(pre): /usr/sbin/useradd
#Requires: tanukiwrapper >= 3.5.9

Provides: %{dpag_name} = %{rhel_version}

Source0: http://www.apache.org/dist//activemq/apache-activemq/%{rhel_version}/apache-activemq-%{rhel_version}-bin.tar.gz
#Source1: activemq.init.rh
Source2: activemq.xml
Source3: activemq.log4j.properties
Source4: activemq.jetty.xml
Source5: activemq.credentials.properties
Source6: activemq.jetty-realm.properties
Source7: activemq-wrapper.conf
Source8: postgresql-9.3-1102.jdbc4.jar
Source9: activemq-broker.ks





%description
ApacheMQ is a JMS Compliant Messaging System

%pre
getent group %{usergroup} >/dev/null || groupadd %{usergroup}
mkdir -p %{package_prefix}%{contentdir}
getent passwd %{username} >/dev/null || \
  useradd -g %{usergroup} -M -s /sbin/nologin \
    -d %{package_prefix}%{contentdir} -c "DPAG PI ActiveMQ" %{username}
chown %{username}:%{usergroup} %{package_prefix}%{contentdir}
exit 0



%prep
%setup -q -n apache-activemq-%{version}

%build


%install
rm -rf $RPM_BUILD_ROOT


install --directory ${RPM_BUILD_ROOT}
install --directory ${RPM_BUILD_ROOT}%{homedir}
install --directory ${RPM_BUILD_ROOT}%{homedir}%{_bindir}
install --directory ${RPM_BUILD_ROOT}%{docsdir}
install --directory ${RPM_BUILD_ROOT}%{libdir}
install --directory ${RPM_BUILD_ROOT}%{homedir}/webapps
install --directory ${RPM_BUILD_ROOT}%{datadir}
install --directory ${RPM_BUILD_ROOT}%{datadir}/data
install --directory ${RPM_BUILD_ROOT}%{homedir}/log/%{name}
install --directory ${RPM_BUILD_ROOT}%{homedir}/run/%{name}
install --directory ${RPM_BUILD_ROOT}%{homedir}/conf
#install --directory ${RPM_BUILD_ROOT}%{_initrddir}

# Config files
install %{_sourcedir}/activemq.xml ${RPM_BUILD_ROOT}/%{homedir}/conf/activemq.xml
install %{_sourcedir}/activemq-wrapper.conf ${RPM_BUILD_ROOT}/%{homedir}/conf/activemq-wrapper.conf
install %{_sourcedir}/activemq.credentials.properties ${RPM_BUILD_ROOT}/%{homedir}/conf/credentials.properties
install %{_sourcedir}/activemq.jetty.xml ${RPM_BUILD_ROOT}/%{homedir}/conf/jetty.xml
install %{_sourcedir}/activemq.log4j.properties ${RPM_BUILD_ROOT}/%{homedir}/conf/log4j.properties
install %{_sourcedir}/activemq.jetty-realm.properties ${RPM_BUILD_ROOT}/%{homedir}/conf/jetty-realm.properties

# SSL Server certificate
install %{_sourcedir}/activemq-broker.ks  ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{_name}/activemq-broker.ks

# lib file for postgresql jdbc driver
install %{_sourcedir}/postgresql-9.3-1102.jdbc4.jar ${RPM_BUILD_ROOT}/%{libdir}/postgresql-9.3-1102.jdbc4.jar


# startup script
#install bin/activemq ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
#install %{_sourcedir}/activemq.init.rh ${RPM_BUILD_ROOT}%{_initrddir}/%{name}
# Bin and doc dirs
install *.txt ${RPM_BUILD_ROOT}%{docsdir}
#install *.html ${RPM_BUILD_ROOT}%{docsdir}
#cp -r docs ${RPM_BUILD_ROOT}%{docsdir}

#Install our custom launcher script:
install %{_sourcedir}/start-activemq-console ${RPM_BUILD_ROOT}/%{homedir}/bin
# note that we should still search replace DEFAULTPREFIX with whatever prefix is during build.
# INSTALLPREFIX

install bin/activemq.jar \
            bin/activemq-admin \
            bin/activemq \
        ${RPM_BUILD_ROOT}%{homedir}/bin

#install --directory ${RPM_BUILD_ROOT}%{_bindir}
#%{__ln_s} -f %{homedir}/bin/activemq-admin ${RPM_BUILD_ROOT}%{_bindir}

# Runtime directory
cp -r lib/* ${RPM_BUILD_ROOT}%{libdir}
cp -r webapps/admin ${RPM_BUILD_ROOT}%{homedir}/webapps



%post
# install activemq (but don't activate)
#/sbin/chkconfig --add %{name}
echo "Installed activemq under ${RPM_INSTALL_PREFIX}"
# Correct paths in start script

#First we need to escape all the slashes in the prefix path:
ESCAPED_PREFIX=$(echo ${RPM_INSTALL_PREFIX}| sed -e 's/\\/\\\\/g' -e 's/\//\\\//g' -e 's/&/\\\&/g')

#Now correct the paths in the istart  script
sed -i s/PREFIX/$ESCAPED_PREFIX/g ${RPM_INSTALL_PREFIX}/bin/start-activemq-console

%preun
#if [ $1 = 0 ]; then
#    [ -f /var/lock/subsys/%{name} ] && %{_initrddir}/%{name} stop
#    [ -f %{_initrddir}/%{name} ] && /sbin/chkconfig --del %{name}
#fi

%postun

%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-,%{username},%{usergroup})
%dir %{package_prefix}
#%{homedir}/webapps
#%{homedir}/log
#%{homedir}/conf
#%docdir %{docsdir}
#%{docsdir}
#%{libdir}
#%attr(775,activemq,activemq) %dir %{_localstatedir}/log/%{name}
#%attr(775,activemq,activemq) %dir %{_localstatedir}/run/%{name}
#%attr(755,activemq,activemq) %dir %{datadir}/data
#%attr(755,root,root) %{_initrddir}/%{name}
#%config(noreplace) %{_sysconfdir}/%{_name}/activemq.xml
#%config(noreplace) %{_sysconfdir}/%{_name}/activemq-wrapper.conf
#%config(noreplace) %attr(750,root,activemq) %{_sysconfdir}/%{_name}/credentials.properties
#%config(noreplace) %{_sysconfdir}/%{_name}/jetty.xml
#%config(noreplace) %{_sysconfdir}/%{_name}/jetty-realm.properties
#%config(noreplace) %{_sysconfdir}/%{_name}/log4j.properties

%changelog
* Tue Sep 09 2014 Thomas Ferris Nicolaisen * <thomas.nicolaisen@viaboxx.de> - 5.9.1
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
