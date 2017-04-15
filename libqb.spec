#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	tests		# "make check" call
#
Summary:	libqb - high performance client server reusable features
Summary(pl.UTF-8):	libqb - wysoko wydajne funkcje architektury klient-serwer
Name:		libqb
Version:	1.0.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/ClusterLabs/libqb/releases
Source0:	https://github.com/ClusterLabs/libqb/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	62c93482bfc0d8b61af7910cffdf3609
URL:		https://github.com/ClusterLabs/libqb
%{?with_tests:BuildRequires:	check-devel >= 0.9.4}
BuildRequires:	doxygen
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libqb is a library with the primary purpose of providing high
performance client server reusable features. It provides high
performance logging, tracing, ipc, and poll.

%description -l pl.UTF-8
libqb to biblioteka, której głównym celem jest dostarczenie
wysoko wydajnych funkcji użytecznych przy architekturze klient-serwer.
Udostępnia wysoko wydajne logowanie, śledzenie, IPC oraz poll.

%package devel
Summary:	Header files for libqb library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libqb
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libqb library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libqb.

%package static
Summary:	Static libqb library
Summary(pl.UTF-8):	Statyczna biblioteka libqb
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libqb library.

%description static -l pl.UTF-8
Statyczna biblioteka libqb.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libqb.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.markdown
%attr(755,root,root) %{_sbindir}/qb-blackbox
%attr(755,root,root) %{_libdir}/libqb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqb.so.0
%{_mandir}/man8/qb-blackbox.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqb.so
%{_includedir}/qb
%{_pkgconfigdir}/libqb.pc
%{_mandir}/man3/qb*.h.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqb.a
%endif
