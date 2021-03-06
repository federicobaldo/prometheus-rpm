Name:		prometheus-node-exporter
Version:	0.10.0
Release:	1%{?dist}
Summary:	Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/node_exporter
Source0:	https://github.com/prometheus/node_exporter/archive/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):  /usr/sbin/useradd
Requires:       daemonize
AutoReqProv:	No

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
mkdir -vp $RPM_BUILD_ROOT/var/log/prometheus/
mkdir -vp $RPM_BUILD_ROOT/var/run/prometheus
mkdir -vp $RPM_BUILD_ROOT/var/lib/prometheus
mkdir -vp $RPM_BUILD_ROOT/usr/bin
mkdir -vp $RPM_BUILD_ROOT/etc/init.d
mkdir -vp $RPM_BUILD_ROOT/etc/prometheus
mkdir -vp $RPM_BUILD_ROOT/etc/sysconfig
install -m 755 node_exporter $RPM_BUILD_ROOT/usr/bin/node_exporter
install -m 644 contrib/node_exporter.conf $RPM_BUILD_ROOT/etc/prometheus/node_exporter.conf
install -m 755 contrib/node_exporter.init $RPM_BUILD_ROOT/etc/init.d/node_exporter
install -m 644 contrib/node_exporter.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/node_exporter

%clean
make clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d $RPM_BUILD_ROOT/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%files
%defattr(-,root,root,-)
/usr/bin/node_exporter
%config(noreplace) /etc/prometheus/node_exporter.conf
/etc/init.d/node_exporter
%config(noreplace) /etc/sysconfig/node_exporter
/var/run/prometheus
/var/log/prometheus
