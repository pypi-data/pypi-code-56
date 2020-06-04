from robotstxt.processor import *


test_robots = '''
# some more comments
some uncommented comments

user-agent: bingbot
user-agent: googlebot
Disallow: /case_insensitive_token
Disallow: *url_query_test
Disallow: /multiple_token_block
Allow: /same_length_allow_beats_disallow
Disallow: /same_length_allow_beats_disallow
Allow: /longer_allow_beats_disallow*
Disallow: /longer_allow_beats_disallow
Disallow: /inline_comment # inline comment
Disallow: missing_leading_slash
Disallow: *leading_wildcard
Disallow: /multiple*wildcards*test
Disallow: *unencoded|
Disallow: *encoded%40 # @ symbol
Disallow: /positive_fallback_test
Disallow: /default_trailing_wildcard

Disallow: /block_break

user-agent: googlebot
Disallow: /split_block_test

user-agent: googlebot-images
Disallow: /negative_fallback_test

user-agent: *
Disallow: /default_token

user-agent: blank
Disallow:

Sitemap: https://www.domain.com/sitemap.xml
sitemap: https://www.domain.com/lower_case.xml
SITEMAP: https://www.domain.com/upper_case.xml
sitemap: www.domain.com/missing_protocol.xml
sitemap: missing_domain.xml
sitemap: https://www.domain.com/has_comment.xml #comment
  Sitemap: https://www.domain.com/leading_whitespace.xml
Sitemap: https://www.domain.com/trailing_whitespace.xml   
Sitemap:    https://www.domain.com/rule_leading_whitespace.xml   

'''


def test_RobotsFile():
    robots = RobotsFile(test_robots)
    robots_size_exceeded = RobotsFile('x' * 900000)

    #assert robots.byte_size == 652 #todo uncomment this when tests finalized
    assert robots.size_exceeded == False
    assert robots_size_exceeded.size_exceeded == True

    assert robots.sitemaps[0].url == 'https://www.domain.com/sitemap.xml'
    assert robots.sitemaps[1].url == 'https://www.domain.com/lower_case.xml'
    assert robots.sitemaps[2].url == 'https://www.domain.com/upper_case.xml'
    assert robots.sitemaps[3].url == 'www.domain.com/missing_protocol.xml'
    assert robots.sitemaps[4].url == 'missing_domain.xml'
    assert robots.sitemaps[5].url == 'https://www.domain.com/has_comment.xml'
    assert robots.sitemaps[6].url == 'https://www.domain.com/leading_whitespace.xml'
    assert robots.sitemaps[7].url == 'https://www.domain.com/trailing_whitespace.xml'
    assert robots.sitemaps[8].url == 'https://www.domain.com/rule_leading_whitespace.xml'

    assert robots.sitemaps[0].valid_url == True
    assert robots.sitemaps[3].valid_url == False
    assert robots.sitemaps[4].valid_url == False

    assert robots.test_url('http://test.chris24.co.uk/case_insensitive_token', 'GOOGLEBOT')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/split_block_test', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/multiple_token_block', 'bingbot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/default_token', 'some_token')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/inline_comment', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/?url_query_test=123', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/missing_leading_slash', 'googlebot')['disallowed'] == False
    assert robots.test_url('http://test.chris24.co.uk/negative_fallback_test', 'googlebot-images')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/same_length_allow_beats_disallow', 'googlebot')[
               'disallowed'] == False
    assert robots.test_url('http://test.chris24.co.uk/longer_allow_beats_disallow', 'googlebot')['disallowed'] == False
    assert robots.test_url('http://test.chris24.co.uk/block_break', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/positive_fallback_test', 'googlebot-news')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/leading_wildcard', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/multiple_wildcards_test_', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/default_trailing_wildcard_test', 'googlebot')[
               'disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/encoded%40', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/encoded@', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/unencoded%7C', 'googlebot')['disallowed'] == True
    assert robots.test_url('http://test.chris24.co.uk/blank_disallow', 'blank')['disallowed'] == False


def test_Sitemap():
    sitemap_result = Sitemap('https://www.example.com/sitemap.xml')
    assert sitemap_result.valid_url == True
    assert sitemap_result.url == 'https://www.example.com/sitemap.xml'

    sitemap_result = Sitemap('ttps://www.example.com/sitemap.xml')
    assert sitemap_result.valid_url == False

print('something')