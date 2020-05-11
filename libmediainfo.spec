# TODO: system libs:
# - pkgconfig(aes_gladman)
# - pkgconfig(sha1_gladman)
# - pkgconfig(sha2_gladman)
# - pkgconfig(hmac_gladman)
# - md5? (which implementation? pkgconfig(md5) is checked)
#
# Conditional build:
%bcond_without	curl		# cURL support
%bcond_without	mms		# MMS support
%bcond_without	apidocs		# API documentation (doxygen generated)
%bcond_without	static_libs	# static library

%define	libzen_ver 0.4.37
Summary:	Supplies technical and tag information about a video or audio file
Summary(pl.UTF-8):	Informacje techniczne i znaczniki dla plików wideo i dźwiękowych
Name:		libmediainfo
Version:	19.09
Release:	1
License:	BSD or Apache v2.0+ or LGPL v2.1+ or GPL v2+ or MPL v2.0+
Group:		Libraries
Source0:	https://github.com/MediaArea/MediaInfoLib/archive/v%{version}.tar.gz
# Source0-md5:	5d24b2fcc3c551e070b5dd6192424a4b
URL:		https://github.com/MediaArea/MediaInfoLib
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
%{?with_curl:BuildRequires:	curl-devel}
BuildRequires:	doxygen
%{?with_mms:BuildRequires:	libmms-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libzen-devel >= %{libzen_ver}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	tar >= 1:1.22
BuildRequires:	tinyxml2-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	libzen >= %{libzen_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MediaInfo supplies technical and tag information about a video or
audio file.

What information can I get from MediaInfo?
- General: title, author, director, album, track number, date,
  duration...
- Video: codec, aspect, fps, bitrate...
- Audio: codec, sample rate, channels, language, bitrate...
- Text: language of subtitle
- Chapters: number of chapters, list of chapters

Supported files: DivX, XviD, H263, H.263, H264, x264, ASP, AVC,
iTunes, MPEG-1, MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V,
QuickTime, RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2,
MSMPEG4v3, VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

Supported formats/containers:
- Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1, MPEG-2,
  MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP, H.264, AVC...)
- Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
- Subtitles: SRT, SSA, ASS, SAMI

This package contains the shared library for MediaInfo.

%description -l pl.UTF-8
MediaInfo udostępnia informacje techniczne oraz znaczniki dla plików
wideo i dźwiękowych.

Dostępne są informacje:
- ogólne: tytuł, autor, reżyser, album, numer ścieżki, data, czas
  trwania...
- wideo: kodek, proporcje, liczba klatek na sekundę, pasmo...
- dźwięk: kodek, częstotliwość próbkowania, liczba kanałów, język,
  pasmo...
- tekst: język napisów
- książki: liczba rozdziałów, ich lista

Obsługiwane pliki: DivX, XviD, H263, H.263, H264, x264, ASP, AVC,
iTunes, MPEG-1, MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V,
QuickTime, RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2,
MSMPEG4v3, VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

Obsługiwane formaty/kontenery:
- wideo: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1, MPEG-2,
  MPEG-4, DVD (VOB) (kodeki: DivX, XviD, MSMPEG4, ASP, H.264, AVC...)
- dźwięk: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
- napisy: SRT, SSA, ASS, SAMI

Ten pakiet zawiera bibliotekę współdzieloną MediaInfo.

%package devel
Summary:	Header files for MediaInfo library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki MediaInfo
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_curl:Requires:	curl-devel}
%{?with_mms:Requires:	libmms-devel}
Requires:	libstdc++-devel
Requires:	libzen-devel >= %{libzen_ver}
Requires:	tinyxml2-devel
Requires:	zlib-devel

%description devel
Header files for MediaInfo library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki MediaInfo.

%package static
Summary:	Static MediaInfo library
Summary(pl.UTF-8):	Statyczna biblioteka MediaInfo
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static MediaInfo library.

%description static -l pl.UTF-8
Statyczna biblioteka MediaInfo.

%package apidocs
Summary:	API documentation for MediaInfo library
Summary(pl.UTF-8):	Dokumentacja API biblioteki MediaInfo
Group:		Documentation
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description apidocs
API documentation for MediaInfo library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki MediaInfo.

%prep
%setup -q -n MediaInfoLib-%{version}
cp -p Release/ReadMe_DLL_Linux.txt ReadMe.txt
%{__mv} History_DLL.txt History.txt
%undos *.txt *.html Source/Doc/*.html
chmod 644 *.txt *.html Source/Doc/*.html

%build
cd Project/GNU/Library
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{?with_static_libs:--enable-static} \
	%{?with_curl:--with-libcurl} \
	%{?with_mms:--with-libmms} \
	--with-libtinyxml2

%{__make} clean
%{__make}

%if %{with apidocs}
cd ../../../Source/Doc
doxygen Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/Library install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changes.txt History.txt License.html README.md ReadMe.txt
%attr(755,root,root) %{_libdir}/libmediainfo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediainfo.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmediainfo.so
%{_libdir}/libmediainfo.la
%{_includedir}/MediaInfo
%{_includedir}/MediaInfoDLL
%{_pkgconfigdir}/libmediainfo.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmediainfo.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
# Documentation.html expects Doc/index.html
%doc Source/Doc/Documentation.html Doc Source/Example/HowToUse*
%endif
