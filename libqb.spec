#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	tests		# don't build and run tests
#
Summary:	libqb - high performance client server reusable features
Summary(pl.UTF-8):	libqb - wysoko wydajne funkcje architektury klient-serwer
Name:		libqb
Version:	0.14.0
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://fedorahosted.org/releases/q/u/quarterback/%{name}-%{version}.tar.gz
# Source0-md5:	1c310cc167fd5e2d074d693f33671595
URL:		http://www.libqb.org/
%{?with_tests:BuildRequires:	check-devel}
BuildRequires:	doxygen
BuildRequires:	glib2-devel
BuildRequires:	pkgconfig
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
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README.*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/libqb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libqb.so.0
%{_mandir}/man8/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libqb.so
%{_libdir}/libqb.la
%{_includedir}/qb
%{_pkgconfigdir}/libqb.pc
%{_mandir}/man3/*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libqb.a
%endif
