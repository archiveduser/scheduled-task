# generated by chatgpt
import requests
import re
import os
import json

# 定义项目列表
repolist = [
    {
        "name": "mihomo",
        "url": "https://github.com/MetaCubeX/mihomo",
        "filter": [".gz"],
    },
    {
        "name": "ClashMetaForAndroid",
        "url": "https://github.com/MetaCubeX/ClashMetaForAndroid",
        "filter": [".apk"],
    },
    {
        "name": "clash-verge-rev",
        "url": "https://github.com/clash-verge-rev/clash-verge-rev",
        "filter": [".exe", ".deb", ".dmg", "portable.zip"],
    },
    {
        "name": "qbittorrent-nox-static",
        "url": "https://github.com/userdocs/qbittorrent-nox-static",
        "filter": ["nox"],
    },
    {
        "name": "v2rayng",
        "url": "https://github.com/2dust/v2rayng",
        "filter": [".apk"],
    },
    {
        "name": "termux-app",
        "url": "https://github.com/termux/termux-app",
        "filter": [".apk"],
    },
    {
        "name": "winlator",
        "url": "https://github.com/brunodev85/winlator",
        "filter": [".apk"],
    },
    {
        "name": "MaterialFiles",
        "url": "https://github.com/zhanghai/MaterialFiles",
        "filter": [".apk"],
    },
    {
        "name": "Thanox",
        "url": "https://github.com/Tornaco/Thanox",
        "filter": [".apk"],
    },
    {
        "name": "moonlight-android",
        "url": "https://github.com/moonlight-stream/moonlight-android",
        "filter": [".apk"],
    },
    {
        "name": "alist",
        "url": "https://github.com/AlistGo/alist",
        "filter": [".gz", ".zip"],
    },
    {
        "name": "rclone",
        "url": "https://github.com/rclone/rclone",
        "filter": [".gz", ".zip"],
    },
    {
        "name": "magisk-delta",
        "url": "https://github.com/HuskyDG/magisk-files",
        "filter": [".apk"],
    },
    {
        "name": "magisk",
        "url": "https://github.com/topjohnwu/magisk",
        "filter": [".apk"],
    },
    {
        "name": "gkd",
        "url": "https://github.com/gkd-kit/gkd",
        "filter": [".apk"],
    },
    {
        "name": "LSPosed",
        "url": "https://github.com/LSPosed/LSPosed",
        "filter": [".zip"],
    },
]

repolist = sorted(repolist, key=lambda x: x['name'].lower())

REVERSE_PROXY_URL = os.getenv("REVERSE_PROXY_URL", "")


def get_github_releases(repo_url, limit=5, filter_ext=None):
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)/?", repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL")

    owner, repo = match.groups()

    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        releases = response.json()

        release_list = []
        count = 0
        for release in releases:
            # 跳过 Pre-release 版本
            #if release.get("prerelease", False):
            #    continue

            release_info = {
                "tag_name": release.get("tag_name", "Unnamed Tag"),
                "assets": [],
            }

            # 过滤链接的扩展名
            for asset in release.get("assets", []):
                url = asset.get("browser_download_url")
                if filter_ext:
                    if any(url.endswith(ext) for ext in filter_ext):
                        release_info["assets"].append(url)
                else:
                    release_info["assets"].append(url)

            release_list.append(release_info)
            count += 1

            # 只保留前 limit 个发布版本
            if count >= limit:
                break

        return release_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching releases for {repo_url}: {e}")
        return []


def generate_alist_tree(repolist, limit=5):
    tree = {}
    for repo in repolist:
        project_name = repo["name"]
        repo_url = repo["url"]
        filter_ext = repo.get("filter", [])
        releases = get_github_releases(repo_url, limit, filter_ext)
        tree[project_name] = {}

        for release in releases:
            release_name = release["tag_name"]
            tree[project_name][release_name] = release["assets"]

    return tree


def generate_alist_tree_text(tree):
    tree_lines = []
    for project, releases in tree.items():
        tree_lines.append(f"{project}:")
        for release, links in releases.items():
            tree_lines.append(f"  {release}:")
            for link in links:
                tree_lines.append(f"    {REVERSE_PROXY_URL}{link}")
    return "\n".join(tree_lines)


# 生成 Alist 地址树并保存到变量
alist_tree = generate_alist_tree(repolist, limit=10)

# 生成文本格式的目录树并保存到变量
alist_tree_text = generate_alist_tree_text(alist_tree)

# 打印生成的文本
print(alist_tree_text)

with open("/tmp/urltree", "a", encoding="utf8") as f:
    f.write(f"{alist_tree_text}\n")
