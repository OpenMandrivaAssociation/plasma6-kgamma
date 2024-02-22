%define stable %([ "$(echo %{version} |cut -d. -f2)" -ge 80 -o "$(echo %{version} |cut -d. -f3)" -ge 80 ] && echo -n un; echo -n stable)
%define git 20240222
%define gitbranch Plasma/6.0
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

Name:		plasma6-kgamma
Summary:	Plasma 6 monitor calibration module
Version:	6.0.0
Release:	%{?git:0.%{git}.}1
Group:		Graphical desktop/KDE
License:	GPLv2
URL:		http://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/plasma/kgamma/-/archive/%{gitbranch}/kgamma-%{gitbranchd}.tar.bz2#/kgamma5-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/plasma/%(echo %{version} |cut -d. -f1-3)/kgamma-%{version}.tar.xz
%endif
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6ConfigWidgets)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	gettext

%description
Plasma 6 monitor calibration module.

%files -f kcmkgamma.lang
%dir %{_datadir}/kgamma
%dir %{_datadir}/kgamma/pics
%{_datadir}/kgamma/pics/*.png
%{_qtdir}/plugins/plasma/kcminit/kcm_kgamma_init.so
%{_qtdir}/plugins/plasma/kcms/systemsettings_qwidgets/kcm_kgamma.so
%{_datadir}/applications/kcm_kgamma.desktop

#----------------------------------------------------------------------

%prep
%autosetup -p1 -n kgamma-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%find_lang kcmkgamma --all-name --with-html || touch kcmkgamma.lang
