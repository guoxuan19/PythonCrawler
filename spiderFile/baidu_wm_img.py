# import requests
# import re
#
# url = 'http://image.baidu.com/search/index'
# date = {
#     'cl': '2',
#     'ct': '201326592',
#           'fp': 'result',
#           'gsm': '1e',
#           'ie': 'utf-8',
#           'ipn': 'rj',
#           'istype': '2',
#           'lm': '-1',
#           'nc': '1',
#           'oe': 'utf-8',
#           'pn': '30',
#           'queryword': '唯美意境图片',
#           'rn': '30',
#           'st': '-1',
#           'tn': 'resultjson_com',
#           'word': '唯美意境图片'
# }
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
#     'Accept': 'text/plain, */*; q=0.01',
#     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
#     'Accept-Encoding': 'gzip, deflate',
#     'X-Requested-With': 'XMLHttpRequest',
#     'Referer': 'http://image.baidu.com/search/index?ct=201326592&cl=2&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs3&word=%E5%94%AF%E7%BE%8E%E6%84%8F%E5%A2%83%E5%9B%BE%E7%89%87&ofr=%E9%AB%98%E6%B8%85%E6%91%84%E5%BD%B1',
#     'Cookie': 'BDqhfp=%E5%94%AF%E7%BE%8E%E6%84%8F%E5%A2%83%E5%9B%BE%E7%89%87%26%26NaN-1undefined-1undefined%26%260%26%261; Hm_lvt_737dbb498415dd39d8abf5bc2404b290=1455016371,1455712809,1455769605,1455772886; PSTM=1454309602; BAIDUID=E5493FD55CFE5424BA25B1996943B3B6:FG=1; BIDUPSID=B7D6D9EFA208B7B8C7CB6EF8F827BD4E; BDUSS=VSeFB6UXBmRWc3UEdFeXhKOFRvQm4ySmVmTkVEN2N0bldnM2o5RHdyaE54ZDlXQVFBQUFBJCQAAAAAAAAAAAEAAABzhCtU3Mbj5cfl0e8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE04uFZNOLhWZW; H_PS_PSSID=1447_18282_17946_15479_12166_18086_10634; Hm_lpvt_737dbb498415dd39d8abf5bc2404b290=1455788775; firstShowTip=1; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm',
#     'Connection': 'keep-alive'
# }
#
#
# def get_page(url, date, headers):
#     page = requests.get(url, date, headers=headers).text
#     return page
#
#
# def get_img(page, headers):
#     reg = re.compile('http://.*?\.jpg')
#     imglist = re.findall(reg, page)[::3]
#     x = 0
#     for imgurl in imglist:
#         with open('E:/Pic/%s.jpg' % x, 'wb') as file:
#             file.write(requests.get(imgurl, headers=headers).content)
#             x += 1
#
# if __name__ == '__main__':
#     page = get_page(url, date, headers)
#     get_img(page, headers)



# 以上是过时脚本，此脚本主要目的是抓取百度图片`唯美意境`模块。
import requests
import re
import os
import hashlib
from urllib.parse import unquote

# 使用现代的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 百度图片搜索的API地址
url = 'https://image.baidu.com/search/acjson'


def get_page(word, headers):
    """获取搜索结果页面"""
    # 构造适用于新API的参数
    params = {
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
        'pn': 30,
        'rn': 30,
        'gsm': '1e',
    }

    print(f"正在搜索关键词: '{word}'...")
    # GET请求应该使用 'params' 参数来传递数据
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()  # 如果请求失败则抛出异常
    page = response.text
    print("--- 成功获取百度返回数据 ---")
    return page


def get_img(page, headers):
    """从页面中解析并下载图片，使用hash命名以防重复"""
    # 创建一个新目录来保存唯美图片，避免混淆
    save_dir = 'images_wm'
    os.makedirs(save_dir, exist_ok=True)
    print(f"图片将保存在 '{save_dir}' 文件夹中。")

    # 使用 'middleURL'，它通常是直接的图片链接
    reg = re.compile('"middleURL":"(.*?)"')
    img_urls = re.findall(reg, page)
    print(f"成功解析出 {len(img_urls)} 个图片链接。")

    if not img_urls:
        print("在返回的数据中未找到图片链接，可能是接口规则已更新。")
        return

    download_count = 0
    for img_url in img_urls:
        try:
            decoded_url = unquote(img_url)
            if not decoded_url:
                print("发现空的图片链接，跳过。")
                continue

            # 使用URL的MD5哈希值作为文件名，避免重复和覆盖
            file_hash = hashlib.md5(decoded_url.encode()).hexdigest()
            filepath = os.path.join(save_dir, f'{file_hash}.jpg')

            if os.path.exists(filepath):
                print(f"图片已存在，跳过: {filepath}")
                continue

            print(f"正在下载: {decoded_url} ...")
            response = requests.get(decoded_url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()

            content_type = response.headers.get('content-type')
            if not content_type or not content_type.startswith('image'):
                print(f"链接非图片格式，跳过: {decoded_url}")
                continue

            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

            print(f"成功保存图片至: {filepath}")
            download_count += 1
        except requests.exceptions.RequestException as e:
            print(f"下载失败: {decoded_url}. 错误: {e}")
        except Exception as e:
            print(f"处理链接时发生未知错误: {decoded_url}. 错误: {e}")

    print(f"\n本次运行新下载了 {download_count} 张图片。")


if __name__ == '__main__':
    # 脚本的核心搜索词
    search_term = '唯美意境图片'

    try:
        page_content = get_page(search_term, headers)
        get_img(page_content, headers)
    except requests.exceptions.RequestException as e:
        print(f"无法从百度获取搜索结果. 错误: {e}")
    except Exception as e:
        print(f"程序运行出错: {e}")
