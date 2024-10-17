#Module-Specific definitions
%define mod_name mod_upload
%define mod_conf A70_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0
Release:	14
Group:		System/Servers
License:	GPL
URL:		https://apache.webthing.com/mod_upload/
# there is no official tar ball
# http://apache.webthing.com/svn/apache/forms/mod_upload.c
Source0:	http://apache.webthing.com/svn/apache/filters/xmlns/mod_upload.c
Source1:	README.mod_upload
Source2:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file

%description
mod_upload is an input filter module for multipart/form-data, as submitted from
File Upload forms on the Web. mod_upload decodes the data, so the handler gets
the file itself without the MIME encoding. Other fields from the form are
provided as a table of names/values.

%prep

%setup -q -c -T -n %{mod_name}-%{version}

cp %{SOURCE0} %{mod_name}.c
cp %{SOURCE1} README
cp %{SOURCE2} %{mod_conf}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean

%files
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 0-13mdv2012.0
+ Revision: 773232
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 0-12
+ Revision: 678431
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0-11mdv2011.0
+ Revision: 588077
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0-10mdv2010.1
+ Revision: 516206
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0-9mdv2010.0
+ Revision: 406665
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0-8mdv2009.0
+ Revision: 235117
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0-7mdv2009.0
+ Revision: 215660
- fix rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0-6mdv2008.1
+ Revision: 181944
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0-4mdv2008.0
+ Revision: 82689
- rebuild


* Wed Mar 14 2007 Oden Eriksson <oeriksson@mandriva.com> 0-3mdv2007.1
+ Revision: 143742
- bunzip sources

* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0-2mdv2007.1
+ Revision: 140767
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0-1mdv2007.0
+ Revision: 79533
- Import apache-mod_upload

* Tue Jul 18 2006 Oden Eriksson <oeriksson@mandriva.com> 0-1mdv2007.0
- initial Mandriva package

