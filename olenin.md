## Задние 1

Команда:
```
grep -o '^[^:]*' /etc/passwd | sort
```
Вывод:
```
adm
avahi
bin
chrony
colord
daemon
DanOle
dbus
dnsmasq
ftp
games
geoclue
gluster
halt
lp
mail
nm-openconnect
nm-openvpn
nobody
nslcd
openvpn
operator
pipewire
polkitd
postfix
root
rpc
rtkit
sddm
shutdown
sigma
sshd
student
sync
systemd-coredump
systemd-oom
systemd-resolve
systemd-timesync
tcpdump
tss
unbound
vboxadd
```
## Задание 2
Команда:
```
grep -v '^#' /etc/protocols | awk 'NF>=2 {print $2, $1}' | sort -nr | head -n 5
```
Вывод:
```
142 rohc
141 wesp
140 shim6
139 hip
138 manet
```
## Задание 3

Команда:
```
echo '#!/bin/sh' > banner
echo 'text="$*"' >> banner
echo 'border=$(echo "$text" | sed "s/./-/g")' >> banner
echo 'echo "+-$border-+"' >> banner
echo 'echo "| $text |"' >> banner
echo 'echo "+-$border-+"' >> banner
chmod +x banner
./banner "Hello from RTU MIREA!"
./banner "Hi"
```
Вывод:
```
+-----------------------+
| Hello from RTU MIREA! |
+-----------------------+
+----+
| Hi |
+----+
```
## Задание 4

Команда:
```
echo '#include <stdio.h>' > hello.c
echo 'int main(void) {' >> hello.c
echo '    printf("hello world\n");' >> hello.c
echo '    return 0;' >> hello.c
echo '}' >> hello.c
cat hello.c
grep -oE '[A-Za-z_][A-Za-z0-9_]*' hello.c | sort -u | tr '\n' ' '; echo
```
Вывод:
```
#include <stdio.h>
int main(void) {
    printf("hello world\n");
    return 0;
}
h hello include int main n printf return stdio void world
```

## Задание 5

Команда:
```
echo '#!/bin/sh' > reg
echo 'chmod 755 "$1"' >> reg
echo 'cp "$1" /usr/local/bin/' >> reg
echo 'echo "Команда $1 зарегистрирована"' >> reg
chmod +x reg
sudo ./reg banner
ls -l /usr/local/bin/banner
banner "Works without ./"
```
Вывод:
```
Команда banner зарегистрирована
-rwxr-xr-x. 1 root root 114 окт  1 13:03 /usr/local/bin/banner
+------------------+
| Works without ./ |
+------------------+
```

## Задание 6

Команда:
```
echo '// comment' > a.c
echo 'x = 1' > b.py
echo '/* comment */' > c.js
for f in *.c *.js *.py; do case "$f" in *.py) p='^#';; *) p='^(//|/\*)';; esac; head -n 1 "$f" | grep -qE "$p" && echo "$f: есть комментарий" || echo "$f: нет комментария"; done
```
Вывод:
```
a.c: есть комментарий
hello.c: нет комментария
c.js: есть комментарий
b.py: нет комментария
```
