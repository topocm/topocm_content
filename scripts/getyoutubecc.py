# This code is adapted from https://github.com/ihinojal/getyoutubecc

import urllib.request, urllib.error, urllib.parse
from xml.etree import ElementTree as ET
import json
from codecs import open

def get_cc(video_id, lang="en", track="", tlang="" ):
    """Get closed captions from YouTube and parse the XML."""
    cc_url = ("http://youtube.com/api/timedtext?v=" + video_id + "&lang=" +
              lang + "&name=" + track + "&tlang=" + tlang)

    xml_source = urllib.request.urlopen(cc_url).read()
    if not len(xml_source):
        raise RuntimeError("No CC available")

    utf8_parser = ET.XMLParser(encoding='utf-8')
    return ET.fromstring(xml_source, parser=utf8_parser)


def xml2sjson(cc):
    """Translate a single language YouTube XML to EdX sjson."""
    entries = cc.getchildren()
    entries = [(float(i.attrib['start']), float(i.attrib['dur']),
                i.text.replace('\n', ' ')) for i in entries]
    entries = [(int(i * 1e3), int((i + j) * 1e3), k) for (i, j, k) in entries]
    result = {'start': [i[0] for i in entries],
              'end': [i[1] for i in entries],
              'text': [i[2] for i in entries]}
    return result


def write_sjson(sjson, filename):
    with open(filename, 'w', 'utf-8') as f:
        json.dump(sjson, f)


def save_youtube_cc(video_id, filename):
    feed = get_cc(video_id)
    sjson = xml2sjson(feed)
    write_sjson(sjson, filename)
