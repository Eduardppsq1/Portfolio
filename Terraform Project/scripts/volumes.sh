#!/bin/bash

set -ex

vgchange -ay

DISC_ADITIONAL=`blkid -o value -s TYPE ${DEVICE} || echo ""`
if [ "`echo -n $DISC_ADITIONAL`" == "" ] ; then 
  # wait for the device to be attached
  DEVICENAME=`echo "${DEVICE}" | awk -F '/' '{print $3}'`
  DISCT_EXISTA=''
  while [[ -z $DISCT_EXISTA ]]; do
    echo "Verificare $DEVICENAME"
    DISCT_EXISTA=`lsblk |grep "$DEVICENAME" |wc -l`
    if [[ $DISCT_EXISTA != "1" ]]; then
      sleep 15
    fi
  done
  pvcreate ${DEVICE}
  vgcreate test ${DEVICE}
  lvcreate --name volume1 -l test volume
  mkfs.ext4 /dev/test/volume1
fi
mkdir -p /test
echo '/dev/test/volume1 /test ext4 defaults 0 0' >> /etc/fstab
mount /test

