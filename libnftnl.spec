%define rpmversion 1.0.8
%define specrelease 1%{?dist}

Name:           libnftnl
Version:        %{rpmversion}
Release:        %{specrelease}%{?buildid}
Summary:        Library for low-level interaction with nftables Netlink's API over libmnl
License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl/
Source0:        http://ftp.netfilter.org/pub/libnftnl/libnftnl-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libmnl-devel
#BuildRequires:  mxml-devel
BuildRequires:  jansson-devel

%description
A library for low-level interaction with nftables Netlink's API over libmnl.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
# This is what autogen.sh (only in git repo) does - without it, patches changing
# Makefile.am cause the build system to regenerate Makefile.in and trying to use
# automake-1.14 for that which is not available in RHEL.
autoreconf -fi
rm -rf autom4te*.cache

%configure --disable-static --disable-silent-rules \
           --with-json-parsing --without-xml-parsing
make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_libdir}/*.so.*

%files devel
%{_libdir}/libnft*.so
%{_libdir}/pkgconfig/libnftnl.pc
%{_includedir}/libnftnl

%changelog
* Fri Oct 13 2017 Phil Sutter <psutter@redhat.com> [1.0.8-1.el7]
- Rebase onto upstream version 1.0.8 (Phil Sutter) [1472260]

* Tue May 16 2017 Phil Sutter <psutter@redhat.com> [1.0.6-6.el7]
- chain: dynamically allocate name (Phil Sutter) [1353320]
- src: Avoid returning uninitialized data (Phil Sutter) [1353319]
- expr/limit: Drop unreachable code in limit_to_type() (Phil Sutter) [1353312]
- ruleset: Initialize ctx.flags before calling nftnl_ruleset_ctx_set() (Phil Sutter) [1353322]
- src: Fix nftnl_*_get_data() to return the real attribute length (Phil Sutter) [1353322]
- expr/ct: prevent array index overrun in ctkey2str() (Phil Sutter) [1353309]
- utils: Don't return directly from SNPRINTF_BUFFER_SIZE (Phil Sutter) [1353311]
- set: prevent memleak in nftnl_jansson_parse_set_info() (Phil Sutter) [1353311]

* Fri May 12 2017 Phil Sutter <psutter@redhat.com> [1.0.6-5.el7]
- expr: lookup: give support for inverted matching (Phil Sutter) [1441084]
- tests: stricter string attribute validation (Phil Sutter) [1441084]

* Thu Feb 23 2017 Phil Sutter <psutter@redhat.com> [1.0.6-4.el7]
- Add automake and libtool as additional build requirements (Phil Sutter) [1418967]

* Thu Feb 23 2017 Phil Sutter <psutter@redhat.com> [1.0.6-3.el7]
- Fix libnftnl.spec for patches changing Makefile.am (Phil Sutter) [1418967]

* Thu Feb 23 2017 Phil Sutter <psutter@redhat.com> [1.0.6-2.el7]
- src: add range expression (Phil Sutter) [1418967]

* Wed Jun 29 2016 Phil Sutter <psutter@redhat.com> 1.0.6-1
- Rebased from Fedora Rawhide and adjusted for RHEL review.
