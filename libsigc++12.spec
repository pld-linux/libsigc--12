#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	The Typesafe Signal Framework for C++
Summary(pl.UTF-8):	Środowisko sygnałów z kontrolą typów dla C++
Name:		libsigc++12
Version:	1.2.7
Release:	4
License:	LGPL v2+
Group:		Libraries
Source0:	https://download.gnome.org/sources/libsigc++/1.2/libsigc++-%{version}.tar.bz2
# Source0-md5:	212f48536019e1f003d2509b4c9b36df
Patch0:		%{name}-m4.patch
Patch1:		am-lt.patch
URL:		https://libsigcplusplus.github.io/libsigcplusplus/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	m4
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with apidocs}
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	libxslt-progs
%endif
Obsoletes:	libsigc++-examples
Obsoletes:	libsigc++ < 1:1.9
Conflicts:	libsigc++ < 1.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library implements a full callback system for use in widget
libraries, abstract interfaces, and general programming. Originally
part of the Gtk-- widget set, libsigc++ is now a seperate library to
provide for more general use. It is the most complete library of its
kind with the ablity to connect an abstract callback to a class
method, function, or function object. It contains adaptor classes for
connection of dissimilar callbacks and has an ease of use unmatched by
other C++ callback libraries.

%description -l pl.UTF-8
Ta biblioteka jest implementacją pełnego systemu callbacków do
używania w bibliotekach widgetów, interfejsach abstrakcyjnych i
ogólnym programowaniu. Oryginalnie była to część zestawu widgetów
Gtk--, ale jest teraz oddzielną biblioteką ogólniejszego
przeznaczenia. Jest to kompletna biblioteka tego typu z możliwością
łączenia abstrakcyjnych callbacków z metodami klas, funkcjami lub
obiektami funkcji. Zawiera klasy adapterów do łączenia różnych
callbacków.

%package devel
Summary:	Development tools for the Typesafe Signal Framework for C++
Summary(pl.UTF-8):	Narzędzia programistyczne do środowiska libsig++
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	m4
Obsoletes:	libsigc++-devel < 1:1.9

%description devel
Development tools for the Typesafe Signal Framework for C++.

%description devel -l pl.UTF-8
Narzędzia programistyczne do środowiska libsigc++ - sygnałów z
kontrolą typów.

%package static
Summary:	Static Typesafe Signal Framework for C++ libraries
Summary(pl.UTF-8):	Statyczna biblioteka libsigc++
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	libsigc++-static < 1:1.9

%description static
Static Typesafe Signal Framework for C++ libraries.

%description static -l pl.UTF-8
Statyczna biblioteka libsigc++ - środowiska sygnałów z kontrolą typów.

%package apidocs
Summary:	API documentation for libsigc++ 1.2.x
Summary(pl.UTF-8):	Dokumentacja API do libsigc++ 1.2.x
Group:		Documentation
%{?noarchpackage}

%description apidocs
API documentation for libsigc++ 1.2.x.

%description apidocs -l pl.UTF-8
Dokumentacja API do libsigc++ 1.2.x.

%prep
%setup -q -n libsigc++-%{version}
%patch0 -p1
%patch1 -p1

%build
CXXFLAGS="%{rpmcflags} -fno-exceptions"
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__automake}
%configure
%{__make}

%if %{with apidocs}
%{__make} -C doc/manual
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsigc-1.2.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FEATURES IDEAS NEWS README TODO
%attr(755,root,root) %{_libdir}/libsigc-1.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libsigc-1.2.so.5

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsigc-1.2.so
%{_includedir}/sigc++-1.2
%{_libdir}/sigc++-1.2
%{_pkgconfigdir}/sigc++-1.2.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsigc-1.2.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/{API,FAQ,UML,conventions,diagrams,marshal,powerusers,requirements,signals} doc/manual/html
%endif
