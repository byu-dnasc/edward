SMRT_ROOT="" # path to "SMRT_ROOT" directory
PROXY_HOST=""
PROXY_DIR=$(dirname $(pwd)/$0)
CERT=$SMRT_ROOT/userdata/config/security/pb-smrtlink-default.crt
CERT_KEY=$SMRT_ROOT/userdata/config/security/pb-smrtlink-default.key
SL_PORT=8243
PROXY_PORT=8244
EDWARD_PORT=9093

[ -z "$PROXY_HOST" ] && echo "Please insert value of PROXY_HOST in $0." && exit 1
[ -z "$SMRT_ROOT" ] && echo "Please insert value of SMRT_ROOT in $0." && exit 1

# if the index.html file does not exist, generate it from template
if [ ! -f $PROXY_DIR/index.html ]; then
    cp $PROXY_DIR/template.html $PROXY_DIR/index.html
    sed -i "s|PROXY_HOST|$PROXY_HOST|g" $PROXY_DIR/index.html
    sed -i "s|PROXY_PORT|$PROXY_PORT|g" $PROXY_DIR/index.html
fi

# if nginx.conf file does not exist, generate it from template
if [ ! -f $PROXY_DIR/nginx.conf ]; then
    cp $PROXY_DIR/template.conf $PROXY_DIR/nginx.conf
    sed -i "s|CERT|$CERT|g" $PROXY_DIR/nginx.conf
    sed -i "s|SL_PORT|$SL_PORT|g" $PROXY_DIR/nginx.conf
    sed -i "s|CERT_KEY|$CERT_KEY|g" $PROXY_DIR/nginx.conf
    sed -i "s|PROXY_DIR|$PROXY_DIR|g" $PROXY_DIR/nginx.conf
    sed -i "s|PROXY_PORT|$PROXY_PORT|g" $PROXY_DIR/nginx.conf
    sed -i "s|EDWARD_PORT|$EDWARD_PORT|g" $PROXY_DIR/nginx.conf
fi

# run nginx
if [ $1 = "start" ]; then
    if [ -f $PROXY_DIR/nginx.pid ]; then
        echo "Nginx is already running."
        exit 1
    fi
    nginx -c $PROXY_DIR/nginx.conf -e $PROXY_DIR/error.log
    exit 0
elif [ $1 = "stop" ]; then
    nginx -c $PROXY_DIR/nginx.conf -e $PROXY_DIR/error.log -s stop
elif [ $1 = "reload" ]; then
    nginx -c $PROXY_DIR/nginx.conf -e $PROXY_DIR/error.log -s reload
else
    echo "Usage: $0 {start|stop|reload}"
    exit 1
fi