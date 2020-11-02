# coding:utf-8
# Copyright (c) 2020  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json

import yaml
from easydict import EasyDict

import paddlehub.env as hubenv


class HubConfig:
    '''
    PaddleHub configuration management class. Each time the PaddleHub package is loaded, PaddleHub will set the
    corresponding functions according to the configuration obtained in HubConfig, such as the log level of printing,
    server address and so on. When the configuration is modified, PaddleHub needs to be reloaded to take effect.
    '''

    def __init__(self):
        self._initialize()
        self.file = os.path.join(hubenv.CONF_HOME, 'config.yaml')
        with open(self.file, 'r') as file:
            try:
                cfg = yaml.load(file, Loader=yaml.FullLoader)
                self.data.update(cfg)
            except:
                ...

    def _initialize(self):
        # Set default configuration values.
        self.data = EasyDict()
        self.data.server = 'http://paddlepaddle.org.cn/paddlehub'
        self.data.log = EasyDict()
        self.data.log.enable = True
        self.data.log.level = 'DEBUG'

    def reset(self):
        '''Reset configuration to default.'''
        self._initialize()
        self.flush()

    @property
    def log_level(self):
        '''
        The lowest output level of PaddleHub logger. Logs below the specified level will not be displayed. The default
        is Debug.
        '''
        return self.data.log.level

    @log_level.setter
    def log_level(self, level: str):
        from paddlehub.utils import log
        if not level in log.log_config.keys():
            raise ValueError('Unknown log level {}. The valid values are {}'.format(level, list(log.log_config.keys())))

        self.data.log.level = level
        self.flush()

    @property
    def log_enable(self):
        '''Whether to enable the PaddleHub logger to take effect. The default is True.'''
        return self.data.log.enable

    @log_enable.setter
    def log_enable(self, enable: bool):
        self.data.log.enable = enable
        self.flush()

    @property
    def server(self):
        '''PaddleHub Module server url.'''
        return self.data.server

    @server.setter
    def server(self, url: str):
        self.data.server = url
        self.flush()

    def flush(self):
        '''Flush the current configuration into the configuration file.'''
        with open(self.file, 'w') as file:
            # convert EasyDict to dict
            cfg = json.loads(json.dumps(self.data))
            yaml.dump(cfg, file)

    def __str__(self):
        cfg = json.loads(json.dumps(self.data))
        return yaml.dump(cfg)


def _load_old_config(config: HubConfig):
    # The old version of the configuration file is obsolete, read the configuration value and delete it.
    old_cfg_file = os.path.join(hubenv.CONF_HOME, 'config.json')
    if os.path.exists(old_cfg_file):
        with open(old_cfg_file) as file:
            try:
                cfg = json.loads(file.read())
                config.server = cfg['server_url']
                config.log_level = cfg['log_level']
            except:
                ...
        os.remove(old_cfg_file)


config = HubConfig()
_load_old_config(config)