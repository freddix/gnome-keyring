Summary:	Keep passwords and other user's secrets
Name:		gnome-keyring
Version:	3.12.0
Release:	1
License:	LGPL v2+/GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-keyring/3.12/%{name}-%{version}.tar.xz
# Source0-md5:	b0e2041c31c68b92f324d1ec7fa9d289
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gcr-devel >= 3.12.0
BuildRequires:	gobject-introspection-devel >= 1.38.0
BuildRequires:	gtk+3-devel >= 3.10.0
BuildRequires:	libcap-ng-devel
BuildRequires:	libtool
BuildRequires:	p11-kit-devel
BuildRequires:	pkg-config
Requires(post,postun):	glib-gio-gsettings
Requires:	gcr >= 3.12.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GNOME Keyring is a program that keeps password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

The library libgnome-keyring is used by applications to integrate with
the GNOME keyring system.

%prep
%setup -q

# freddix only
%{__sed} -i "s|LXDE|OPENBOX|g" daemon/*.desktop.in.in

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile   \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install   \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/{*,*/*}/*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache

%postun
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gnome-keyring
%attr(755,root,root) %{_bindir}/gnome-keyring-3
%attr(755,root,root) %{_bindir}/gnome-keyring-daemon

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/devel
%dir %{_libdir}/pkcs11
%attr(755,root,root) %{_libdir}/pkcs11/*.so
%attr(755,root,root) %{_libexecdir}/devel/*.so

%attr(755,root,root) %{_libdir}/security/pam_gnome_keyring.so

%{_datadir}/dbus-1/services/org.freedesktop.secrets.service
%{_datadir}/dbus-1/services/org.gnome.keyring.service

%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/glib-2.0/schemas/*.xml

%{_sysconfdir}/xdg/autostart/gnome-keyring-gpg.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-secrets.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-ssh.desktop
%{_datadir}/p11-kit/modules/gnome-keyring.module

#%{_mandir}/man1/gnome-keyring-daemon.1*

