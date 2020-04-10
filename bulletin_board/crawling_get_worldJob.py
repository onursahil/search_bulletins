import requests as req
from bs4  import BeautifulSoup 
import datetime

'''
pip install requests // http 요청 모듈
pip install beautifulsoup4   // html 태그 파싱용 모듈(bs4)
pip install lxml  // bs4 보조 모듈(필수요소는 아니지만, 사용 시 더 빠른 파싱 가능)
'''

class BWU_worldJob():
  def __init__(self):
    pass
  
  def get_notice(self, keyword, count):
    print('crwal start:', keyword, count)

    base_url = 'http://www.worldjob.or.kr/'
    searched_url = base_url +\
      'info/bbs/notice/list.do?tabCheck=1&srchType=&menuId=1000000049&srchTxt='+keyword

    try:
      res = req.get(searched_url)
      # lxml을 설치하지 않았다면 soup = BeautifulSoup(res.text, 'html.parser')
      soup = BeautifulSoup(res.text, 'lxml')
    except Exception as e:
      print(e)
      return []

    json_form = []
    text_form = ''

    dl_list = soup.select('dl.post-article')
    
    
    for dl in dl_list[:]:
      # if type(tr_tag.get('class')) != type(None) :
      #   continue
      # td_tags = dl.select('span')

      a_tag = dl.select('a')

      if dl.select('span.t_notice'):
        row_num = dl.select('span.t_notice')[0].text.strip()
      elif dl.select('p.t_number'):
        row_num = dl.select('p.t_number')[0].text.strip()

      row_title = dl.select('h2.ellipsis')[0].text.strip()
      row_link = base_url + a_tag[0].get('href')
      # row_writer = td_tags[2].text.strip()
      row_date = dl.select('dd.post-arrow-right > span')[0].text.strip()
      row_date = row_date.replace("-", ".")
      row_read = dl.select('dd.post-arrow-right > span')[1].text.strip()
      row_file = False
      if dl.select('i.fa-paperclip'):
        row_file = True
      
      
      # if len(td_tags[5].select('img')):
      #   row_file = True

      todays_date = datetime.datetime.now().strftime('%Y.%m.%d')
      row = {
          'post_date': row_date,
          'crawled_date': todays_date,
          'title': row_title,
          'link': row_link,
        }
      json_form.append(row)

      # now = datetime.now()
      # today = str(now)[:10]

      # # JSON 형식으로 저장할때
      # if row_date == today:
      #   row = {
      #     'post_date': row_date,
      #     'crawled_date': datetime.datetime.now().strftime('%Y.%m.%d'),
      #     'title': row_title,
      #     'link': row_link,
      #   }
      #   json_form.append(row)

      # 텍스트형식으로 보여줄때
      text_form += "번호: {number}, 제목: {title}, 링크: {link}, "\
                  ", 작성일: {date}, 조회수: {read}, 파일유무: {is_file}"\
                  .format(number=row_num, title=row_title, link=row_link, 
                  date=row_date, read=row_read, is_file=row_file)
      text_form += '\n'

      if len(json_form) > count-1:
        break

    if text_form and not text_form.isspace():
      # print(text_form)
      pass
    else:
      print('신규 게시물이 없습니다.')
    return json_form
    
if __name__ == '__main__':
    b = BWU()
    keywords = ['해외취업', '골목식당']
    count = 5
    for keyword in keywords:
      b.get_notice(keyword, count)
      # print(b.get_notice(keyword, count))
    
