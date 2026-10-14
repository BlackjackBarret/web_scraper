import unittest
from crawl import extract_page_data, get_first_paragraph_from_html, get_heading_from_html, get_images_from_html, get_urls_from_html, normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_query_params(self):
        input_url = "https://www.boot.dev/blog/path?query=param"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_fragment(self):
        input_url = "https://www.boot.dev/blog/path#fragment"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_no_scheme(self):
        input_url = "www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_only_domain(self):
        input_url = "https://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_root_slash(self):
        input_url = "https://www.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_case_insensitivity(self):
        input_url = "https://WWW.Boot.Dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html(self):
        html = "<h1>Hello, World!</h1>"
        actual = get_heading_from_html(html)
        expected = "Hello, World!"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_no_h1(self):
        html = "<p>No heading here</p>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_multiple_h1(self):
        html = "<h1>First Heading</h1><h1>Second Heading</h1>"
        actual = get_heading_from_html(html)
        expected = "First Heading"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_nested_h1(self):
        html = "<div><h1>Nested Heading</h1></div>"
        actual = get_heading_from_html(html)
        expected = "Nested Heading"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_empty_h1(self):
        html = "<h1></h1>"
        actual = get_heading_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_h1_and_other_tags(self):
        html = "<h1>Heading</h1><p>Paragraph</p>"
        actual = get_heading_from_html(html)
        expected = "Heading"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_h1_and_attributes(self):
        html = '<h1 class="title">Heading with Class</h1>'
        actual = get_heading_from_html(html)
        expected = "Heading with Class"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_h1_and_special_characters(self):
        html = "<h1>Heading &amp; Special Characters</h1>"
        actual = get_heading_from_html(html)
        expected = "Heading & Special Characters"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_h1_and_whitespace(self):
        html = "<h1>   Heading with Whitespace   </h1>"
        actual = get_heading_from_html(html)
        expected = "   Heading with Whitespace   "
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_h1_and_nested_tags(self):
        html = "<h1>Heading with <span>Nested</span> Tags</h1>"
        actual = get_heading_from_html(html)
        expected = "Heading with Nested Tags"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_h1_and_line_breaks(self):   
        html = "<h1>Heading with<br>Line Breaks</h1>"
        actual = get_heading_from_html(html)
        expected = "Heading withLine Breaks"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html(self):
        html = "<p>This is the first paragraph.</p>"
        actual = get_first_paragraph_from_html(html)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_with_no_p(self):
        html = "<h1>No paragraph here</h1>"
        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><p>No links here</p></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_with_fragment(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com#section"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com#section"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_with_query_params(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com?query=param"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com?query=param"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_with_relative_and_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a><a href="/about"><span>About</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com", "https://crawler-test.com/about"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_with_empty_href(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href=""><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/image.jpg" alt="Image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/image1.jpg" alt="Image 1"><img src="/image2.jpg" alt="Image 2"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image1.jpg", "https://crawler-test.com/image2.jpg"]
        self.assertEqual(actual, expected)  

    def test_get_images_from_html_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><p>No images here</p></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_with_empty_src(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="" alt="Image"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_heading(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_paragraph(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_links(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_empty_html(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()