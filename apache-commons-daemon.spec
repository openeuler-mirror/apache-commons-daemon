Name:              apache-commons-daemon
Version:           1.0.15
Release:           20
Summary:           Defines API to support an alternative invocation mechanism
License:           ASL 2.0
URL:               http://commons.apache.org/daemon
Source0:           http://archive.apache.org/dist/commons/daemon/source/commons-daemon-%{version}-src.tar.gz
BuildRequires:     maven-local java-devel >= 1:1.6.0 jpackage-utils apache-commons-parent
BuildRequires:     maven-surefire-provider-junit xmlto gcc make
Provides:          apache-commons-daemon-jsvc = %{version}-%{release} jsvc = 1:%{version}-%{release}
Obsoletes:         apache-commons-daemon-jsvc < %{version}-%{release}

Patch0001:         apache-commons-daemon-JAVA_OS.patch
Patch0002:         apache-commons-daemon-secondary.patch
Patch0003:         apache-commons-daemon-aarch64.patch
Patch0004:         apache-commons-daemon-riscv64.patch

%description
The scope of this package is to define an API in line with the current Java Platform APIs to support
an alternative invocation mechanism which could be used instead of the public static void main(String[]) method.
This specification covers the behavior and life cycle of what we define as Java daemons, or, in other words, non interactive Java applications.

%package           help
Requires:          jpackage-utils
BuildArch:         noarch
Summary:           Help documents for apache-commons-daemon
Provides:          apache-commons-daemon-javadoc = %{version}-%{release}
Obsoletes:         apache-commons-daemon-javadoc < %{version}-%{release}

%description       help
The apache-commons-daemon-help package conatins manual pages and API documents for apache-commons-daemon.

%prep
%autosetup -n commons-daemon-%{version}-src -p1

rm -rf src/samples/build/*
cd src/native/unix
xmlto man man/jsvc.1.xml

%build
cd src/native/unix
%configure --with-java=%{java_home}
make clean
%make_build
cd -

%mvn_file  : commons-daemon apache-commons-daemon
%mvn_alias : org.apache.commons:commons-daemon
%mvn_build

%install
install -Dpm 755 src/native/unix/jsvc $RPM_BUILD_ROOT%{_bindir}/jsvc
install -Dpm 644 src/native/unix/jsvc.1 $RPM_BUILD_ROOT%{_mandir}/man1/jsvc.1

%mvn_install

%files -f .mfiles
%doc LICENSE.txt
%{_bindir}/jsvc

%files help -f .mfiles-javadoc
%doc PROPOSAL.html NOTICE.txt RELEASE-NOTES.txt src/samples src/docs/*
%{_mandir}/man1/jsvc.1*

%changelog
* Wed Mar 9 2022 wangyangdahai<admin@you2.top> - 1.0.15-20
- fix riscv64 target

* Mon Dec 2 2019 liujing<liujing144@huawei.com> - 1.0.15-19
- Package init
