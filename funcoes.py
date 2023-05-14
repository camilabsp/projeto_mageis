from tkinter import *
from datetime import *
from tkinter import messagebox
import sqlite3 

class funcoes:
    def __init__(self,data,ativo,qtd,valor_unit,c_v,taxa_corret=5.00):
        self.data = data    
        self.ativo = ativo
        self.qtd = qtd
        self.valor_unit = valor_unit
        self.c_v = c_v
        self.taxa_corret = taxa_corret

    def limpar_tela(self):
        self.data_entry.delete(0,END)
        self.ativo_entry.delete(0,END)
        self.qtd_entry.delete(0,END)
        self.valor_unit_entry.delete(0,END)

    def conecta_bd(self):
        self.conn = sqlite3.connect('dado.bd')
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def cria_bd(self):
        self.conecta_bd()
        ##criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dado(
                data TEXT,
                ativo TEXT,
                qtd TEXT,
                valor_unit TEXT,
                c_v TEXT,
                valor_operacao REAL,
                tx_corret REAL,
                tx_b3 REAL,
                valor_total REAL,
                preco_medio REAL
                
            );
        """)

        self.conn.commit();print('banco de dados criado')
        self.desconecta_bd

    def adiciona_dados(self):

        try:
            self.data = str(self.data_entry.get())
            self.ativo = self.ativo_entry.get().upper()
            self.qtd = int(self.qtd_entry.get())
            self.valor_unit = float(self.valor_unit_entry.get())
            self.c_v = self.radio_valor.get()
        
            self.valor_operacao = round((self.qtd * self.valor_unit),2)
            self.tx_corret = 5.00
            self.tx_b3 = round((0.0003 * self.valor_operacao),2)

            if self.c_v == 1:
                self.c_v = 'C'
                self.valor_total = round((self.valor_operacao + self.tx_corret + self.tx_b3),2)
            elif self.c_v == 2:
                self.c_v = 'V'
                self.valor_total = round((self.valor_operacao - self.tx_corret - self.tx_b3),2)


            self.preco_medio = self.valor_total/self.qtd #verificar o cálculo de preço médio
                
            self.conecta_bd()

            self.cursor.execute("""INSERT INTO dado(data,ativo,qtd,valor_unit,c_v,valor_operacao,tx_corret,tx_b3,valor_total,preco_medio)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",(self.data,self.ativo,self.qtd,self.valor_unit,self.c_v,self.valor_operacao,self.tx_corret,self.tx_b3,self.valor_total,self.preco_medio)) 

            self.conn.commit()
            self.desconecta_bd()
            self.atualiza_tabela()
            self.limpar_tela()

        except:
            msg = 'Todos os campos devem ser preenchidos'
            messagebox.showinfo('Otimizador de Investimentos',msg)

    def atualiza_tabela(self):
        self.tabela_dados.delete(*self.tabela_dados.get_children())
        self.conecta_bd()
        l = self.cursor.execute(""" SELECT data,ativo,qtd,valor_unit,c_v,valor_operacao,tx_corret,tx_b3,valor_total,preco_medio
            FROM dado ORDER BY data ASC""")
        for i in l:
            self.tabela_dados.insert("",END,values=i)

        self.desconecta_bd()
    
    def buscar_ativo(self):
        self.conecta_bd()
        self.tabela_dados.delete(*self.tabela_dados.get_children()) 

        self.filtrar_ativo_entry.insert(END,"%")
        filtrar_ativo = self.filtrar_ativo_entry.get()
        self.cursor.execute(
            """SELECT data,ativo,qtd,valor_unit,c_v,valor_operacao,tx_corret,tx_b3,valor_total,preco_medio FROM dado WHERE ativo LIKE '%s' ORDER BY data ASC""" % filtrar_ativo)
        buscacodigo = self.cursor.fetchall()
        for i in buscacodigo:
            self.tabela_dados.insert("",END,values=i)
        self.limpar_tela()
        self.desconecta_bd()

    def excluir_registro(self):
        
        selecao = self.tabela_dados.focus() # Obtem o item selecionado na Tabela de dados
        
        if selecao:
            
            valores = self.tabela_dados.item(selecao)['values'] # valores dos itens selecionados
            registro = valores[0]  

            self.conecta_bd()

            self.cursor.execute("DELETE FROM dado WHERE data = ?", (registro,))
            self.conn.commit()

            self.desconecta_bd()

            self.tabela_dados.delete(selecao)

            self.limpar_tela()
            self.atualiza_tabela() # Atualiza tabela

