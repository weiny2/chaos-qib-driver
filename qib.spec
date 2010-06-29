%if 0%{?require_kver:1}
%define kdir /usr/src/kernels/%{require_kver}
%define kver %{require_kver}
BuildRequires: chaos-kernel-devel = %{kver}
%else
%define kdir %((echo X; ls -1d /usr/src/kernels/*)|tail -1)
%define kver %(basename %{kdir})
BuildRequires: chaos-kernel-devel
%endif
%if 0%{!?build_src_rpm:1}
%define relext _%(echo %{kver}|sed -e 's/-/_/g')
%endif

Name: qib
Version: 1.5.2
Release: test
Source: qib-%{version}.tgz

Summary: QLogic QIB driver
Packager: Ira Weiny <weiny2@llnl.gov>
License: GPLv2 or BSD
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Url: http://openfabrics.org
Requires: chaos-kernel = %{kver}

%description
QIB provides the driver to QLogic QDR cards.

%prep
%setup -q

%build
make VERSION=%version KERNVER=%kver KERNDIR=%kdir RELEASE=%release

%install
make VERSION=%version KERNVER=%kver KERNDIR=%kdir RELEASE=%release DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/lib/modules/*

%post
depmod -a

