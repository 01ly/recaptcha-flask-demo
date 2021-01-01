# recaptcha-flask-demo
A demo of Google reCAPTCHA v2 and v3 by Flask.

## 0.了解谷歌reCAPTCHA

`reCAPTCHA`是谷歌推出的免费人机识别技术，使用图像验证码/用户行为评分来区别当前网站应用的用户是机器人还是正常人类。当前有`v2`版本和新的`v3`版本，当然，攻守永恒，破解`reCAPTCHA`的大有人在，`unCaptcha2`就是一个例子，相关：

> -  [`reCAPTCHA`官网-（需要科学上网）](https://www.google.com/recaptcha) 
> -  [`reCAPTCHA`代码仓库-Github](https://github.com/google/recaptcha)
> -  [`reCAPTCHA`验证流程在线demo](https://recaptcha-demo.appspot.com/)
> -  [`reCAPTCHA`破解库`unCaptcha2`代码仓库Github](https://github.com/ecthros/uncaptcha2)

  作为谷歌强推的一款人机识别利器，`reCAPTCHA v2`使用图像/语音识别技术来区分人类和机器;`reCAPTCHA v3`则通过分析网站应用的大量用户流量进而使用其机器学习技术来识别用户行为并为其打分，分值范围`0.0~1.0`,得分越低的越表明当前用户是机器人。
  
 <!--more-->

> 假设我们的网站应用是属于`登录/注册`后进而后续操作的类型，那么防止用户滥注册或机器人登录破坏网站应用生态尤为重要，反爬/`anti-robot`迫在眉睫.而第一关卡就是阻止机器人/恶意注册程序进入我们网站应用的数据空间，将其拒之门外或者诱敌深入（爬虫蜜罐）。谷歌`reCAPTCHA`或许可以帮助我们实现基础的第一步：拒机器人/恶意程序于门外。

> 以下简称恶意程序或机器人为`攻击者`.

## 1.验证码(CAPTCHA)


一分为二地看，我们的网站应用被恶意爬取或机器人造访，必是有可图之物，比如某个功能强大的`路由`（页面工具），对于攻击者的意图有针对性的进行防护是基础反爬意识；其次，基于“料敌从宽 御敌从严”的理念，我们有必要预设攻击者的`攻击模型`，即攻击者可能使用的突破反爬的技术手段，进而采取对应的反爬措施。

对于我们的网站应用，有价值的工具或者页面操作需要在`注册/登录`后才能进一步访问，因而阻止攻击者高频次的注册/登录是首要矛盾。注册/登录验证码可以有效过滤掉一波攻击者。市面上的验证码一般有：

> ![识别颠倒文字](https://i.loli.net/2020/12/31/gxZmWRDUs37q4Mp.gif)
<img src="https://i.loli.net/2020/12/31/i8GdcVe3EDJRUQZ.jpg" width="250" height="200" align="left">
<img src="https://i.loli.net/2020/12/31/Hz7dRXAJgxOhCf6.png" width="250" height="200" align="left">
<img src="https://i.loli.net/2020/12/31/xITmp7LwRBXbNka.jpg" width="250" height="200" align="left">
<img src="https://i.loli.net/2020/12/31/k7jvn9qfwJrSclg.gif" width="250" height="200" align="left">
<img src="https://i.loli.net/2020/12/31/sXoKjOTaruCcy9B.gif" width="250" height="200" align="left">
<img src="https://i.loli.net/2020/12/31/eGR18Xk7Yud6ftV.png" width="250" height="200" align="left">
<img src="https://i.loli.net/2020/12/31/QUrTfYz5NC8OkSB.gif" width="250" height="200" align="left"><img src="https://i.loli.net/2020/12/31/ltevmJFSGxfAaWu.gif" width="250" height="200" align="center">





以上种种验证码只是当前验证码市场的一小部分，针对图像验证码，可以根据机器学习技术对大量的训练集进行学习，进一步达到破解的目的，亦或是接入人工打码平台，而对于简单的字符数字识别验证码，则有对应的成熟的第三方库可以轻易破解，网站应用加入验证码的目的只是提高或者延长攻击者的破解周期和成本代价而已。


## 2.Why reCAPTCHA?

谷歌`reCAPTCHA`两个版本的数据流均是前端点击识别/用户环境生成关键参数`g-recaptcha-response`对服务端进行验证查询,类似如下：
```json
{
    "g-recaptcha-response": "03AGdBq27snbv3yi57Y7mbBf2BY8JKo-KJdzgYtt4A5td07JoOMdPcYjVHGxRl5XR-twUQxlcURIUoYW8d0roXwm4qA0r5WxNFBzIr4Wu4hyNzodl0Mvn-jgd0qvu2YGWXY5X8UfTC67-sI2hkbwdy7K3giaHesVlhJQVg4vdfxvxBY-DfRwgATj77PrhPF_3XX43FCI29n8nYVk97JAFKFSH2lIlWQDBH6xCkk9x3MKHW7eTLxUOYd_S0Hj4Tz9C3gM7OmkG0oWKIM40cn112FsQ3QsvUYMlIneOhTr8GGXnsiGOM2iyFL8p1OtwIMrad5RjThYPRwitQjyFIRtEGgDceBobowaH46cv5aG34XUjsRd8Z6hjK3z1uN4mQJLfn7cFHfI1Z6GFyTjxRGIsFDZOOJBktCb9aBHlNKqui3m3xdGbVjF1-etN_xlo6i4VbzPPc4CBsfI956xrCYfEOdMU0cLGhzzHoAg",
}
```
此值`唯一且无法重复使用`，通过用户环境生成，可以作为注册登录携带的必要参数，服务端通过`私钥`与谷歌通信查询验证此值有效性从而达到识别人机的作用。

## 3.使用前准备

### 3.1 注册recaptcha密钥对

登录[Google reCAPTCHA（需科学上网）](https://www.google.com/recaptcha/admin/create)管理界面，点击创建recaptcha密钥对：
![Snipaste_2020-12-31_21-15-18.png](https://i.loli.net/2021/01/01/VzW6crYxgO3HmyZ.png)

### 3.2 保存密钥对
![Snipaste_2020-12-30_19-12-35.png](https://i.loli.net/2021/01/01/m9HfET1ivraO8GN.png)

第一个密钥为内嵌在网站应用上的`site_key`,第二个为服务端与Google通信用的密钥`secret_key`，不能外泄。

## 4.接入reCAPTCHA

本文使用`flask`作为后台服务框架，demo环境：
> - python3.7
> - win10 64位
> - requests

文件结构：
```text
recaptcha-demo
├── README.md
├── index.py #脚本服务器入口
├── config.py # 密钥对配置文件
├── gunicorn.conf.py # gunicorn运行配置脚本，适用于Linux环境
├── templates
│   ├── recaptcha-v2-checkbox.html # v2版本复选框模式
│   ├── recaptcha-v2-checkbox-explicit-rendering.html #v2版本多部件渲染
│   ├── recaptcha-v2-invisible.html #v2版本隐藏模式 
│   ├── recaptcha-v2-invisible-explicit-rendering.html #v2版本隐藏onload回调模式
│   ├── recaptcha-v2-invisible-invoke.html #v2版本隐藏主动调用模式
│   ├── recaptcha-v3.html #v3版本默认模式
│   └── recaptcha-v3-programmatically.html #v3版本程序显式调用模式
└── run.sh # Linux环境下快速启动脚本
```

密钥对配置：
```python


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
                'site_key':'xxxxx',
                'secret_key':'xxxxx',
            }),
            # 后台隐藏模式invisible
            'invisible':Ddict({
                'site_key':'xxxxx',
                'secret_key':'xxxxx',
            })
        })
    }),
    # reCAPTCHA v3版本
    'V3':Ddict({
        # 域名标识键,去除英文点“.”,比如域名：recaptcha.1991.site 可以写为：recaptcha1991site
        'localhost':Ddict({
            'site_key':'xxxxx',
            'secret_key':'xxxxx',
        })
    })
})

```

### 4.1 recaptcha v2

> 复选框checkbox 模式

前端页面`recaptcha-v2-checkbox.html`：
```html
<span style="font-size:14px;"><!DOCTYPE html>
<html lang="en">
<head>
    <title>reCAPTCHA v2 测试</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://www.recaptcha.net/recaptcha/api.js"></script>
</head>
<body>
 <script>
   function onSubmit(token) {
       //回调处理
       alert(token);
   }
 </script>
    <form action="/v2/verify/checkbox" method="post" id="demo-form">
        <input name="username" value="" placeholder="用户名，随便输入">
        <input name="version"  value="V2" hidden>
        <div class="g-recaptcha" data-sitekey="{{ site_key }}" data-action='login' data-callback="onSubmit" ></div>
        <p><button class="btn btn-primary" type="submit"  >Login</button>
    </form>
</body>
</html>
</span>
```
后端路由及验证函数：
```python

@app.route('/v2/checkbox')
def recaptcha_v2_checkbox():
    return render_template('recaptcha-v2-checkbox.html',site_key=Keys.V2.localhost.checkbox.site_key)
    

# ---- 验证路由 ----
@app.route('/v2/verify/checkbox',methods=['POST'])
@verify_recaptcha(Keys.V2.localhost.checkbox.secret_key)
def v2_verrify_checkbox():
    data = {
        'data':request.form,
        'verify':request.verify_response
    }
    return jsonify(data)
```

其中装饰器`verify_recaptcha`是两个版本统一与Google recaptcha通信验证的函数:

```python

def verify_recaptcha(SECRET_KEY):
    def outter(f):
        @functools.wraps(f)
        def wrapper(*args,**kwargs):
            request.verify_response = {}
            request.recaptcha_passed = False
            token = request.form.get('g-recaptcha-response')
            api = 'https://www.recaptcha.net/recaptcha/api/siteverify'
            data = {
                'response': token,
                'secret': SECRET_KEY,
                'remoteip': request.remote_addr
            }
            response = requests.post(api, data=data)
            result = response.json()
            if result.get('success'):
                request.verify_response = result
                request.recaptcha_passed = True
                return f(*args,**kwargs)
            else:
                return result,403
        return wrapper
    return outter
```

验证通过后返回数据示例：
```json
{
  "data": 
  {
    "g-recaptcha-response": "03AGdBq24IwuxxSrI66F_n0AQ6zrthAjVt7cGzvQ4JlfbptQVY8MybRxN_LlGbNxLyOa-9lOHp8iVquam9qBzf_BiwB_yBJcXvRIWlFjBcSUyozz7Sq-NLL53aOTsp4CeWbv_PWUKTTIQ3YRQH10xRCGoHUrU2nSdTb_x-my2HYjnXMJrHwbHXnzONWgLl4IwzoxJBv_S0s8iaqJGSj-7jPKDKw6MHBxIMAfMpJn46Uh2q_2yxax5Vox3DXt_F32WJIWrmhCmnx0xQtEZvVVSTaJxkzYJWEvuR_Nvt2JKrV2AfDFlkbc7idx90P6t8isyVsMDxEOBYZogzzGaWteaaU4FW015MVVBkxctbMkch0LP3_UZv70OC9_kpafEKNDT_1HUCT_EW48vEzWpBBDCbe4cMhJJx0-Ho_mrRWlL2LsdCJqXLGLQ-2IRFiBlTG6TWPCaaL72iDXLdpEjVo94eA87GPdx2ia32AxPnphPhWr_eSZvePD3DUbY",
    "username": "test",
    "version": "V2"
  },
  "verify": 
  {
    "challenge_ts": "2021-01-01T05:33:58Z",
    "hostname": "recaptcha.1991.site",
    "success": true
  }
}

```
验证失败返回示例：
```json
{
  "error-codes": 
  [
    "missing-input-response"
  ],
  "success": false
}

```

其中，`success`字段为`true`则表明验证通过，为`false`则表明验证失败。

对于我们想要使用`recaptcha v2`进行防护的任意路由，在其页面引入v2版本的html元素后，我们在服务端可以直接安上装饰器`verify_recaptcha`,例如对登录路由进行保护:
```python
@app.route('/login',methods=['POST'])
@verify_recaptcha(Keys.V2.localhost.checkbox.secret_key)
def login():
  if request.recaptcha_passed:
  # 进行登录操作
  else:
  #验证不通过操作

```

**在线测试demo: 点击==>[recaptcha.1991.site](http://recaptcha.1991.site:8888/v2/checkbox)**

### 4.2 recaptcha v3

> 默认自动绑定渲染模式

前端页面`recaptcha-v3.html`：
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>reCAPTCHA v3 </title>
    <script src="https://www.recaptcha.net/recaptcha/api.js"></script>
</head>
<body>
<h1>reCAPTCHA v3 测试</h1>
 <script>
   function onSubmit(token) {
       //回调处理
       console.log(token);
     document.getElementById("demo-form").submit();
   }
 </script>
<form action="/v3/verify" method="post" id="demo-form">
    <input name="username" value="" placeholder="用户名，随便输入">
    <input name="version" value="V3" hidden>
    <button class="g-recaptcha"
        data-sitekey="{{ site_key }}"
        data-callback='onSubmit'
        data-action='login'>提交</button>
</form>
</body>
</html>

```

后端路由及验证函数：
```python
# --- html模板路由 ---
@app.route('/v3')
def recaptcha_v3():
    return render_template('recaptcha-v3.html',site_key=Keys.V3.localhost.site_key)
    
# ---- 验证路由 ----    
@app.route('/v3/verify',methods=['POST'])
@verify_recaptcha(Keys.V3.localhost.secret_key)
def v3_verrify():
    data = {
        'data':request.form,
        'verify':request.verify_response,
        'score':request.verify_response.get('score') if request.recaptcha_passed else 0
    }
    return jsonify(data)
```
验证通过后返回数据示例：
```json

{
  "data": 
  {
    "g-recaptcha-response": "03AGdBq24idxSv7r61KK7TAkApl1qRkq_1B7sdqQqYuqASa9A-skQG6Oc7VFn74JkcVPQSgv3gAUmLfKe8iZQTVjadxrW5er-KnJ1lv4db9mHV1KIElLQo-mK_bpwx8CLV5WX04HhgBCXdaosWSftRK9gm6X7LowaVCAlAJy_DzSERK38Bqeepk01_z-joVGf9Rx0j_kJiBeUGyhOJXr0C5N1w2S62ESTtIqDbMjR1KxfOTM7uObOIB9dXeVyfDJzyKqz0qc2VtRlZ-JUAe2yJfwwISWUSfZeavqqSOLTkRb3xjbeOgYMDpQZIvzwuga8Jf0FOMljUCNj_EhpYO72WGANOud5RgSgHdgDJNNuEZng4X9FKdBn9whtV5cyw-0KktmSica8-CJBC6qnTtJhdgdjzVzOHj4YkyXpbe1nfEQxrylzAf_J1v3aARcXO_W8A2EPLwXbH68Jq",
    "username": "test",
    "version": "V3"
  },
  "score": 0.9,
  "verify": 
  {
    "action": "login",
    "challenge_ts": "2021-01-01T06:28:26Z",
    "hostname": "recaptcha.1991.site",
    "score": 0.9,
    "success": true
  }
}
```
v3版本的体验比v2版本的更加顺畅，因为其依赖的是评分机制，越接近`0.0`分则越表明当前用户是机器人从而可以给服务端进行对应处理。但是前提是当前网站的流量必须积累一段时间评分才会愈加精确，有更多的用户流量行为数据进行训练才会更加完善。**如果担心用户隐私的问题，建议慎重选择**

**在线测试demo: 点击==>[recaptcha.1991.site](http://recaptcha.1991.site:8888/v3)**

`v2\v3`其他模式的完整代码示例可见`GitHub`仓库:[recaptcha-flask-demo](https://github.com/01ly/recaptcha-flask-demo)


## 5.后台流量查看

登录`Google reCAPTCHA admin`[后台面板](https://www.google.com/recaptcha/admin)可查看最近网站应用`recaptcha`的流量情况:
![Snipaste_2020-12-31_21-15-50.png](https://i.loli.net/2021/01/01/IRUtEDMThqa5KQY.png)





