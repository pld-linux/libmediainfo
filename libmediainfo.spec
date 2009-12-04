Summary:	Supplies technical and tag information about a video or audio file
Name:		libmediainfo
Version:	0.7.25
Release:	1
License:	GPL
Group:		Libraries
URL:		http://mediainfo.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/mediainfo/source/libmediainfo/%{version}/%{name}_%{version}.tar.bz2
# Source0-md5:	899f1f481c6e96918479a4bb1b2cefbe
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	libzen-devel >= 0.4.9
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
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

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1, MPEG1,
MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime, RealVideo,
RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3, VOB, DVD, WMA,
VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
- Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1, MPEG-2,
  MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP, H.264, AVC...)
- Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
- Subtitles: SRT, SSA, ASS, SAMI

This package contains the shared library for MediaInfo.

%package devel
Summary:	Include files and mandatory libraries for development
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libzen-devel >= 0.4.9

%description devel
Include files and mandatory libraries for development.

%package static
Summary:	Static libmediainfo library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libmediainfo library.

%prep
%setup -q -n MediaInfoLib
cp           Release/ReadMe_DLL_Linux.txt ReadMe.txt
mv           History_DLL.txt History.txt
dos2unix     *.txt *.html Source/Doc/*.html
chmod 644 *.txt *.html Source/Doc/*.html

%build
export CFLAGS="%{rpmcflags}"
export CPPFLAGS="%{rpmcppflags}"
export CXXFLAGS="%{rpmcxxflags}"

cd Source/Doc
	doxygen Doxyfile
cd ../..

cp Source/Doc/*.html ./

cd Project/GNU/Library
	chmod +x autogen
	./autogen
	%configure \
	--enable-shared \
	--disable-libcurl \
	--disable-libmms \


	%{__make} clean
	%{__make}
cd ../../..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C Project/GNU/Library \
	install \
	DESTDIR=$RPM_BUILD_ROOT

# MediaInfoDLL headers and MediaInfo-config
for i in MediaInfo MediaInfoDLL; do
	install -dm 755 $RPM_BUILD_ROOT%{_includedir}/$i
	install -m 644 Source/$i/*.h $RPM_BUILD_ROOT%{_includedir}/$i
done

%{__sed} -i -e 's|Version: |Version: %{version}|g' Project/GNU/Library/libmediainfo.pc
install -dm 755 $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install Project/GNU/Library/libmediainfo.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc History.txt License.html ReadMe.txt
%attr(755,root,root) %{_libdir}/libmediainfo.so.*

%files devel
%defattr(644,root,root,755)
%doc Changes.txt Documentation.html Doc/* Source/Example/HowToUse*
%{_includedir}/MediaInfo
%{_includedir}/MediaInfoDLL
%{_libdir}/libmediainfo.la
%attr(755,root,root) %{_libdir}/libmediainfo.so
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libmediainfo.a
