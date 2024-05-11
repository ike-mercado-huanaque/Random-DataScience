from riotwatcher import RiotWatcher,LolWatcher, ApiError
import pandas as pd
import numpy as np
from types import FunctionType
import time
import pymysql

#nombre invocador
user_name = 'the ghold liom  '
#region
region = 'la2'
#cola de traqueos ranked/flex/normal/aram
cola_raw = 'ranked'
# Usa tu clave de API aquí 
#ESTA API CAMBIA DIARIAMENTE, SE DEBE ACTUALIZAR
api_key = 'RGAPI-fc66b1b8-c5fc-4264-adc7-92a45f5f53cd'
#cantidad de partidas a buscar
num_partidas_input = 100

# Crea un objeto de LolWatcher
lol_watcher = LolWatcher(api_key)
riot_watcher = RiotWatcher(api_key)
# Constantes generales
NORMAL_RECL_ = 400
RANKED_SOLO_ = 420
NORMAL_BLIND_ = 430
RANKED_FLEX_ = 440
ARAM_ = 450
DICC_COLA = {'normal':NORMAL_RECL_,
'ranked':RANKED_SOLO_ ,
'blind':NORMAL_BLIND_ ,
'flex':RANKED_FLEX_,
'aram':ARAM_ }
cola = DICC_COLA[cola_raw]

#Funciones preliminares

def get_last_ranked(usuario,region=region,queue=RANKED_SOLO_):
    return lol_watcher.match.matchlist_by_puuid(region, usuario["puuid"],count=2,queue=queue)[0]
def get_last_match(usuario,region=region):
    return lol_watcher.match.matchlist_by_puuid(region, usuario["puuid"],count=2)[0]
def get_previous_matches(summoner_puuid, region, match_id,queue=None,count=10):
    try:
        #ARREGLAR ESTA LINEA PARA QUE BUSQUE EL MATCHID
        previous_matches = []
        found_match = False
        idx_init=0
        search = min([count+20,100])
        keep = True
        while (not found_match) or keep:
            matchlist = lol_watcher.match.matchlist_by_puuid(region, summoner_puuid,count = search,start=idx_init,queue=queue)
            if len(matchlist) == 0:
                break
            elif keep:
                for match in matchlist:
                    if match == match_id:
                        found_match = True
                    elif found_match:
                        previous_matches.append(match)
                        if len(previous_matches) >= count:
                            keep = False
                            break
                idx_init += search
            
        return previous_matches
    except ApiError as err:
        print(f"Error retrieving previous matches: {err}")
        return None
def get_match_stats(matchid,region,include_teams = False):
    if isinstance(matchid,str):
        matchid = [matchid]
    elif isinstance(matchid,list):
        pass
    else:
        raise TypeError("Solo formato string o list son permitidos.")
    matches_dict = dict()
    i = 0
    for m_id in matchid:
        if len(matchid) > 100 and (i+1)%50 == 0:
            print(f"Obteniedo estadisticas para {i+1} partidas\n")
        elif len(matchid) <= 100 and i%10 == 0:
            print(f"Obteniedo estadisticas para {i+1} partidas\n")
        #print información
        #print(f"Obteniedo estadisticas de la partida {m_id}\n")
        matches_dict[m_id] = lol_watcher.match.by_id(region, m_id)['info']['participants']
        if include_teams:
            print("incluyendo información de teams\n")
            matches_dict[m_id].append(lol_watcher.match.by_id(region, m_id)['info']['teams'])
        i += 1
    return matches_dict

class playerData(object):
    def F00_match_stats(self):
        self.match_stats = get_match_stats(self._LMlist,region,include_teams=False) 
    def F01_dataframe(self):
        df_list = list()
        for mid,lista in self.match_stats.items():
            for dicc in lista:
                df = pd.DataFrame({x:[y] for x,y in dicc.items() if x not in ['challenges','missions','perks']})
                df['idpartida'] = mid
                df_list.append(df)
        print('Consolidando DataFrame...\n')
        df = pd.concat(df_list).reset_index(drop=True)
        cols = [x for x in df.columns if x not in ['riotIdGameName','idpartida']]
        cols = ['idpartida','riotIdGameName'] + cols
        self.dataframe = df[cols]
        print('DataFrame generado.\n')
    def F02_createTable(self):
        dicc_dtype2sql = {np.dtype('int64'):'INT',
                        np.dtype('float64'):'FLOAT',
                        np.dtype('O'):'VARCHAR(30)',
                        np.dtype('bool'):'BOOL'}
        schema = [x + ' ' + dicc_dtype2sql[y] + ' NOT NULL' for x,y in self.dataframe.dtypes.items() if x in ('riotIdGameName','idpartida')] +\
        [x + ' ' + dicc_dtype2sql[y] for x,y in self.dataframe.dtypes.items() if x not in ('riotIdGameName','idpartida')]              
        schema = ', '.join(['id INT AUTO_INCREMENT PRIMARY KEY']+schema)
        self.altercols = {'add':['riotIdGameName','summonerId','puuid'],
                          'encoding':['riotIdTagline']}
        self.schema = schema
        query_create = f"CREATE TABLE IF NOT EXISTS partidas ({schema});"
        conn = pymysql.connect(host="localhost",user="root",passwd="12345",db="lol")
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(query_create)
                conn.commit()
    def F03_alterTable(self):
        querys = [f"ALTER TABLE partidas MODIFY {q} VARCHAR(100)"\
                     for x,y in self.altercols.items() if x == 'add' for q in y]
        querys += [f"ALTER TABLE partidas MODIFY COLUMN {q} VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;"\
                     for x,y in self.altercols.items() if x == 'encoding' for q in y]
        conn = pymysql.connect(host="localhost",user="root",passwd="12345",db="lol")
        with conn:
            with conn.cursor() as cursor:
                for qu in querys:
                    cursor.execute(qu)
                    conn.commit()
    def F04_uploadSQL(self):
        ssf2 = (len(self.dataframe.columns.tolist())-1)*'%s,' + '%s'
        ssf1 = ','.join(self.dataframe.columns.tolist())
        datos = [tuple(x) for x in self.dataframe.values]
        insert_query = f"INSERT INTO partidas ({ssf1}) VALUES ({ssf2});"
        conn = pymysql.connect(host="localhost",user="root",passwd="12345",db="lol")
        with conn:
            with conn.cursor() as cursor:
                cursor.executemany(insert_query,datos)
                conn.commit()
    def __run__(self):
        for x in dir(self):
            if 'F00' in x and self._nummatch > 100: 
                print('Esperando 30 seg para requests de api...\n')
                time.sleep(30)   
            if x.startswith('F'):
                print(x)
                getattr(self,x)()                             
    def __init__(self,user_name,region):
        self._nummatch = num_partidas_input
        self._puuid = riot_watcher.account.by_riot_id(region='AMERICAS',game_name=user_name,tag_line='LAS')['puuid']
        self._usuario = lol_watcher.summoner.by_puuid(region, self._puuid)
        self._LMseed = get_last_ranked(self._usuario,region=region)
        self._LMlist = get_previous_matches(self._puuid, region=region,match_id=self._LMseed,queue=RANKED_SOLO_,count=self._nummatch)

