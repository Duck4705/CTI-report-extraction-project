import trafilatura
import re
def fetch_and_extract(url):
	downloaded = trafilatura.fetch_url(url)
	text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
	return text

def clean_text(text):
	if text:
		# Loại bỏ xuống dòng, tab, gạch đầu dòng ở đầu dòng
		text = re.sub(r"[\n\r\t]+", " ", text)
		# Loại bỏ gạch đầu dòng ở đầu dòng hoặc giữa dòng
		text = re.sub(r"\s*-\s*", " ", text)
		# Loại bỏ nhiều khoảng trắng liên tiếp
		text = re.sub(r"\s+", " ", text)
		# Đảm bảo chỉ có dấu chấm để phân cách câu
		text = re.sub(r"\.+", ".", text)
		# Loại bỏ dấu chấm ở đầu/cuối nếu có
		text = text.strip(" .")
		# Thêm dấu chấm cuối nếu thiếu
		if not text.endswith('.'):
			text += '.'
		return text
	return ""

def crawl_url(url):
    content = fetch_and_extract(url)
    clean_text_content = clean_text(content)
    return clean_text_content