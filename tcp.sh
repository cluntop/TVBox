#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
 exec sudo "$0" "$@"
 exit 1
fi

clun_download() {
cd ~ && curl -s https://gh.clun.top/raw.githubusercontent.com/cluntop/sh/refs/heads/main/tcp.sh -o clun_tcp.sh && chmod +x clun_tcp.sh && ./clun_tcp.sh $1
} && clun_download $1
