run(){
    proot --link2symlink -S $(container_path) -w /root /usr/bin/env \
    -i HOME=/root LANG=C.UTF-8 \
    PATH=/bin:/usr/bin:/sbin:/usr/sbin:/usr/local/bin:/usr/local/sbin \
    TERM=xterm-256color /bin/$(shell) --login \
    
}