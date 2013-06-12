Name:      hunspell
Summary:   A spell checker and morphological analyzer library
Version:   1.2.8
Release:   3
Source0:   http://downloads.sourceforge.net/%{name}/hunspell-%{version}.tar.gz
Source1:   http://people.debian.org/~agmartin/misc/ispellaff2myspell
Source2:   http://people.redhat.com/caolanm/hunspell/wordlist2hunspell
Group:     System/Libraries
URL:       http://hunspell.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:   LGPLv2+ or GPLv2+ or MPLv1.1
BuildRequires: libtool, ncurses-devel
Patch1:    hunspell-1.2.7-2314461.ispell-alike.patch

%description
Hunspell is a spell checker and morphological analyzer library and program
designed for languages with rich morphology and complex word compounding or
character encoding. Hunspell interfaces: Ispell-like terminal interface using
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

%package devel
Requires: hunspell = %{version}-%{release}, pkgconfig
Summary: Files for developing with hunspell
Group: Development/Libraries

%description devel
Includes and definitions for developing with hunspell

%prep
%setup -q -n %{name}-%{version}/hunspell
%patch1 -p1 -b .ispell-alike.patch
# Filter unwanted Requires for the "use explicitely" string in ispellaff2myspell
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(explicitely)/d'
EOF

%define __perl_requires %{_builddir}/%{name}/%{name}-req
chmod +x %{__perl_requires}

%build
%reconfigure --disable-static  --with-ui --with-readline
for i in man/*.? man/hu/*.?; do
    iconv -f ISO-8859-2 -t UTF-8 $i > $i.new
    mv -f $i.new $i
done
make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}
rm -f $RPM_BUILD_ROOT/%{_bindir}/example
mkdir $RPM_BUILD_ROOT/%{_datadir}/myspell
mv $RPM_BUILD_ROOT/%{_includedir}/*munch* $RPM_BUILD_ROOT/%{_includedir}/%{name}
install -m 755 src/tools/affixcompress $RPM_BUILD_ROOT/%{_bindir}/affixcompress
install -m 755 src/tools/makealias $RPM_BUILD_ROOT/%{_bindir}/makealias
install -m 755 src/tools/wordforms $RPM_BUILD_ROOT/%{_bindir}/wordforms
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}/ispellaff2myspell
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/%{_bindir}/wordlist2hunspell

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README README.myspell COPYING COPYING.LGPL COPYING.MPL AUTHORS AUTHORS.myspell license.hunspell license.myspell THANKS
%{_libdir}/*.so.*
%{_datadir}/myspell
%{_bindir}/hunspell
%{_mandir}/man1/hunspell.1.gz
%{_mandir}/man4/hunspell.4.gz
%lang(hu) %{_mandir}/hu/man1/hunspell.1.gz
%lang(hu) %{_mandir}/hu/man4/hunspell.4.gz

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/*.so
%{_bindir}/affixcompress
%{_bindir}/makealias
%{_bindir}/munch
%{_bindir}/unmunch
%{_bindir}/analyze
%{_bindir}/chmorph
%{_bindir}/hzip
%{_bindir}/hunzip
%{_bindir}/ispellaff2myspell
%{_bindir}/wordlist2hunspell
%{_bindir}/wordforms
%{_libdir}/pkgconfig/hunspell.pc
%{_mandir}/man1/hunzip.1.gz
%{_mandir}/man1/hzip.1.gz
%{_mandir}/man3/hunspell.3.gz

