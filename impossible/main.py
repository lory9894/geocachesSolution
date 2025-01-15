from itertools import count

import requests
from bs4 import BeautifulSoup
from enum import Enum
class Symbols(Enum):
    Picche = 0
    Cuori = 1
    Quadri = 2
    Fiori = 3
class Sides(Enum):
    North = 0
    West = 1
    East = 2
    South = 3

'''

correct_deck = {
'North': {'Picche': 'AKQJ1098765432', 'Cuori': '—', 'Quadri': '—', 'Fiori': '—'}, 'South': {'Picche': '—', 'Cuori': 'K10632', 'Quadri': 'KJ953', 'Fiori': 'A109'}, 'East': {'Picche': '—', 'Cuori': 'A9754', 'Quadri': 'AQ108762', 'Fiori': 'Q'}, 'West': {'Picche': '—', 'Cuori': 'QJ8', 'Quadri': '4', 'Fiori': 'KJ8765432'}
}
'''
correct_deck = {
'North': {'Picche': 'AKQJ1098765432', 'Cuori': '—', 'Quadri': '—', 'Fiori': '—'}, 'South': {'Picche': '—', 'Cuori': 'KQ986', 'Quadri': 'J4', 'Fiori': 'AK10876'}, 'East': {'Picche': '—', 'Cuori': 'A7542', 'Quadri': 'KQ108762', 'Fiori': 'Q'}, 'West': {'Picche': '—', 'Cuori': 'J103', 'Quadri': 'A953', 'Fiori': 'J95432'}
}
def get_page(number):
    url = f"https://bridge.thomasoandrews.com/bridge/impossible/bin/impossible.cgi?pageNumbers={number}&scramble=&bookName=Andrews&showWork="

    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve content: {response.status_code}")


def check_html(soup):

    for deal in soup.find_all('table', class_='deal'):
        deal_obj = {"pageNr" : deal.find("th").get_text(strip=True).split(" ")[1],"deck" : {'North':{}, "South":{}, "East": {}, "West": {}}}
        tables = deal.find_all('table', class_='hand')

        count = 0
        is_possible = True
        for table in tables:
                rows = table.find_all('tr')
                count2 = 0
                for row in rows:
                    columns = row.find_all('td')
                    deal_obj["deck"][Sides(count).name][Symbols(count2).name] = (columns[1].get_text(strip=True))
                    if deal_obj["deck"][Sides(count).name][Symbols(count2).name] != correct_deck[Sides(count).name][Symbols(count2).name]:
                        is_possible = False
                        break
                    count2 += 1
                if not is_possible:
                  break
                count += 1

        if deal_obj["deck"] == correct_deck:
            print(f"correct deck: {deal_obj["pageNr"]}")
            exit(1)

def read_txt(path):
    numbers = []
    with open(path, 'r') as file:
        for line in file:
            numbers.append(line.strip())
    return numbers

def process_chunk(chunk):
    html = get_page('+'.join(chunk))
    soup = BeautifulSoup(html, 'html.parser')
    check_html(soup)

if __name__ == "__main__":
    html =  """
     <body>
      <div class="back">
       Back to the
       <a href="../preface.html">
        Preface
       </a>
      </div>
      <div class="body">
       <h1>
        Pages from the Impossible Bridge Book
       </h1>
       <h2>
        (Andrews edition)
       </h2>
       <table class="deal">
        <tr>
         <th colspan="10">
          Page 491662530827348946
         </th>
        </tr>
        <tr valign="bottom">
         <td align="left" colspan="3" valign="top" width="30%">
         </td>
         <td colspan="4" width="40%">
          <table class="hand">
           <tr>
            <td>
             <font style="color:black">
              ♠
             </font>
            </td>
            <td>
             AKQJ109875432
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♥
             </font>
            </td>
            <td>
             A
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♦
             </font>
            </td>
            <td>
             —
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:black">
              ♣
             </font>
            </td>
            <td>
             —
            </td>
           </tr>
          </table>
          <td colspan="3" width="30%">
          </td>
         </td>
        </tr>
        <tr>
         <td colspan="4" width="40%">
          <table class="hand">
           <tr>
            <td>
             <font style="color:black">
              ♠
             </font>
            </td>
            <td>
             —
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♥
             </font>
            </td>
            <td>
             3
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♦
             </font>
            </td>
            <td>
             KJ1098752
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:black">
              ♣
             </font>
            </td>
            <td>
             J1093
            </td>
           </tr>
          </table>
         </td>
         <td colspan="2" width="20%">
         </td>
         <td colspan="4" width="40%">
          <table class="hand">
           <tr>
            <td>
             <font style="color:black">
              ♠
             </font>
            </td>
            <td>
             —
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♥
             </font>
            </td>
            <td>
             —
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♦
             </font>
            </td>
            <td>
             AQ643
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:black">
              ♣
             </font>
            </td>
            <td>
             AKQ87652
            </td>
           </tr>
          </table>
         </td>
        </tr>
        <tr valign="top">
         <td align="left" colspan="3" width="30%">
         </td>
         <td colspan="4" width="40%">
          <table class="hand">
           <tr>
            <td>
             <font style="color:black">
              ♠
             </font>
            </td>
            <td>
             6
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♥
             </font>
            </td>
            <td>
             KQJ109876542
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:red">
              ♦
             </font>
            </td>
            <td>
             —
            </td>
           </tr>
           <tr>
            <td>
             <font style="color:black">
              ♣
             </font>
            </td>
            <td>
             4
            </td>
           </tr>
          </table>
          <td colspan="3" width="30%">
          </td>
         </td>
        </tr>
       </table>
      </div>
      <div class="signature">
       <table>
        <tr>
         <td valign="middle">
          <a class="image" href="../../">
           <img alt="Silhouette" src="/graphics/StampSm.gif" style="border:0;width:40px;height:56px"/>
          </a>
         </td>
         <td>
          Copyright 1996-2002. Thomas Andrews
    (
          <a href="mailto:thomaso@best.com">
           thomaso@best.com
          </a>
          ) .
         </td>
        </tr>
       </table>
      </div>
     </body>
    </html>
    """
    coord_list = read_txt("readable_coords.txt")
    chunk_size = 500
    for i in range(16000, len(coord_list), chunk_size):
        chunk = coord_list[i:i + chunk_size]
        process_chunk(chunk)
        print(f"({i}/{len(coord_list)}) Done")
