Summary: A library which allows userspace access to USB devices
Name: libusb
Version: 0.1.12
Release: 23%{?dist}
Source0: http://prdownloads.sourceforge.net/libusb/%{name}-%{version}.tar.gz
Patch0: libusb-0.1.12-libusbconfig.patch
Patch1: libusb-0.1.12-memset.patch
Patch2: libusb-0.1.12-openat.patch
Patch3: libusb-0.1.12-wakeups.patch
Patch4: libusb-0.1.12-concurrency-timeout.patch
License: LGPLv2+
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://sourceforge.net/projects/libusb/
BuildRequires: docbook-utils, pkgconfig
BuildRequires: docbook-dtds >= 1.0-5, docbook-utils-pdf
BuildRequires: openjade autoconf

%description
This package provides a way for applications to access USB devices.

%package devel
Summary: Development files for libusb
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files, libraries  and documentation needed to
develop applications that use libusb.

%package static
Summary: Static development files for libusb
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
This package contains static libraries to develop applications that use libusb.

%prep
%setup -q
%patch0 -p1 -b .libusbconfig
%patch1 -p1 -b .memset
%patch2 -p1 -b .openat
#%patch3 -p0 -b .wakeups
#%patch4 -p1 -b .concurrency-timeout

%build
autoconf
%configure
make CFLAGS="$RPM_OPT_FLAGS"
pushd doc
docbook2ps manual.sgml
sed -i '/DVIPSSource:/d;/CreationDate:/d' manual.ps
popd

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%doc AUTHORS README LICENSE INSTALL.libusb NEWS ChangeLog doc/manual.ps doc/html
%{_bindir}/libusb-config
%{_libdir}/pkgconfig/libusb.pc
%{_includedir}/*
%{_libdir}/*.so

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%changelog
* Thu Feb 25 2010 Jindrich Novy <jnovy@redhat.com>  0.1.12-23
- add LICENSE to docs

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.1.12-22.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-20
- remove ExcludeArch: s390 s390x, libusb works fine there (#467768)

* Tue Oct 14 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-19
- don't apply the concurrency timeout handling patch, it breaks
  pilot-link (#456811)

* Mon Oct  6 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-18
- fix multiarch conflict in libusb-devel (#465209)

* Sat Aug  2 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-17
- apply patch from Graeme Gill to fix concurrency timeout
  handling (#456811)

* Fri Apr 18 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-16
- rebuild to fix broken ppc build

* Tue Feb 26 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-15
- don't apply wakeups patch until it's fixed, it causes problems
  with Eye-One Pro (#434950)

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 0.1.12-14
- manual rebuild because of gcc-4.3 (#434189)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.12-13
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-12
- remove unnecessary 1ms wakeups while USB transfers are in progress,
  thanks to Scott Lamb (#408131)

* Tue Nov  6 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-11
- fix multilib conflict in manual.ps (#342461)
- drop useless BR: gawk

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-10
- optimize usb_find_devices() and use openat() instead of open()
 (#273901), thanks to Ulrich Drepper
- BR gawk

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-9
- update License
- rebuild for BuildID

* Wed Aug  1 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-8
- don't use uninitialized buffers on stack (#250274)

* Tue Feb 08 2007 Jindrich Novy <jnovy@redhat.com> 0.1.12-7
- merge review spec fixes (#226053)
- create -static subpackage to ship static libs separately
- don't use auto* stuff, drop automake, libtool deps
- BuildRequire openjade, fix Requires

* Tue Dec 12 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-6
- fix BuildRoot, add dist tag, rpmlint warnfixes

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.1.12-5.1
- rebuild

* Fri Jun 08 2006 Jesse Keating <jkeating@redhat.com> 0.1.12-5
- Add missing BR automake, libtool.
- Add missing Requires in -devel on pkgconfig

* Thu Jun  1 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-4
- remove .la files from libusb-devel (#172643)

* Wed May 30 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-3
- use pkg-config calls in libusb-config instead of hardcoded
  defaults to avoid multiarch conflicts (#192714)

* Fri May  5 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-2
- add docbook-utils-pdf BuildRequires (#191744)

* Mon Mar  6 2006 Jindrich Novy <jnovy@redhat.com> 0.1.12-1
- update to 0.1.12
- drop .format, .searchorder patches, applied upstream

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.1.11-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.1.11-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Jindrich Novy <jnovy@redhat.com> 0.1.11-2
- change device search order, /dev/bus/usb is tried first,
  then /proc/bus/usb, and never try /sys/bus/usb (#178994)

* Fri Jan 20 2006 Jindrich Novy <jnovy@redhat.com> 0.1.11-1
- 0.1.11
- require pkgconfig, package libusb.pc
- fix printf format in linux.c so that libusb can be built with -Werror (default)

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 0.1.10a-3
- Rebuild.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Mon Nov 21 2005 Tim Waugh <twaugh@redhat.com> 0.1.10a-2
- Build does not require xorg-x11-devel.  Fixes rebuild problem (no more
  xorg-x11-devel package).

* Wed Mar  9 2005 Tim Waugh <twaugh@redhat.com> 0.1.10a-1
- 0.1.10a.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.1.10-2
- Rebuild for new GCC.

* Fri Feb 11 2005 Tim Waugh <twaugh@redhat.com> 0.1.10-1
- 0.1.10.

* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 0.1.9-1
- Build requires xorg-x11-devel.
- 0.1.9.

* Sat Jan 08 2005 Florian La Roche <laroche@redhat.com>
- rebuilt to get rid of legacy selinux filecontexts

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Tim Waugh <twaugh@redhat.com> 0.1.8-3
- Run aclocal/autoconf to make shared libraries work again.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 11 2004 Tim Waugh <twaugh@redhat.com> 0.1.8-1
- 0.1.8.

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 0.1.7-3
- Fixed spec file.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com>
- Use the CFLAGS from the environment.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 0.1.7-1
- 0.1.7.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe

* Tue Jun 25 2002 Tim Waugh <twaugh@redhat.com> 0.1.6-1
- 0.1.6.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.1.5-6
- automated rebuild

* Fri Jun 21 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-5
- Rebuild to fix broken deps.

* Thu May 23 2002 Tim Powers <timp@redhat.com> 0.1.5-4
- automated rebuild

* Thu Apr 11 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-3
- Rebuild (fixes bug #63196).

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-2
- Rebuild in new environment.

* Thu Feb  7 2002 Tim Waugh <twaugh@redhat.com> 0.1.5-1
- 0.1.5.

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 0.1.4-2
- Rebuild in new environment.
- Work around tarball brokenness (doc directory was not automade).

* Mon Oct 29 2001 Tim Waugh <twaugh@redhat.com> 0.1.4-1
- Adapted for Red Hat Linux.
- 0.1.4.

* Thu Mar  1 2001 Frederic Crozat <fcrozat@mandrakesoft.com> 0.1.3b-1mdk
- Initial Mandrake release
