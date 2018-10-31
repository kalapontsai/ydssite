# ateconfig_default.py

configs = {
    'db': {
        'driver': '{ODBC Driver 17 for SQL Server}',
        'host': '192.168.1.4',
        'user': 'sa',
        'password': 'yds6f',
        'database': 'ate'
    },
#不包含程式自動產生的 [Dc-DcTestDataRecode]目錄
    'catch':{
        'root_path':'V:\\z_rd_qc_mk\\ATE_01\\'
    },

    'export': {
        'save_to': 'V:\\z_rd_qc_mk\\ATE_01\\spcc',
        'template': 'V:\\z_rd_qc_mk\ATE_01\\spcc\\template-XR.xlsx'
    }
}