%define		_plugin	mail_fwd
%define		mversion	1.4.0
Summary:	A squirrel email forwarding plug-in
Summary(pl):	Wtyczka umo¿liwiaj±ca przekierowanie poczty
Name:		squirrelmail-plugin-%{_plugin}
Version:	0.4.1
Release:	2
License:	GPL
Group:		Applications/Mail
Source0:	http://www.squirrelmail.org/plugins/%{_plugin}.%{version}-%{mversion}.tar.gz
# Source0-md5:	472bfb19e60d865b7aa363f3ea0293c2
Patch0:		%{name}-Makefile.patch
URL:		http://www.squirrelmail.org/plugin_view.php?id=16
Requires:	php(ftp)
Requires:	squirrelmail >= 1.4.6-2
Requires:	squirrelmail-compatibility-2.0.4
Obsoletes:	squirrelmail-mail_fwd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_datadir}/squirrelmail/plugins/%{_plugin}
%define		_sysconfdir	/etc/webapps/squirrelmail

%description
This plug-in allows to set email forwarding.

Warning: this package contains file with suid bit set!

%description -l pl
Ta wtyczka pozwala na ustawienie przekierowania poczty.

Uwaga: ten pakiet zawiera plik z ustawionym bitem suid!

%prep
%setup -q -n %{_plugin}
%patch0 -p0

rm -f fwdfile/wfwd.o

%build
%{__make} -C fwdfile \
	CFLAGS="%{rpmcflags}" \
	LFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_plugindir} $RPM_BUILD_ROOT%{_sysconfdir} \
	$RPM_BUILD_ROOT%{_sbindir}

install fwdfile/wfwd $RPM_BUILD_ROOT%{_sbindir}
mv config_dist.php $RPM_BUILD_ROOT%{_sysconfdir}/%{_plugin}_config.php
install *.php $RPM_BUILD_ROOT%{_plugindir}
ln -s %{_sysconfdir}/%{_plugin}_config.php $RPM_BUILD_ROOT%{_plugindir}/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{_plugin}_config.php
%attr(4755,root,root) %{_sbindir}/wfwd
%dir %{_plugindir}
%{_plugindir}/*.php
