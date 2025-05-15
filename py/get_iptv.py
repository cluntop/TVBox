import re
import requests
from collections import OrderedDict
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

tv_urls = [
    "https://qu.ax/vUBde.txt",
    "http://live.nctv.top/x.txt",
    "https://json.doube.eu.org/XingHuo.txt",
    "https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt",
    "https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u",
    "https://raw.githubusercontent.com/YueChan/Live/refs/heads/main/APTV.m3u",
    "https://raw.githubusercontent.com/Wirili/IPTV/refs/heads/main/live.m3u",
    "https://raw.githubusercontent.com/wwb521/live/refs/heads/main/tv.m3u",
    "https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u",
    "https://live.zbds.top/tv/iptv4.txt",
    "https://live.zbds.top/tv/iptv6.txt",
]

def parse_template(template_file):
    template_channels = OrderedDict()
    current_category = None
    with open(template_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "#genre#" in line:
                    current_category = line.split(",")[0].strip()
                    template_channels[current_category] = []
                elif current_category:
                    channel_name = line.split(",")[0].strip()
                    template_channels[current_category].append(channel_name)
    return template_channels

def fetch_channels(url):
    channels = OrderedDict()
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        response.encoding = "utf-8"
        lines = response.text.split("\n")
        
        is_m3u = any("#EXTINF" in line for line in lines[:5])
        current_category = None

        if is_m3u:
            channel_name = ""
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    match = re.search(r'group-title="(.*?)",(.*)', line)
                    if match:
                        current_category = match.group(1).strip()
                        channel_name = match.group(2).strip()
                        if current_category not in channels:
                            channels[current_category] = []
                elif line and not line.startswith("#"):
                    if current_category and channel_name:
                        channels[current_category].append((channel_name, line))
                        channel_name = ""
        else:
            for line in lines:
                line = line.strip()
                if "#genre#" in line:
                    current_category = line.split(",")[0].strip()
                    channels[current_category] = []
                elif current_category and line:
                    parts = line.split(",", 1)
                    if len(parts) == 2:
                        name, url = parts
                        channels[current_category].append((name.strip(), url.strip()))
        return channels

    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return OrderedDict()

def match_channels(template_channels, all_channels):
    matched = OrderedDict()
    for category, names in template_channels.items():
        matched[category] = OrderedDict()
        for name in names:
            primary_name = name.split("|")[0]
            for src_category, channels in all_channels.items():
                for chan_name, chan_url in channels:
                    if chan_name in name.split("|"):
                        matched[category].setdefault(primary_name, []).append(chan_url)
    return matched

def is_ipv6(url):
    return re.match(r"^http:\/\/\[[0-9a-fA-F:]+\]", url) is not None

def generate_outputs(channels, template_channels):
    written_urls = set()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    with open("lib/iptv.m3u", "w", encoding="utf-8") as m3u, \
         open("lib/iptv.txt", "w", encoding="utf-8") as txt:

        # Write channel list
        total_count = 0
        for category in template_channels:
            if category not in channels:
                continue
                
            txt.write(f"\n{category},#genre#\n")
            for name in template_channels[category]:
                primary_name = name.split("|")[0]
                urls = channels[category].get(primary_name, [])
                
                # URL filtering and sorting
                filtered = [
                    url for url in urls
                    if url and url not in written_urls
                    # and not any(b in url for b in config.url_blacklist)
                ]
                if not filtered:
                    continue

                # IP version priority sorting
                # filtered.sort(key=lambda x: is_ipv6(x) != (config.ip_version_priority == "ipv6"))
                
                # Format URLs
                total = len(filtered)
                for idx, url in enumerate(filtered, 1):
                    base_url = url.split("$")[0]
                    suffix = "$LR•" + ("IPV6" if is_ipv6(url) else "IPV4")
                    if total > 1:
                        suffix += f"•{total}『线路{idx}』"
                    final_url = f"{base_url}{suffix}"
                    
                    m3u.write(f'#EXTINF:-1 tvg-id="{idx}" tvg-name="{primary_name}" '
                             #f'tvg-logo="https://example.com/logo/{primary_name}.png" '
                             f'group-title="{category}",{primary_name}\n')
                    m3u.write(f"{final_url}\n")
                    txt.write(f"{primary_name},{final_url}\n")
                    written_urls.add(url)
                    total_count += 1

        print(f"频道处理完成，总计有效频道数：{total_count}")

def filter_sources(template_file):
    template = parse_template(template_file)
    all_channels = OrderedDict()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_channels, url): url for url in tv_urls}
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                for cat, chans in result.items():
                    all_channels.setdefault(cat, []).extend(chans)
            except Exception as e:
                print(f"处理源 {url} 时出错: {str(e)}")

    return match_channels(template, all_channels), template

if __name__ == "__main__":
    matched_channels, template = filter_sources("py/config/iptv.txt")
    generate_outputs(matched_channels, template)