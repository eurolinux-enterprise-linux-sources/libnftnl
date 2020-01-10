Name:           libnftnl
Version:        1.0.6
Release:        1%{?dist}
Summary:        Library for low-level interaction with nftables Netlink's API over libmnl
License:        GPLv2+
URL:            http://netfilter.org/projects/libnftnl/
Source0:        http://ftp.netfilter.org/pub/libnftnl/libnftnl-%{version}.tar.bz2
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
%setup -q

%build
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
* Wed Jun 29 2016 Phil Sutter <psutter@redhat.com> 1.0.6-1
- Rebased from Fedora Rawhide and adjusted for RHEL review.
