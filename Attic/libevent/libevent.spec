%global develdocdir %{_docdir}/%{name}-devel

Name:           libevent
Version:        2.1.11
Release:        1qsecofr
Summary:        Abstract asynchronous event notification library

# arc4random.c, which is used in build, is ISC. The rest is BSD.
License:        BSD and ISC
URL:            http://libevent.org/
Source0:        https://github.com/libevent/libevent/releases/download/release-%{version}-stable/libevent-%{version}-stable.tar.gz
Patch0:         libevent-py3.patch

# Disable network tests

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. libevent is meant to replace the asynchronous event
loop found in event driven network servers. An application just needs
to call event_dispatch() and can then add or remove events dynamically
without having to change the event loop.

%package devel
Summary: Development files for %{name}
License: BSD
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3

%description devel
This package contains the header files and libraries for developing
with %{name}.

%package doc
Summary: Development documentation for %{name}
# The files sample/openssl_hostname_validation.{c,h} and sample/hostcheck.{c,h}
# are MIT. The rest is BSD.
License: BSD and MIT
BuildArch: noarch

%description doc
This package contains the development documentation for %{name}.

%prep
%setup -q -n libevent-%{version}-stable
%patch0 -p1

%build

autoreconf -fiv .
%configure \
    LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static
%make_build

%install

%make_install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Tests fail due to nameserver not running locally
# [msg] Nameserver 127.0.0.1:38762 has failed: request timed out.
# On some architects this error is ignored on others it is not.
#make check

%files
%defattr(-, qsys, *none)
%license LICENSE
%doc ChangeLog README.md
%{_libdir}/libevent*.so.*

%files devel
%defattr(-, qsys, *none)
%{_includedir}/*.h
%{_includedir}/event2/*.h
%{_libdir}/libevent*.so
%{_libdir}/pkgconfig/*.pc
%{_bindir}/event_rpcgen.*


%changelog
* Sun Mar 1 2020 Calvin Buckley <calvin@cmpct.info> - 2.1.11-1qsecofr
- Bump and add to git
- Python3 patch from Alpine/Adelie
- Use modern i RPM conventions, including...
- Switch to Rochester svr4 sonames. This may be breaking.

* Thu Nov 22 2018 Yvan Janssens <qsecofr@qseco.fr> - 2.1.8-6
- Modified for use on IBM i.

* Mon Sep 03 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.1.8-4
- Corrected the License tag
- Resolves: rhbz#1624851

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Steve Dickson <steved@redhat.com> - 2.1.8-2
- Explicitly express SONAME in the %%file section

* Thu Feb 15 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.8-1
- Fix ownership of pkg-config files
- Remove unneeded Group tag

* Wed Feb 14 2018 Steve Dickson <steved@redhat.com> - 2.1.8-0
- Updated to the latest upstream release 2.1.8 (bz 1418488)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.22-7
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 12 2017 Nils Philippsen <nils@redhat.com> - 2.0.22-4
- don't build doxygen documentation during modular build

* Mon Mar 27 2017 Tomáš Mráz <tmraz@redhat.com> - 2.0.22-3
- Make it build with OpenSSL-1.1.0, cherry-picked from upstream git

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 24 2016 Orion Poplawski <orion@cora.nwra.com> - 2.0.22-1
- Update to 2.0.22
- Spec cleanup, new URL
- Support multilib devel (bug #477685)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 2.0.21-4
- Fix -doc package for F20 UnversionedDocDirs (#993956)
- Add missing directory /usr/include/event2
- Fix directory ownership in -doc package
- Correct summary and description of -devel and -doc packages
- Set -doc package Group tag to "Documentation"
- Add %%?_isa to -devel package base dependency
- Remove %%defattr

* Wed Aug 21 2013 Steve Dickson <steved@redhat.com> 2.0.21-3
- Removed rpmlint warnings

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May  2 2013 Orion Poplawski <orion@cora.nwra.com> - 2.0.21-1
- Update to 2.0.21
- Add %%check

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr  4 2012 Steve Dickson <steved@redhat.com> 2.0.18-1
- Updated to latest stable upstream version: 2.0.18-stable
- Moved documentation into its own rpm (bz 810138)

* Mon Mar 12 2012 Steve Dickson <steved@redhat.com> 2.0.17-1
- Updated to latest stable upstream version: 2.0.17-stable

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Steve Dickson <steved@redhat.com> 2.0.14-1
- Updated to latest stable upstream version: 2.0.14-stable (bz 727129)
- Removed the installion of the outdate man pages and the latex raw docs.
- Corrected where the other doc are installed.

* Wed Aug 10 2011 Steve Dickson <steved@redhat.com> 2.0.13-1
- Updated to latest stable upstream version: 2.0.13-stable (bz 727129)

* Tue Aug  2 2011 Steve Dickson <steved@redhat.com> 2.0.12-1
- Updated to latest stable upstream version: 2.0.12-stable

* Wed Feb 09 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 2.0.10-2
- Fix build
- Update spec to match current guidelines
- drop no longer needed patch

* Tue Feb  8 2011 Steve Dickson <steved@redhat.com> 2.0.10-1
- Updated to latest stable upstream version: 2.0.10-stable

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 22 2010 Steve Dickson <steved@redhat.com> 1.4.14b-1
- Updated to latest stable upstream version: 1.4.14b

* Fri May 21 2010 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.13-2
- disable static libs (bz 556067)

* Tue Dec 15 2009 Steve Dickson <steved@redhat.com> 1.4.13-1
- Updated to latest stable upstream version: 1.4.13

* Tue Aug 18 2009 Steve Dickson <steved@redhat.com> 1.4.12-1
- Updated to latest stable upstream version: 1.4.12
- API documentation is now installed (bz 487977)
- libevent-devel multilib conflict (bz 477685)
- epoll backend allocates too much memory (bz 517918)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Steve Dickson <steved@redhat.com> 1.4.10-1
- Updated to latest stable upstream version: 1.4.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul  1 2008 Steve Dickson <steved@redhat.com> 1.4.5-1
- Updated to latest stable upstream version 1.4.5-stable

* Mon Jun  2 2008 Steve Dickson <steved@redhat.com> 1.4.4-1
- Updated to latest stable upstream version 1.4.4-stable

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3e-2
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Steve Dickson <steved@redhat.com> 1.3e-1
- Updated to latest stable upstream version 1.3e

* Fri Mar  9 2007 Steve Dickson <steved@redhat.com> 1.3b-1
- Updated to latest upstream version 1.3b
- Incorporated Merge Review comments (bz 226002)
- Increased the polling timeout (bz 204990)

* Tue Feb 20 2007 Steve Dickson <steved@redhat.com> 1.2a-1
- Updated to latest upstream version 1.2a

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.1a-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> - 1.1a-3
- rebuild (#177697)

* Mon Jul 04 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-2
- Removed unnecessary -r from rm

* Fri Jun 17 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1a-1
- Upstream update

* Wed Jun 08 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-2
- Added some docs
- Moved "make verify" into %%check

* Mon Jun 06 2005 Ralf Ertzinger <ralf@skytale.net> - 1.1-1
- Initial build for Fedora Extras, based on the package
  by Dag Wieers
