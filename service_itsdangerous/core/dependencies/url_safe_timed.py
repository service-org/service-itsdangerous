#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from service_itsdangerous.constants import ITSDANGEROUS_CONFIG_KEY
from service_itsdangerous.core.client import URLSafeTimedSerializerClient

from service_core.core.service.dependency import Dependency

logger = getLogger(__name__)


class URLSafeTimedSerializer(Dependency):
    """ URLSafeTimedSerializer依赖类

    doc: https://itsdangerous.palletsprojects.com/en/2.0.x/concepts/#the-salt
    """

    name = 'URLSafeTimedSerializer'

    def __init__(
            self,
            alias: t.Text,
            serializer_options: t.Optional[t.List[t.Dict[t.Text, t.Any]]] = None,
            **kwargs: t.Any
    ) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param serializer_options: 序列化配置
        """
        self.alias = alias
        self.client = None
        self.serializer_options = serializer_options or {}
        super(URLSafeTimedSerializer, self).__init__(**kwargs)

    def setup(self) -> None:
        """ 声明周期 - 载入阶段 """
        serializer_options = self.container.config.get(f'{ITSDANGEROUS_CONFIG_KEY}.{self.alias}.serializer_options', default={})
        # 防止YAML中声明值为None
        self.serializer_options = (serializer_options or {}) | self.serializer_options
        self.client = URLSafeTimedSerializerClient(**self.serializer_options)

    def get_instance(self) -> URLSafeTimedSerializerClient:
        """ 获取注入对象

        @return: URLSafeTimedSerializerClient
        """
        return self.client
