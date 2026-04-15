import requests

def obter_dados():
    url = "https://www.tipminer.com/br/historico/sortenabet/aviator"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        spans = soup.find_all("span")
        valores = []

        for s in spans:
            txt = s.text.replace("x", "").strip()
            try:
                v = float(txt)
                if 1 <= v <= 100:
                    valores.append(v)
            except:
                pass

        return valores[:200]

    except Exception as e:
        print(e)
        return []
        
if not dados:
  dados = obter_dados()

if not dados:
    st.warning("⚠️ Não conseguiu pegar dados do site")
    dados = [1.2, 1.5, 2.0, 1.1, 3.2, 1.3, 2.5, 1.8, 1.4, 2.2]
