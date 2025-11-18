# import requests
# import re
#
# url = 'http://image.baidu.com/search/index'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Accept-Encoding': 'gzip, deflate',
#     'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&fm=detail&lm=-1&st=-1&sf=2&fmq=&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%AB%98%E6%B8%85%E6%91%84%E5%BD%B1&oq=%E9%AB%98%E6%B8%85%E6%91%84%E5%BD%B1&rsp=-1',
#     'Cookie': 'HOSUPPORT=1; UBI=fi_PncwhpxZ%7ETaMMzY0i9qXJ9ATcu3rvxFIc-a7KI9byBcYk%7EjBVmPGIbL3LTKKJ2D17mh5VfJ5yjlCncAb2yhPI5sZM51Qo7tpCemygM0VNUzuTBJwYF8OYmi3nsCCzbpo5U9tLSzkZfcQ1rxUcJSzaipThg__; HISTORY=fec845b215cd8e8be424cf320de232722d0050; PTOKEN=ff58b208cc3c16596889e0a20833991d; STOKEN=1b1f4b028b5a4415aa1dd9794ff061d312ad2a822d52418f3f1ffabbc0ac6142; SAVEUSERID=0868a2b4c9d166dc85e605f0dfd153; USERNAMETYPE=3; PSTM=1454309602; BAIDUID=E5493FD55CFE5424BA25B1996943B3B6:FG=1; BIDUPSID=B7D6D9EFA208B7B8C7CB6EF8F827BD4E; BDUSS=VSeFB6UXBmRWc3UEdFeXhKOFRvQm4ySmVmTkVEN2N0bldnM2o5RHdyaE54ZDlXQVFBQUFBJCQAAAAAAAAAAAEAAABzhCtU3Mbj5cfl0e8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE04uFZNOLhWZW; H_PS_PSSID=1447_18282_17946_18205_18559_17001_17073_15479_12166_18086_10634; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm',
# }
#
#
# def get_html(url, headers):
#     data = {
#         'cl': '2',
#         'ct': '201326592',
#               'face': '0',
#               'fp': 'result',
#               'gsm': '200001e',
#               'ic': '0',
#               'ie': 'utf-8',
#               'ipn': 'rj',
#               'istype': '2',
#               'lm': '-1',
#               'nc': '1',
#               'oe': 'utf-8',
#               'pn': '30',
#               'queryword': '高清摄影',
#               'rn': '30',
#               'st': '-1',
#               'tn': 'resultjson_com',
#               'word': '高清摄影'
#     }
#
#     page = requests.get(url, data, headers=headers).text
#     return page
#
#
# def get_img(page, headers):
#     #     img_url_list = []
#     reg = re.compile('http://.*?\.jpg')
#     imglist1 = re.findall(reg, page)
#     imglist2 = imglist1[0: len(imglist1): 3]
#     #   [img_url_list.append(i) for i in imglist if not i in img_url_list]
#     x = 0
#     for imgurl in imglist2:
#         bin = requests.get(imgurl, headers=headers).content
#         with open('./%s.jpg' % x, 'wb') as file:
#             file.write(bin)
#             x += 1
#
# if __name__ == '__main__':
#     page = get_html(url, headers)
#     get_img(page, headers)









# 以上代码都是过时了，百度图片搜索的API接口已经发生了变化，导致旧的请求方式无法获取数据，原始代码中的requests.get方法的参数使用不正确
# 这份代码是按顺序获取百度图片搜索结果中的图片链接，然后按顺序下载这些图片。

import requests
import re
import os
from urllib.parse import unquote

# 使用现代的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 更新为当前百度图片搜索的API地址
url = 'https://image.baidu.com/search/acjson'


