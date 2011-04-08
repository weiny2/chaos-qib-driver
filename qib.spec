#  kmod package will be named kmod-{kmod_name}
%define kmod_name qib

#  Ideally, the build would occur against the oldest supported kernel
#   for a given release, e.g. 2.6.32-71.el6 for RHEL6.0. This is because
#   kABI is more likely to be forward compatible rather than backward
#   compatible.
#
#  [This is currently broken with yum though. Change kversion to
#   kernel_version when the yum bugs have been worked out, and for now
#   we build against the most recent kernel-devel package]
#
%{!?kversion: %define kversion 2.6.32-71.el6.%{_target_cpu}}

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
#  Base qib rpm now requires kmod-qib
Requires: kmod-%{name} = %{version}-%{release}

#  redhat-rpm-config includes the % kernel_module_package macro
BuildRequires: redhat-rpm-config

%description
QIB provides the driver to QLogic QDR cards.

#  The kernel_module_package macro creates the kmod-%{name} package
#   for the kernel module, and handles generation of kABI Requires,
#    handles %preinst/%postinst for kmod-* package, etc.
#
# kernel_module_package [ -n name ] [ -v version ] [ -r release ] [ -s script ]
#                       [ -f filelist] [ -x ] [ -p preamble ] flavor flavor ...
#
#  After expansion, it also defines kverrel macro as the kernel version
#   we built against (which is set to the latest installed kernel unless
#   kernel_version is defined.)
#
# By default kernel_module_package only packages the kernel module itself.
#  since we also want to include a file under depmod.d/ we have to supply
#  a -f filelist:
#
%kernel_module_package -f kmod-%{name}.list

#  Use kverrel defined by kernel_module_package to set kdir
%define kdir %{_usrsrc}/kernels/%{kverrel}

%prep
%setup -q
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
make VERSION=%version KERNVER=%kverrel KERNDIR=%kdir RELEASE=%release

%install
#  install depmod.d conf file
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
make VERSION=%version KERNVER=%kverrel KERNDIR=%kdir RELEASE=%release DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
/lib/modules/*

%post
#depmod -a %{kver}

