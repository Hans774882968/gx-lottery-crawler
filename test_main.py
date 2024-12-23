from article import Article
from main import get_articles_from_html
from to_different_outputs import articles_txt_content, articles_to_2d_array, \
    get_duplicate_and_unique

demo_articles = [
    Article('2024-12-12', 'http://www.lottery.gx.cn/sylm_171188/jdzx/376174.html', '奥运冠军盛李豪、黄雨婷、谢瑜走进“广西体彩大讲堂”分享夺金背后的故事'),
    Article('2024-12-10', 'http://www.lottery.gx.cn/sylm_171188/jdzx/376035.html', '在逆境中绽放，体彩点亮我的人生希望——一名特殊体彩人的自述'),
]
dup_unq_demo = [
    Article('a1', 'b1', 'c1'), Article('a2', 'b2', 'c2'), Article('a3', 'b3', 'c1'),
    Article('a4', 'b4', 'c2'), Article('a5', 'b5', 'c5'), Article('a6', 'b6', 'c1'),
]


def test_get_articles_from_html():
    html_txt = '''
    <ul class="news-list" id="pagelist">
        <!--HTMLBOX-->
        <li>
            <a href="http://www.lottery.gx.cn/sylm_171188/jdzx/376174.html">
                <span class="one-line">
                    奥运冠军盛李豪、黄雨婷、谢瑜走进“广西体彩大讲堂”分享夺金背后的故事
                </span>
                <span>
                    (
                    2024-12-12)
                </span>
            </a>
        </li>
        <li>
            <a href="http://www.lottery.gx.cn/sylm_171188/jdzx/376035.html">
                <span class="one-line">
                    在逆境中绽放，体彩点亮我的人生希望——一名特殊体彩人的自述
                </span>
                <span>
                    (
                    2024-12-10)
                </span>
            </a>
        </li>
    </ul>
    '''
    res = get_articles_from_html(html_txt)
    assert res == demo_articles


def test_articles_txt_content():
    res = articles_txt_content(demo_articles)
    assert res == '2024-12-12 http://www.lottery.gx.cn/sylm_171188/jdzx/376174.html 奥运冠军盛李豪、黄雨婷、谢瑜走进“广西体彩大讲堂”分享夺金背后的故事\n2024-12-10 http://www.lottery.gx.cn/sylm_171188/jdzx/376035.html 在逆境中绽放，体彩点亮我的人生希望——一名特殊体彩人的自述\n'


def test_articles_to_2d_array():
    res = articles_to_2d_array(demo_articles)
    assert res == [
        ['2024-12-12', 'http://www.lottery.gx.cn/sylm_171188/jdzx/376174.html', '奥运冠军盛李豪、黄雨婷、谢瑜走进“广西体彩大讲堂”分享夺金背后的故事'],
        ['2024-12-10', 'http://www.lottery.gx.cn/sylm_171188/jdzx/376035.html', '在逆境中绽放，体彩点亮我的人生希望——一名特殊体彩人的自述'],
    ]


def test_get_duplicate_and_unique():
    duplicate, unq = get_duplicate_and_unique(dup_unq_demo)
    assert duplicate == [Article('a3', 'b3', 'c1'), Article('a4', 'b4', 'c2'), Article('a6', 'b6', 'c1')]
    assert unq == [Article('a1', 'b1', 'c1'), Article('a2', 'b2', 'c2'), Article('a5', 'b5', 'c5')]
