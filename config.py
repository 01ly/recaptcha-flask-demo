#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    @author     :   xstatus
    @time       :   2020/12/31 19:41
    @email      :   crawler@88.com
    @project    :   reCAPTCHA demo -> config.py
    @IDE        :   PyCharm
    @describe   :   密钥配置
"""

class Ddict(dict):
    def __getattr__(self, item):
        return self.get(item)

# recaptcha 版本对应的模式及密钥对
Keys = Ddict({

    # reCAPTCHA v2版本
    'V2':Ddict({
        # 域名标识键,去除英文点“.”,比如域名：recaptcha.1991.site 可以写为：recaptcha1991site
        'localhost':Ddict({
            # 复选框模式checkbox
            'checkbox':Ddict({
                'site_key':'xxxx',
                'secret_key':'xxxx',
            }),
            # 后台隐藏模式invisible
            'invisible':Ddict({
                'site_key':'xxxx',
                'secret_key':'xxxx',
            })
        })
    }),
    # reCAPTCHA v3版本
    'V3':Ddict({
        # 域名标识键,去除英文点“.”,比如域名：recaptcha.1991.site 可以写为：recaptcha1991site
        'localhost':Ddict({
            'site_key':'xxxx',
            'secret_key':'xxxx',
        })
    })
})


