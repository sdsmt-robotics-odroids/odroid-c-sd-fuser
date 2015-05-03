Name:           odroid-c-sd-fuser
Version:        0.1.0
Release:        1%{?dist}
Summary:        Boot media blob for ODROID-C

Group:          System Environment/Base
License:        BSD
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-c1
Source0:        https://github.com/hardkernel/u-boot/raw/odroidc-v2011.03/sd_fuse/bl1.bin.hardkernel
Source1:        odroid-c-sd-fuser
Source2:        odroid-c-emmc-fuser

BuildArch:      noarch

BuildRequires:  odroid-c-uboot

%description
Binary blob used to boot Hardkernel's ODROID-C. The blob contains:
- bl1
- u-boot

%prep
cp -a %{SOURCE1} odroid-c-sd-fuser
cp -a %{SOURCE2} odroid-c-emmc-fuser

%build
signed_bl1_position=0
uboot_position=64

#<BL1 fusing>
echo "BL1 fusing"
dd oflag=dsync if=%{SOURCE0} of=bootblob.bin seek=$signed_bl1_position bs=1 count=442
dd oflag=dsync if=%{SOURCE0} of=bootblob.bin seek=$signed_bl1_position skip=1 seek=1
#<u-boot fusing>
echo "u-boot fusing"
dd if=/boot/uboot/u-boot.bin of=bootblob.bin seek=$uboot_position

chmod +x bootblob.bin

sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-c-sd-fuser
sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-c-emmc-fuser

%install
install -p -m0755 -D bootblob.bin %{buildroot}%{_datadir}/%{name}/bootblob.bin
install -p -m0755 -D odroid-c-sd-fuser %{buildroot}%{_bindir}/odroid-c-sd-fuser
install -p -m0755 -D odroid-c-emmc-fuser %{buildroot}%{_bindir}/odroid-c-emmc-fuser

%files
%{_bindir}/odroid-c-sd-fuser
%{_bindir}/odroid-c-emmc-fuser
%{_datadir}/%{name}/bootblob.bin

%changelog
* Sat May 02 2015 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package
