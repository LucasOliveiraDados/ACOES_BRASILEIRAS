import yfinance as yf
from datetime import datetime, timedelta

def obter_dados_acoes(tickers, dias=30):
    fim = datetime.today()
    inicio = fim - timedelta(days=dias)
    dados = yf.download(tickers, start=inicio, end=fim, group_by='ticker', progress=False)
    registros = []

    for ticker in tickers:
        if ticker not in dados:
            continue
        df = dados[ticker].copy()
        df = df[~df.index.duplicated(keep='first')]
        df = df.dropna(subset=['Close'])

        for data, linha in df.iterrows():
            registros.append({
                'ticker': ticker,
                'data': data.date(),
                'open': round(float(linha['Open']), 2),
                'high': round(float(linha['High']), 2),
                'low': round(float(linha['Low']), 2),
                'close': round(float(linha['Close']), 2),
                'volume': int(linha['Volume'])
            })

    return registros

if __name__ == "__main__":
    with open("tickers_validos.txt", "r") as f:
        tickers = [linha.strip() for linha in f if linha.strip()]

    dados = obter_dados_acoes(tickers)
    print(f"{len(dados)} registros extraídos.")
