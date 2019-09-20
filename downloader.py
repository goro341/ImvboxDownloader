import requests, os
from env import OUTPUT_PATH

def get_links(film_spec, segments):
    links = []
    for i in range(segments + 1):
        links.append(get_url_for_segment(film_spec, i))
    return links


def get_url_for_segment(film_spec, segment_number):
    segment_number_string = str(segment_number)
    while 5 - len(segment_number_string):
        segment_number_string = '0' + segment_number_string
    return 'https://streaming.imvbox.com/%s/segment%s.ts' % (film_spec, segment_number_string)


def download_link(url):
    r = requests.get(url)
    file_name = url.split("/")[-1]
    file_path = os.path.join(OUTPUT_PATH, file_name)
    with open(file_path, 'wb') as f:
        f.write(r.content)


def find_num_segments(film_spec):
    film_spec = film_spec + '/' + film_spec.split("/")[-1]
    url = 'https://streaming.imvbox.com/%s.m3u8' % film_spec
    r = requests.get(url)
    segments = list(filter(lambda x : 'segment' in str(x), r.content.splitlines()))
    return len(segments)
