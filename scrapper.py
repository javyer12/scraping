import requests
import lxml.html as html
import os
# permite crear una carpeta con la fecha actual
import datetime
# se conectara con el modulo os para agregar la gora a la carpeta

# //ejecutamos las const de xpath
TITLES = '//div[@class="row news H_img_V_Title_Lead m-0"]/div/text-fill/a/text()'
source = 'https://www.larepublica.co/economia'


def parse_notice(title, today):
    try:
        response = requests.get(title)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(TITLES)[0]
                title = title.replace('\' ', ' ')
                with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                    f.write(title)
                    f.write('\n\n')
                    for t in title:
                        f.write(t)
            except IndexError:
                return

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as err:
        print(err)


def parse_home():
    try:
        response = requests.get(source)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_news = parsed.xpath(TITLES)

            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for title in links_news:
                # print("phrase: " + title)
                parse_notice(title, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as er:
        print(er)


def run():
    parse_home()


if __name__ == '__main__':
    run()
