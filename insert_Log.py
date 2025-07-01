import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from sqlalchemy import create_engine, text
from tqdm import tqdm

DB_CONFIG = {
    'host': "",
    'user': "",
    'password': "",
    'database': "",
    'port': 
}

def conectar_banco():
    engine = create_engine(
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}",
        pool_pre_ping=True,
        connect_args={'connect_timeout': 10}
    )
    return engine

def abrir_site():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.google.com/maps")
    print("✅ Google Maps aberto com sucesso!")
    return driver

def pesquisar_cep(driver, cep):
    try:
        wait = WebDriverWait(driver, 20)
        campo_pesquisa = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#searchboxinput")))
        campo_pesquisa.clear()
        campo_pesquisa.send_keys(cep)
        campo_pesquisa.send_keys(Keys.ENTER)
        print(f"🔍 Buscando CEP: {cep}")
        time.sleep(8)
    except Exception as e:
        print(f"❌ Erro ao buscar o CEP {cep}: {e}")

def clicar_direito_e_capturar_lat_long(driver):
    try:
        time.sleep(2)
        mapa = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "widget-scene"))
        )
        ActionChains(driver).move_to_element_with_offset(mapa, 500, 300).context_click().perform()
        time.sleep(2)
        coordenada = driver.find_element(By.CLASS_NAME, "mLuXec").text.strip()
        print(f"📍 Coordenadas capturadas: {coordenada}")
        return coordenada
    except Exception as e:
        print(f"❌ Erro ao capturar coordenadas: {e}")
        return None

def atualizar_coordenadas_no_banco(engine, cep, coordenadas):
    try:
        if not coordenadas:
            return False
        with engine.begin() as conn:
            update_query = text("""
                UPDATE dados_gov 
                SET LAG_LOG = :coordenadas 
                WHERE CEP = :cep
            """)
            result = conn.execute(update_query, {"coordenadas": coordenadas, "cep": cep})
            print(f"📝 CEP {cep} atualizado com {coordenadas} ({result.rowcount} linha(s) afetada(s))")
            return result.rowcount > 0
    except Exception as e:
        print(f"❌ Erro ao atualizar CEP {cep}: {e}")
        return False

def formatar_cep(cep):
    # Remove zeros à esquerda, igual ao banco
    return str(int(''.join(filter(str.isdigit, str(cep)))))

def main():
    engine = conectar_banco()
    print("🔍 Buscando CEPs com LAG_LOG NULL no banco...")

    query = text("""
        SELECT DISTINCT CEP 
        FROM dados_gov 
        WHERE LAG_LOG IS NULL
        AND CEP IS NOT NULL
        AND TRIM(CEP) != ''
        LIMIT 10
    """)

    df_ceps = pd.read_sql(query, engine)
    ceps = df_ceps['CEP'].unique().tolist()

    if not ceps:
        print("✅ Todos os CEPs já possuem geocodificação!")
        return

    print(f"📊 Total de CEPs a processar: {len(ceps)}")
    driver = abrir_site()
    time.sleep(5)

    try:
        for cep in tqdm(ceps, desc="Processando CEPs"):
            cep_formatado = formatar_cep(cep)
            print(f"\n🔄 Processando CEP: {cep_formatado}")

            pesquisar_cep(driver, cep_formatado)
            coordenadas = clicar_direito_e_capturar_lat_long(driver)

            if coordenadas:
                if atualizar_coordenadas_no_banco(engine, cep_formatado, coordenadas):
                    print(f"✓ CEP {cep_formatado} atualizado com sucesso!")
                else:
                    print(f"⚠️ CEP {cep_formatado} não foi atualizado (pode já ter sido processado)")
            else:
                print(f"❌ Falha ao geocodificar CEP {cep_formatado}")

            time.sleep(random.uniform(3, 7))  # Pausa aleatória

    finally:
        driver.quit()
        print("✅ Processo finalizado!")

        # Verifica quantos registros foram atualizados
        with engine.connect() as conn:
            res = conn.execute(text("SELECT COUNT(*) FROM dados_gov WHERE LAG_LOG IS NOT NULL"))
            total = res.scalar()
            print(f"📊 Total de registros geocodificados: {total}")

if __name__ == "__main__":
    main()
