# Copyright 2018 Lucas Walter
# All rights reserved.
#
# Software License Agreement (BSD License 2.0)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Lucas Walter nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import os
from pathlib import Path  # noqa: E402
import sys

# Hack to get relative import of .camera_config file working
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from camera_config import CameraConfig, USB_CAM_DIR  # noqa: E402

from launch import LaunchDescription  # noqa: E402
from launch.actions import DeclareLaunchArgument, GroupAction  # noqa: E402
from launch.substitutions import LaunchConfiguration, PythonExpression  # noqa: E402
from launch_ros.actions import Node  # noqa: E402
from launch_ros.parameter_descriptions import ParameterValue  # noqa: E402


CAMERAS = []
CAMERAS.append(
    CameraConfig(
        name='camera1',
        param_path=Path(USB_CAM_DIR, 'config', 'params_1.yaml')
    )
    # Add more Camera's here and they will automatically be launched below
)

CAMERAS.append(
    CameraConfig(
        name='camera2',
        param_path=Path(USB_CAM_DIR, 'config', 'params_2.yaml')
    )
    # Add more Camera's here and they will automatically be launched below
)

CAMERAS.append(
    CameraConfig(
        name='camera3',
        param_path=Path(USB_CAM_DIR, 'config', 'params_3.yaml')
    )
    # Add more Camera's here and they will automatically be launched below
)

def generate_launch_description():
    ld = LaunchDescription()

    log_display = LaunchConfiguration('log_display')
    log_display_param = ParameterValue(log_display, value_type=bool)
    log_level = PythonExpression([
        "'debug' if '",
        log_display,
        "'.lower() in ['true', '1', 'yes', 'on'] else 'warn'",
    ])

    ld.add_action(
        DeclareLaunchArgument(
            'log_display',
            default_value='false',
            description='Show usb_cam informational and timing logs when true.'
        )
    )

    parser = argparse.ArgumentParser(description='usb_cam demo')
    parser.add_argument('-n', '--node-name', dest='node_name', type=str,
                        help='name for device', default='usb_cam')

    camera_nodes = [
        Node(
            package='usb_cam', executable='usb_cam_node_exe', output='screen',
            name=camera.name,
            namespace=camera.namespace,
            parameters=[
                camera.param_path,
                {
                    'log_display': log_display_param,
                    # 'image_raw.ffmpeg.encoder': 'h264_vaapi',
                    # 'image_raw.ffmpeg.bit_rate': 3000000,
                    # 'image_raw.ffmpeg.gop_size': 10,
                    # 'image_raw.ffmpeg.qmax': 30,
                    # 'image_raw.ffmpeg.encoder_av_options': 'profile:main',
                },
            ],
            remappings=camera.remappings,
            arguments=['--ros-args', '--log-level', log_level]
        )
        for camera in CAMERAS
    ]

    camera_group = GroupAction(camera_nodes)

    ld.add_action(camera_group)
    return ld