def get_html(word, headers):
    """获取搜索结果页面的HTML"""
    # 构造适用于新API的参数
    data = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592',
        'is': '',
        'fp': 'result',
        'queryWord': word,
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '-1',
        'z': '',
        'ic': '0',
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': word,
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '0',
        'istype': '2',
        'qc': '',
        'nc': '1',
        'fr': '',
        'pn': 30,  # 从第30条结果开始
        'rn': 30,  # 每页返回30条结果
        'gsm': '1e',
    }

    print(f"正在搜索关键词: '{word}'...")
    # GET请求应该使用 'params' 参数来传递数据
    response = requests.get(url, params=data, headers=headers)
    response.raise_for_status()  # 如果请求失败则抛出异常
    page = response.text
    print("--- 成功获取百度返回数据 (前500字符) ---")
    print(page[:500])
    print("---------------------------------------------")
    return page

# def get_img(page, headers):
#     """从HTML页面中解析并下载图片"""
#     # 创建一个名为 'images' 的文件夹来保存图片
#     save_dir = 'images'
#     os.makedirs(save_dir, exist_ok=True)
#     print(f"图片将保存在 '{save_dir}' 文件夹中。")
#
#     # 使用更精确的正则表达式来匹配JSON响应中的图片URL
#     reg = re.compile('"objURL":"(.*?)"')
#     img_urls = re.findall(reg, page)
#     print(f"成功解析出 {len(img_urls)} 个图片链接。")
#
#     if not img_urls:
#         print("在返回的数据中未找到图片链接，可能是接口规则已更新。")
#         return
#
#     x = 0
#     for img_url in img_urls:
#         try:
#             # Baidu返回的URL可能需要解码
#             decoded_url = unquote(img_url)
#             print(f"正在下载: {decoded_url} ...")
#
#             bin_content = requests.get(decoded_url, headers=headers, timeout=20).content
#             filepath = os.path.join(save_dir, f'{x}.jpg')
#
#             with open(filepath, 'wb') as file:
#                 file.write(bin_content)
#
#             print(f"成功保存图片至: {filepath}")
#             x += 1
#         except requests.exceptions.RequestException as e:
#             print(f"下载失败: {decoded_url}. 错误: {e}")
#         except Exception as e:
#             print(f"处理链接时发生未知错误: {decoded_url}. 错误: {e}")

def get_img(page, headers):
    """从HTML页面中解析并下载图片"""
    # 创建一个名为 'images' 的文件夹来保存图片
    save_dir = 'images'
    os.makedirs(save_dir, exist_ok=True)
    print(f"图片将保存在 '{save_dir}' 文件夹中。")

    # 使用 'middleURL'，它通常是直接的图片链接，比 'objURL' 更可靠
    reg = re.compile('"middleURL":"(.*?)"')
    img_urls = re.findall(reg, page)
    print(f"成功解析出 {len(img_urls)} 个图片链接。")

    if not img_urls:
        print("在返回的数据中未找到图片链接，可能是接口规则已更新。")
        return

    x = 0
    for img_url in img_urls:
        try:
            # middleURL 通常不需要解码，但保留 unquote 以防万一
            decoded_url = unquote(img_url)

            # 新增检查，如果URL为空字符串，则跳过
            if not decoded_url:
                print("发现空的图片链接，跳过。")
                continue

            print(f"正在下载: {decoded_url} ...")

            # 使用流式下载，并增加超时
            response = requests.get(decoded_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()

            # 检查Content-Type头，确保是图片
            content_type = response.headers.get('content-type')
            if not content_type or not content_type.startswith('image'):
                print(f"链接非图片格式，跳过: {decoded_url}")
                continue

            filepath = os.path.join(save_dir, f'{x}.jpg')

            with open(filepath, 'wb') as file:
                # 以块的方式写入文件，优化大文件下载
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"成功保存图片至: {filepath}")
            x += 1
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {decoded_url}. 错误: {e}")
        except Exception as e:
            print(f"处理链接时发生未知错误: {decoded_url}. 错误: {e}")


if __name__ == '__main__':
    search_term = '高清摄影'  # 定义搜索关键词
    try:
        html_page = get_html(search_term, headers)
        get_img(html_page, headers)
        print("\n所有图片下载完成。")
    except requests.exceptions.RequestException as e:
        print(f"无法从百度获取搜索结果. 错误: {e}")
    except Exception as e:
        print(f"程序运行出错: {e}")


