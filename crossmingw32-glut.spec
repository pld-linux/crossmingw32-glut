%define		realname	glut
Summary:	OpenGL Utility Toolkit (GLUT) - Mingw32 cross version
Summary(pl):	OpenGL Utility Toolkit (GLUT) - wersja skro¶na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	3.7
Release:	2
License:	GPL
Group:		Libraries
Source0:	http://www.opengl.org/resources/libraries/glut/%{realname}-%{version}.tar.gz
# Source0-md5:	dc932666e2a1c8a0b148a4c32d111ef3
URL:		http://www.opengl.org/resources/libraries/glut.html
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	/bin/csh
Conflicts:	crossmingw32-w32api < 2.5-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
A 3-D graphics library which uses the OpenGL API.

%description -l pl
Biblioteka graficzna 3D u¿ywaj±ca API z OpenGL.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

cd lib/glut

rm capturexfont.c
rm glut_menu.c
rm glut_menu2.c
rm layerutil.c

for i in *.c
do
	%{__cc} %{rpmcflags} -c $i -I../../include
done

rm -f libglut.a
$AR cru libglut.a *.o
$RANLIB libglut.a

%{__cc} --shared *.o -Wl,--enable-auto-image-base -o glut.dll -Wl,--out-implib,libglut.dll.a -lopengl32 -lglu32 -lgdi32 -lwinmm

%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include/GL,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install include/GL/{f,g}*.h $RPM_BUILD_ROOT%{arch}/include/GL
install lib/glut/libglut{,.dll}.a $RPM_BUILD_ROOT%{arch}/lib
install lib/glut/glut.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
