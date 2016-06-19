# TODO: system [lib]tinyxml2 when released (http://www.grinninglizard.com/tinyxml2/index.html)
#
# Conditional build:
%bcond_without	curl	# cURL support
%bcond_without	mms	# MMS support
#
%define	libzen_ver 0.4.33

Summary:	Supplies technical and tag information about a video or audio file
Summary(pl.UTF-8):	Informacje techniczne i znaczniki dla plików wideo i dźwiękowych
Name:		libmediainfo
Version:	0.7.86
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/mediainfo/%{name}_%{version}.tar.bz2
# Source0-md5:	98fc5e3c89cf13bb53353312aaf26596
URL:		http://mediainfo.sourceforge.net/
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
BuildRequires:	sed >= 4.0
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
Requires:	libzen-devel >= %{libzen_ver}
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

%prep
%setup -q -n MediaInfoLib
cp Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv History_DLL.txt History.txt
%undos *.txt *.html Source/Doc/*.html
chmod 644 *.txt *.html Source/Doc/*.html

%build
cd Project/GNU/Library
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-shared \
	%{?with_curl:--with-libcurl} \
	%{?with_mms:--with-libmms}

%{__make} clean
%{__make}
cd ../../../Source/Doc
doxygen Doxyfile

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/Library install \
	DESTDIR=$RPM_BUILD_ROOT

# MediaInfoDLL headers and MediaInfo-config
for i in MediaInfo MediaInfoDLL; do
	install -d $RPM_BUILD_ROOT%{_includedir}/$i
	install -m 644 Source/$i/*.h $RPM_BUILD_ROOT%{_includedir}/$i
done

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
install Project/GNU/Library/libmediainfo.pc $RPM_BUILD_ROOT%{_pkgconfigdir}
# fix empty Version tag
%{__sed} -i -e 's|Version: .*|Version: %{version}|g' $RPM_BUILD_ROOT%{_pkgconfigdir}/libmediainfo.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc History.txt License.html ReadMe.txt
%attr(755,root,root) %{_libdir}/libmediainfo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmediainfo.so.0

%files devel
%defattr(644,root,root,755)
# Documentation.html expects Doc/index.html
%doc Changes.txt Source/Doc/Documentation.html Doc Source/Example/HowToUse*
%attr(755,root,root) %{_libdir}/libmediainfo.so
%{_libdir}/libmediainfo.la
%{_includedir}/MediaInfo
%{_includedir}/MediaInfoDLL
%{_pkgconfigdir}/libmediainfo.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmediainfo.a
