
## Storing your LUKS key in TPM NVRAM

First make sure you have all the runtime pre-reqs installed, including the trousers and tpm-tools packages.

You can now generate new LUKS keys and seal them:
```
tpm-luks-ctl init      to generate new LUKS keys and save them in the TPM NVRAM
tpm-luks-ctl backup    to dump the LUKS keys and backup them in a safe place
dracut --force         to update initramfs
reboot                 to verify it works and have all PCRs computed correctly
tpm-luks-ctl seal      to seal the TPM NVRAM
reboot                 to verify it restarts automatically
tpm-luks-ctl check     to be sure
```

For the first boot, keys are not sealed and no password is required.

For the second boot, keys are sealed and automatically read.

Remember that modifying the `/etc/tpm-luks.conf` requires to update the boot:
```
dracut --force
```

## Notes

When initialized or unsealed, the TPM NVRAM is readable directly without having to enter a password. If you want an AUTH password, you can use the `-a` or `--auth-password` option. For the OWNER password, you can use `-o` or `--owner-password`.

If you want to use over PCRs than the defaults, you can modify them directly in the script `/usr/sbin/tpm-luks-gen-tgrub2-pcr-values`, or change the scripts defined for each devices in `/etc/tpm-luks.conf`.

You can check if tpm-luks is configured correctly:
* `tpm-luks-ctl check`

If you want to unseal the TPM, before a reboot for example, remember to seal after the reboot:
* unseal: `tpm-luks-ctl unseal`
* `reboot`
* seal: `tpm-luks-ctl seal`

To add new LUKS partitions at boot time:
* modify `/etc/default/grub` file with new partitions info
* unseal: `tpm-luks-ctl unseal`
* add new partitions: `tpm-luks-ctl init`
* save backup: `tpm-luks-ctl backup`
* update grub: `grub-mkconfig -o /boot/grub/grub.cfg`
* update iniramfs: `dracut --force`
* reboot: `reboot`
* seal: `tpm-luks-ctl seal`
* `reboot` to verify everything is ok

To add new LUKS partitions (i.e. for data) just after boot time, with tpm-luks-svc - beware, the size of TPM NVRAM is limited, so it might be usefull to use the same TPM NVRAM for all data disks -- here I'm using index 1:
* format all data disks using `cyptsetup luksFormat` with a very simple text password for example, and get it's UUID
```
echo -n "abc" > luks.key
cryptsetup luksFormat /dev/sdx --key-file luks.key
cryptsetup luksDump /dev/sdx | grep UUID: | awk '{print $2}'
```
* add the new disks in `/etc/crypttab` with `noauto` option
```
data0x UUID=x*** none noauto
```
* add new paritions with index 1: `tpm-luks-ctl init -i 1`
* save backup: `tpm-luks-ctl backup`
* start service automatically: `chkconfig --add tpm-luks-svc`
* unseal: `tpm-luks-ctl unseal`
* reboot: `reboot`
* seal: `tpm-luks-ctl seal`
* reboot: `reboot`
