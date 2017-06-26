%define dracutlibdir %{_prefix}/lib/dracut

%define dracut_mod_name 90crypt-tpm
%if 0%{?rhel} == 6
%define dracut_mod_name 50plymouth-tpm
%endif

Name:		tpm-luks
Version:	0.8.0
Release:	9%{?dist}
Summary:	Utility for storing a LUKS key using a TPM

Group:		Security
License:	GPLv2
#URL:
Source0:	tpm-luks-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	automake autoconf libtool openssl-devel
#Requires:	cryptsetup dracut gawk coreutils grubby tpm-tools trousers
# for now we require an upstream tpm-tools and trousers, so don't add them
# here so we can avoid --nodeps
Requires:	cryptsetup dracut gawk coreutils grubby

%description
tpm-luks is a set of scripts to enable storage of a LUKS key in your TPM.

%prep
%setup -q

%build
autoreconf -ivf
%configure --prefix=/usr --libdir=%{_libdir}
make %{?_smp_mflags}

%install
[ "${RPM_BUILD_ROOT}" != "/" ] && [ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc/init.d/
ln -s %{_sbindir}/tpm-luks-svc $RPM_BUILD_ROOT/etc/init.d/tpm-luks-svc

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && [ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

%files
%defattr(-,root,root,-)
%doc README TODO
%config /etc/dracut.conf.d/tpm-luks.conf
%{_bindir}/*
%{_sbindir}/*
%dir %{dracutlibdir}/modules.d/%{dracut_mod_name}
%{dracutlibdir}/modules.d/%{dracut_mod_name}/*
%config(noreplace) /etc/tpm-luks.conf
/etc/init.d/tpm-luks-svc

%changelog
* Tue Apr 09 2013 Ryan Harper <ryanh@us.ibm.com>
- Updated to build on F18

* Tue May 29 2012 Kent Yoder <key@linux.vnet.ibm.com>
- Initial drop of version 0.6
