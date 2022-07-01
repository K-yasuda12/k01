## 環境のセットアップ（RTP周り）

想定環境は以下  
* SD Image
  * k04 sdcard

### Install packages

* aptで入れられるもの

```
sudo apt update && sudo apt install libmicrohttpd-dev libjansson-dev libssl-dev libsofia-sip-ua-dev libglib2.0-dev libopus-dev libogg-dev libcurl4-openssl-dev liblua5.3-dev libconfig-dev pkg-config gengetopt libtool automake make git meson ninja-build ffmpeg
```

* libnice

```
git clone https://gitlab.freedesktop.org/libnice/libnice
cd libnice
meson --prefix=/usr --libdir=lib build
ninja -C build
sudo ninja -C build install
```

* libsrtp

```
wget https://github.com/cisco/libsrtp/archive/refs/tags/v2.4.2.tar.gz
tar xfv v2.4.2.tar.gz
cd libsrtp-2.4.2
./configure --prefix=/usr --enable-openssl
make shared_library && sudo make install
```

* janus

```
git clone https://github.com/meetecho/janus-gateway.git
cd janus-gateway
./autogen.sh
./configure --prefix=/opt/janus --disable-aes-gcm
make
sudo make install
sudo make configs
sudo cp ./janus/janus.plugin.streaming.jcfg /opt/janus/etc/janus/janus.plugin.streaming.jcfg
```

ここまででrtp関連は完了

* Refs: 
  * https://www.mikan-tech.net/entry/2020/05/02/173000
  * https://www.mikan-tech.net/entry/raspi-janus-streaming


## 起動

ターミナルを複数使う(nohupで切り離しても良いかも)  

1. 設定の書き換え  

```
vi team2-frontend/src/App.vue
# L21のconst JANUS_URL,axios postをRaspberry PiのIP:8088/janusに書き換え
const JANUS_URL = 'http://192.168.1.220:8088/janus'
axios.post('http://192.168.1.220:5000/cam', {
```

2. 関連するプロセスの立ち上げ

* janus

```
cd /opt/janus
sudo ./bin/janus
```

* ffmpeg

```
ffmpeg -f v4l2 -thread_queue_size 8192 -input_format yuyv422 -video_size 1280x720 -framerate 10 -i /dev/video0 -c:v h264_omx -profile:v baseline -b:v 1M -bf 0 -flags:v +global_header -bsf:v "dump_extra=freq=keyframe" -max_delay 0 -an -bufsize 1M -vsync 1 -g 10 -f rtp rtp://127.0.0.1:8004/
```

* vue(npm,yarn周りがまだの場合は次のセクション)

```
cd ./team2-frontend
yarn install
yarn serve
```

* GPIO用Flaskサーバの立ち上げ

(CORSのえらーが出る場合は以降のflask-corsをインストール)

```
cd <このプロジェクトのディレクトリ>
python3 app.py
```

* アクセス  
  yarnの起動まで完了したらブラウザから http://<raspberrypiのアドレス>:8080/ にアクセスし、「H.264 livestream ～」を選択してStart

### Install Node.js

参考にしたサイトではVue.jsでインストールしていたため、以下の手順でNode.js周りの環境を整える。

```
sudo apt install nodejs npm
sudo -E npm install -g n
sudo -E n stable
exec $SHELL -l
npm install yarn
```

## cors対策（Raspberry Pi内であれば必要ない）

```
pip3 install -U flask-cors
```


### Appendix

projectを作る場合は以下
```
sudo -E npm install -g @vue/cli
vue create team2-streaming
```

#### WebIOPiのインストール

TODO: まだWebIOPi周りは完成していないけど、とりあえず動かせる環境を。

```
wget http://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
tar zxvf WebIOPi-0.7.1.tar.gz
git clone https://github.com/pochiken/pn-webiopi.git
cd WebIOPi-0.7.1/
patch -p1 < ../pn-webiopi/WebIOPi-RPiALL.patch
sudo ./setup.sh
cd /etc/systemd/system/
sudo wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi.service
sudo systemctl start webiopi
sudo systemctl enable webiopi
```


## install docker

TODO: ここの章はインストールを簡単にしようと思ったものの、Hardware Encode周りが上手くいかなかったので無視してください。

```
curl -sSL https://get.docker.com | sh
sudo usermod -a -G docker pi
sudo systemctl start docker
sudo systemctl enable docker
pip3 install docker-compose
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bash_profile
# hwclock対策
wget http://ftp.jp.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.5.4-1_armhf.deb
sudo dpkg -i libseccomp2_2.5.4-1_armhf.deb
```
