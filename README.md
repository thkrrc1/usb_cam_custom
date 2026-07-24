# usb_cam [![ROS 2 CI](https://github.com/ros-drivers/usb_cam/actions/workflows/build_test.yml/badge.svg)](https://github.com/ros-drivers/usb_cam/actions/workflows/build_test.yml)

## V4L USBカメラ用ROS 2ドライバ

このパッケージは、UVC全般ではなく、特にV4Lデバイスを対象として作られています。

ROS 1のドキュメントについては、[ROS Wiki](http://ros.org/wiki/usb_cam)を参照してください。

## 事前インストール
以下の動作に必要なパッケージインストールします。
```shell
sudo apt install ros-jazzy-compressed-image-transport python3-pydantic libopencv ros-jazzy-camera-info-manager v4l-utils
```

## udev設定
USBをPCにまだ登録していない場合は、登録する必要があります。
＊＊注意＊＊　Moswell製のカメラについてユニークIDが存在しないためUSBポートの位置と型番で判断しています（通常はユニークIDを使用すること）。

まず、デバイスがどの`videoID`が割り振られているか確認します。
```shell
v4l2-ctl --list-devices
```

以下のコマンドからデバイスIDを確認します。
```shell
udevadm info --query=all --name=/dev/video0 | grep -E 'ID_SERIAL|ID_SERIAL_SHORT|ID_VENDOR_ID|ID_MODEL_ID|ID_PATH|DEVLINKS'
```
・出力例
```shell
E: ID_MODEL_ID=0100
E: ID_SERIAL=MOSWELL_CO._LTD._MS-M2326FHU2
E: ID_VENDOR_ID=288c
E: ID_PATH_WITH_USB_REVISION=pci-0000:00:14.0-usbv2-0:4.3:1.0
E: ID_PATH=pci-0000:00:14.0-usb-0:4.3:1.0
E: ID_PATH_TAG=pci-0000_00_14_0-usb-0_4_3_1_0
E: DEVLINKS=/dev/camera_right /dev/v4l/by-id/usb-MOSWELL_CO._LTD._MS-M2326FHU2-video-index0 /dev/v4l/by-path/pci-0000:00:14.0-usb-0:4.3:1.0-video-index0 /dev/v4l/by-path/pci-0000:00:14.0-usbv2-0:4.3:1.0-video-index0
```

udevファイルの作成を作成します。

```shell
sudo -E gedit /etc/udev/rules.d/99-usb_camera.rules
```

記入例
```shell
SUBSYSTEM=="video4linux", ENV{ID_SERIAL}=="MOSWELL_CO._LTD._MS-M2326FHU2", ENV{ID_PATH}=="pci-0000:00:14.0-usb-0:4.3:1.0", ATTR{index}=="0", SYMLINK+="camera_right"
```


## ソースからのビルド

ソースコードをワークスペースへクローンまたはダウンロードします。

```shell
cd /ros2/jazzy/src
git clone https://github.com/thkrrc1/usb_cam_custom.git
```

ダウンロード後、ROS 2のアンダーレイ環境をsource済みであることを確認してから、依存パッケージをインストールします。

```shell
cd /ros2/jazzy/
rosdep install --from-paths src --ignore-src -y
```

これで、`usb_cam_custom`パッケージのビルドに必要な依存パッケージがすべてインストールされます。

```shell
cd /ros2/jazzy/
colcon build　--symlink-install
source install/setup.bash
```

ビルドが正常に完了したら、新しくビルドしたパッケージの環境を必ずsourceしてください。
source後は、次のセクションで示す3通りの方法のいずれかでパッケージを実行できます。

## 実行方法
`usb_cam_custom/config/params1.yaml`ディレクトリにパラメータファイルを用意しています。
＊＊注意＊＊　起動前にudev設定にて設定したデバイスIDに変更してください。
例：video_device: "/dev/video0"→　video_device: "/dev/camera_right"　　
　　　　　　　
```shell
# 上記と同じ `usb_cam_custom/config/params.yaml` を読み込むusb_cam実行ファイルと、
# 追加の画像表示ノードをlaunchファイルから起動する
ros2 launch usb_cam camera.launch.py
```

## 対応フォーマット

<a id="device-supported-formats"></a>
### デバイスが対応するフォーマット

接続されているデバイスが対応するフォーマットを確認するには、`usb_cam_node`を実行し、コンソール出力を確認します。

出力例を以下に示します。

```log
This devices supproted formats:
       Motion-JPEG: 1280 x 720 (30 Hz)
       Motion-JPEG: 960 x 540 (30 Hz)
       Motion-JPEG: 848 x 480 (30 Hz)
       Motion-JPEG: 640 x 480 (30 Hz)
       Motion-JPEG: 640 x 360 (30 Hz)
       YUYV 4:2:2: 640 x 480 (30 Hz)
       YUYV 4:2:2: 1280 x 720 (10 Hz)
       YUYV 4:2:2: 640 x 360 (30 Hz)
       YUYV 4:2:2: 424 x 240 (30 Hz)
       YUYV 4:2:2: 320 x 240 (30 Hz)
       YUYV 4:2:2: 320 x 180 (30 Hz)
       YUYV 4:2:2: 160 x 120 (30 Hz)
```

### ドライバが対応するフォーマット

ドライバ側にも対応フォーマットがあります。詳細については、[ソースコード](include/usb_cam/formats/)を参照してください。

[デバイスが対応するフォーマット](#device-supported-formats)を確認した後、[パラメータファイル](config/params.yaml)の`pixel_format`パラメータで使用するフォーマットを指定します。


## 圧縮

このトピックに関する情報を提供している[`ros2_v4l2_camera`パッケージ](https://gitlab.com/boldhearts/ros2_v4l2_camera#usage-1)と、そのドキュメントに感謝します。

システムに`image_transport_plugins`パッケージがインストールされていれば、`usb_cam`は`image_transport`を使用して画像を配信するため、デフォルトで圧縮画像に対応します。プラグインがインストールされている場合、`usb_cam`パッケージは`compressed`トピックを自動的に配信します。

現時点では、`rviz2`と`show_image.py`は圧縮画像の表示に対応していません。そのため、圧縮画像を後段で再配信し、非圧縮画像へ変換する必要があります。

```shell
ros2 run image_transport republish compressed raw --ros-args --remap in/compressed:=image_raw/compressed --remap out:=image_raw/uncompressed
```

## ドキュメント

[Doxygen](http://docs.ros.org/indigo/api/usb_cam/html/)のファイルは、ROS Wikiで確認できます。

### ライセンス

usb_camはBSDライセンスで公開されています。利用条件の全文については、[LICENSE](LICENSE)ファイルを参照してください。

### 作者

コントリビューターの完全な一覧については、[AUTHORS](AUTHORS.md)ファイルを参照してください。
