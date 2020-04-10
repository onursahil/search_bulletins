import requests as req
from bs4  import BeautifulSoup
import datetime

'''
pip install requests // http 요청 모듈
pip install beautifulsoup4   // html 태그 파싱용 모듈(bs4)
pip install lxml  // bs4 보조 모듈(필수요소는 아니지만, 사용 시 더 빠른 파싱 가능)
'''

class BWU_kosaf():
  def __init__(self):
    pass
  
  def get_notice(self, keyword, count):
    print('crwal start:', keyword, count)

    base_url = 'http://www.kosaf.go.kr/ko/notice.do'
    searched_url = base_url + '?searchType=s&searchStr=' + keyword
    try:
      res = req.get(searched_url)
      # lxml을 설치하지 않았다면 soup = BeautifulSoup(res.text, 'html.parser')
      soup = BeautifulSoup(res.text, 'lxml')
    except Exception as e:
      print(e)
      return []

    json_form = []
    text_form = ''

    table_tag = soup.select('table:nth-of-type(1) tr')
    
    
    for tr_tag in table_tag[1:]:

      if type(tr_tag.get('class')) != type(None) :
        continue
      td_tags = tr_tag.select('td')
      if len(td_tags) == 0:
        print("검색결과가 없습니다")
        break
      a_tag = td_tags[1].select('a')

      row_num = td_tags[0].text.strip()
      row_title = a_tag[0].text.strip()
      row_link = base_url + a_tag[0].get('href')
      # row_writer = td_tags[2].text.strip()
      row_date = td_tags[2].text.strip()
      row_date = row_date.replace("-", ".")
      row_read = td_tags[3].text.strip()
      # row_file = False
      # if len(td_tags[5].select('img')):
      #   row_file = True

      # JSON 형식으로 저장할때
      todays_date = datetime.datetime.now().strftime('%Y.%m.%d')
      row = {
          'post_date': row_date,
          'crawled_date': todays_date,
          'title': row_title,
          'link': row_link,
      }
      json_form.append(row)

      # 텍스트형식으로 보여줄때
      text_form += "번호: {number}, 제목: {title}, 링크: {link}, "\
                  ", 작성일: {date}, 조회수: {read}"\
                  .format(number=row_num, title=row_title, link=row_link, 
                  date=row_date, read=row_read) # , is_file=row_file)

      if len(json_form) > count-1:
        break
      text_form += '\n'

    # print(text_form)
    return json_form
    
if __name__ == '__main__':
    b = BWU()
    keywords = ['골목식당', '학자금']
    count = 5
    for keyword in keywords:
      b.get_notice(keyword, count)
      # print(b.get_notice(keyword, count))
    