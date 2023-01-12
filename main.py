from PyQt5 import uic, QtWidgets, Qt, QtGui
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from datetime import date
import bcrypt


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="empresa"
)

cursor = db.cursor()
db.commit()
id_conta = -1


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(password, hashed):
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed)


def ordenar_valor():
    # Ordenando contas por valor total
    cursor.execute(
        "SELECT id_conta, SUM(valor_total) as total FROM pedido GROUP BY id_conta ORDER BY total DESC;")
    contas = cursor.fetchall()
    # print(contas)
    # Formatando tabela
    window_relatorio.usuarios.setRowCount(len(contas))
    # Alterando header da tabela
    window_relatorio.usuarios.setHorizontalHeaderLabels(
        ["ID", "Nome", "Total"])
    # Atualizando label que mostra total de usuários
    window_relatorio.total.setText(f"Total: {len(contas)} contas")
    for id_conta, total in contas:
        # Obtendo nome do cliente
        cursor.execute(
            "SELECT nome FROM cliente WHERE id = (SELECT id_cliente FROM conta WHERE id = %s);", (id_conta,))
        nome = cursor.fetchone()
        nome = nome[0]
        print(nome)

        # Inserindo dados
        window_relatorio.usuarios.setItem(contas.index(
            (id_conta, total)), 0, QtWidgets.QTableWidgetItem(str(id_conta)))
        window_relatorio.usuarios.setItem(contas.index(
            (id_conta, total)), 1, QtWidgets.QTableWidgetItem(nome))
        window_relatorio.usuarios.setItem(contas.index(
            (id_conta, total)), 2, QtWidgets.QTableWidgetItem(str(total)))

    header = window_relatorio.usuarios.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    window_filter.close()


def ordenar_pedidos():
    # Ordenando contas por quantidade de pedidos
    cursor.execute(
        "SELECT id_conta, COUNT(id) as num_pedidos FROM pedido GROUP BY id_conta ORDER BY num_pedidos DESC;")
    contas = cursor.fetchall()
    # print(contas)
    # Formatando tabela
    window_relatorio.usuarios.setHorizontalHeaderLabels(
        ["ID", "Nome", "Pedidos"])
    window_relatorio.usuarios.setRowCount(len(contas))
    # Atualizando label que mostra total de usuários
    window_relatorio.total.setText(f"Total: {len(contas)} contas")
    for id_conta, num_pedidos in contas:
        # Obtendo nome do cliente
        cursor.execute(
            "SELECT nome FROM cliente WHERE id = (SELECT id_cliente FROM conta WHERE id = %s);", (id_conta,))
        nome = cursor.fetchone()
        nome = nome[0]
        print(nome)

        # Inserindo dados
        window_relatorio.usuarios.setItem(contas.index(
            (id_conta, num_pedidos)), 0, QtWidgets.QTableWidgetItem(str(id_conta)))
        window_relatorio.usuarios.setItem(contas.index(
            (id_conta, num_pedidos)), 1, QtWidgets.QTableWidgetItem(nome))
        window_relatorio.usuarios.setItem(contas.index(
            (id_conta, num_pedidos)), 2, QtWidgets.QTableWidgetItem(str(num_pedidos)))

    header = window_relatorio.usuarios.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    window_filter.close()


def filtro():
    # Verificando se algum filtro de localização foi selecionado
    local = ""
    if window_filter.estado.isChecked():
        tipo = "estado"
        local = window_filter.local.text()
        if not local and not window_filter.ano.text():
            QMessageBox.warning(window_filter, "Erro",
                                "Nenhum local inserido!")
            return
    elif window_filter.cidade.isChecked():
        tipo = "cidade"
        local = window_filter.local.text()
        if not local and not window_filter.ano.text():
            QMessageBox.warning(window_filter, "Erro",
                                "Nenhum local inserido!")
            return
    elif window_filter.bairro.isChecked():
        tipo = "bairro"
        local = window_filter.local.text()
        if not local and not window_filter.ano.text():
            QMessageBox.warning(window_filter, "Erro",
                                "Nenhum local inserido!")
            return
    if local:
        local = local.title()
        cursor.execute(
            "SELECT id, nome from cliente where {} = '{}';".format(tipo, local))
        clientes = cursor.fetchall()
        if clientes:
            # Formatando tabela de usuários
            window_relatorio.usuarios.setRowCount(len(clientes))
            # Atualizando label que mostra total de usuários
            window_relatorio.total.setText(
                f"Total: {len(clientes)} em {local}")

            # Para cada cliente, obtendo seu id de conta
            for id, nome in clientes:
                cursor.execute(
                    "SELECT id from conta WHERE id_cliente = %s;", (id,))
                conta = cursor.fetchone()
                conta = conta[0]

                # Obtendo quantidade de pedidos
                cursor.execute(
                    "SELECT COUNT(id) FROM pedido WHERE id_conta = %s;", (conta,))
                num_pedidos = cursor.fetchone()
                num_pedidos = num_pedidos[0]

                # Organizando tabela
                window_relatorio.usuarios.setItem(clientes.index(
                    (id, nome)), 0, QtWidgets.QTableWidgetItem(str(conta)))
                window_relatorio.usuarios.setItem(clientes.index(
                    (id, nome)), 1, QtWidgets.QTableWidgetItem(nome))
                window_relatorio.usuarios.setItem(clientes.index(
                    (id, nome)), 2, QtWidgets.QTableWidgetItem(str(num_pedidos)))
        else:
            QMessageBox.warning(window_filter, "Erro",
                                "Nenhum cliente encontrado!")
    else:
        # Segundo filtro
        ano = window_filter.ano.text()
        if not ano:
            QMessageBox.warning(window_filter, "Erro",
                                "Nenhum ano inserido!")
            return
        elif not ano.isnumeric():
            QMessageBox.warning(window_filter, "Erro",
                                "Ano inválido!")
            return
        elif int(ano) > date.today().year:
            QMessageBox.warning(window_filter, "Erro",
                                "Ano inválido!")
            return
        # Obtendo todos as contas que fizeram pedidos em todos os meses do ano selecionado
        cursor.execute(
            "SELECT id_conta, COUNT(DISTINCT MONTH(data)) as num_meses FROM pedido WHERE YEAR(data)=%s GROUP BY id_conta HAVING num_meses=12", (ano,))
        contas = cursor.fetchall()
        if contas:
            # Formatando tabela
            window_relatorio.usuarios.setRowCount(len(contas))
            # Atualizando label que mostra total de usuários
            window_relatorio.total.setText(f"Total: {len(contas)} em {ano}")
            for id_conta, num_meses in contas:
                # Obtendo nome do cliente
                cursor.execute(
                    "SELECT nome FROM cliente WHERE id = (SELECT id_cliente FROM conta WHERE id = %s);", (id_conta,))
                nome = cursor.fetchone()
                nome = nome[0]

                # Obtendo numero de pedidos
                cursor.execute(
                    "SELECT COUNT(id) FROM pedido WHERE id_conta = %s;", (id_conta,))
                num_pedidos = cursor.fetchone()
                num_pedidos = num_pedidos[0]

                # Inserindo dados
                window_relatorio.usuarios.setItem(contas.index(
                    (id_conta, num_meses)), 0, QtWidgets.QTableWidgetItem(str(id_conta)))
                window_relatorio.usuarios.setItem(contas.index(
                    (id_conta, num_meses)), 1, QtWidgets.QTableWidgetItem(nome))
                window_relatorio.usuarios.setItem(contas.index(
                    (id_conta, num_meses)), 2, QtWidgets.QTableWidgetItem(str(num_pedidos)))
        else:
            QMessageBox.warning(window_filter, "Erro",
                                "Nenhum usuário encontrado!")
            return

        # Formatando tabela
        header = window_relatorio.usuarios.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
    window_filter.close()


def gerar_relatorio():
    # Obtendo forma de pagamento mais utilizada
    cursor.execute(
        "SELECT forma_pagamento, COUNT(*) FROM pagamento GROUP BY forma_pagamento ORDER BY COUNT(*) DESC LIMIT 1;")
    forma_pagamento = cursor.fetchall()
    if not forma_pagamento:
        window_relatorio.forma.setText("Sem registro de pedidos")
        window_relatorio.media.setText("Sem registro de pedidos")
        window_relatorio.ano.setText("Sem registro de pedidos")
        window_relatorio.mes.setText("Sem registro de pedidos")
    else:
        forma_pagamento = forma_pagamento[0][0]
        # Atualizando label com forma de pagamento mais utilizada
        window_relatorio.forma.setText(forma_pagamento)

        # Obtendo a média anual de vendas
        cursor.execute(
            "SELECT AVG(valor_total) FROM pedido WHERE YEAR(data) = YEAR(CURDATE());")
        media_vendas = cursor.fetchall()
        media_vendas = media_vendas[0][0]
        media_vendas = round(media_vendas, 2)
        # Atualizando label com a média anual de vendas
        window_relatorio.media.setText(f"R$ {media_vendas}")

        # Obtendo o ano com maior número de vendas
        cursor.execute(
            "SELECT YEAR(data), COUNT(*) FROM pedido GROUP BY YEAR(data) ORDER BY COUNT(*) DESC LIMIT 1;"
        )
        ano_maior_vendas = cursor.fetchall()
        ano_maior_vendas = ano_maior_vendas[0][0]
        # Atualizando label com o ano com maior número de vendas
        window_relatorio.ano.setText(str(ano_maior_vendas))

        # Obtendo o mês com maior número de vendas
        cursor.execute(
            "SELECT MONTH(data), COUNT(*) FROM pedido GROUP BY MONTH(data) ORDER BY COUNT(*) DESC LIMIT 1;"
        )
        mes_maior_vendas = cursor.fetchall()
        mes_maior_vendas = mes_maior_vendas[0][0]
        # Atualizando label com o mês com maior número de vendas
        window_relatorio.mes.setText(str(mes_maior_vendas))

    # obtendo todos os ids de contas
    cursor.execute("SELECT id FROM conta;")
    ids_contas = cursor.fetchall()

    # Organizando tabela de clientes
    window_relatorio.usuarios.setRowCount((len(ids_contas) - 1))

    posicao = -1
    for id in ids_contas:
        posicao += 1
        if id[0] == id_conta:
            # print(id_conta)
            posicao -= 1
            continue
        # nome de cada cliente
        cursor.execute(
            "SELECT id_cliente FROM conta WHERE id = %s;", (id[0],))
        id_cliente = cursor.fetchone()
        id_cliente = id_cliente[0]
        cursor.execute(
            "SELECT nome FROM cliente WHERE id = %s;", (id_cliente,))
        nome_cliente = cursor.fetchone()
        nome_cliente = nome_cliente[0]

        # Obtendo numero de pedidos
        cursor.execute(
            "SELECT COUNT(id) FROM pedido WHERE id_conta = %s;", (id[0],))
        num_pedidos = cursor.fetchone()
        num_pedidos = num_pedidos[0]

        window_relatorio.usuarios.setItem(
            posicao, 0, QtWidgets.QTableWidgetItem(str(id[0])))
        window_relatorio.usuarios.setItem(
            posicao, 1, QtWidgets.QTableWidgetItem(nome_cliente))
        window_relatorio.usuarios.setItem(
            posicao, 2, QtWidgets.QTableWidgetItem(str(num_pedidos)))

    header = window_relatorio.usuarios.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    window_relatorio.total.setText(
        f"Total: {len(ids_contas) -1} usuários no sistema")

    window_relatorio.show()


def realizar_pagamento():
    # Obtendo id do pedido que foi selecionado
    linha = window_pagamento.tableWidget.currentRow()
    try:
        id_pedido = window_pagamento.tableWidget.item(linha, 0).text()
    except:
        QMessageBox.warning(window_pagamento, "Erro",
                            "Selecione um pedido para realizar o pagamento")
        return
    # Obtendo valor a pagar do pedido
    cursor.execute(
        "SELECT valor_a_pagar FROM pedido WHERE id = %s;", (id_pedido,))
    valor_a_pagar = cursor.fetchall()
    valor_a_pagar = valor_a_pagar[0][0]

    # Obtendo forma de pagamento do radio button
    if window_pagamento.cartao.isChecked():
        forma_pagamento = "cartao"
    elif window_pagamento.boleto.isChecked():
        forma_pagamento = "boleto"
    elif window_pagamento.pix.isChecked():
        forma_pagamento = "pix"
    else:
        QMessageBox.warning(window_pagamento, "Erro",
                            "Forma de pagamento não selecionada!")
        window_pagamento.close()

    # Obtendo valor pago da double spin box
    valor_pago = window_pagamento.valor_pago.value()
    # print(valor_pago)

    # Verificando se o valor pago é maior que o valor a pagar
    if valor_pago > valor_a_pagar:
        QMessageBox.warning(window_pagamento, "Erro",
                            "Valor pago maior que valor a pagar!")
    else:
        valor_a_pagar -= valor_pago
        # Atualizando valor a pagar do pedido
        cursor.execute(
            "UPDATE pedido SET valor_a_pagar = %s WHERE id = %s;",
            (valor_a_pagar, id_pedido))
        # Atualizando status do pedido
        if valor_a_pagar == 0:
            cursor.execute(
                "UPDATE pedido SET status = 'pago' WHERE id = %s;",
                (id_pedido,))
        else:
            cursor.execute(
                "UPDATE pedido SET status = 'pagamento parcial' WHERE id = %s;",
                (id_pedido,))
        # Registrando pagamento
        data = date.today()
        cursor.execute(
            "INSERT INTO pagamento (id_pedido, valor, forma_pagamento, data) VALUES (%s, %s, %s, %s);", (id_pedido, valor_pago, forma_pagamento, data))
        QMessageBox.about(window_pagamento, "Sucesso", "Pagamento realizado!")
        window_pagamento.close()
        db.commit()


def conf_window_pagamento():
    # Organizando tabela com pedidos com pagamento pendente
    cursor.execute(
        "SELECT id, valor_total, valor_a_pagar, data FROM pedido WHERE id_conta = %s and (status = 'aguardando pagamento' or status = 'pagamento parcial');",
        (id_conta,))
    resultado = cursor.fetchall()
    if not resultado:
        QMessageBox.about(window_pagamento, "Erro",
                          "Não há pedidos com pagamento pendente!")
        return
    window_pagamento.tableWidget.setRowCount(len(resultado))

    for id, valor_total, valor_a_pagar, data in resultado:
        window_pagamento.tableWidget.setItem(
            resultado.index((id, valor_total, valor_a_pagar, data)), 0,
            QtWidgets.QTableWidgetItem(str(id)))
        window_pagamento.tableWidget.setItem(
            resultado.index((id, valor_total, valor_a_pagar, data)), 1,
            QtWidgets.QTableWidgetItem(str(valor_total)))
        window_pagamento.tableWidget.setItem(
            resultado.index((id, valor_total, valor_a_pagar, data)), 2,
            QtWidgets.QTableWidgetItem(str(valor_a_pagar)))
        window_pagamento.tableWidget.setItem(
            resultado.index((id, valor_total, valor_a_pagar, data)), 3,
            QtWidgets.QTableWidgetItem(str(data)))

    header = window_pagamento.tableWidget.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    window_pagamento.show()


def cad_prod():
    nome = window_cad_prod.nome.text()
    preco = window_cad_prod.preco.text()
    cor = window_cad_prod.cor.text()
    if nome and cor:
        try:
            cursor.execute(
                "INSERT INTO catalogo (nome, preco, cor) VALUES (%s, %s, %s);",
                (nome, preco, cor))
        except:
            QMessageBox.warning(window_cad_prod, "Erro",
                                "Verifique os dados inseridos!")
        else:
            QMessageBox.about(window_cad_prod, "Sucesso!",
                              "Produto registrado!")
            window_cad_prod.close()
            window_cad_prod.nome.setText("")
            window_cad_prod.preco.setText("")
            window_cad_prod.cor.setText("")
    else:
        QMessageBox.warning(window_cad_prod, "Erro",
                            "Verifique os dados inseridos!")
    db.commit()


def realiza_pedido_adm():
    global id_conta
    id_conta = window_ask_id.lineEdit.text()
    id_conta = int(id_conta)
    # Verificando se o id da conta existe
    cursor.execute("SELECT id from conta where id = %s;", (id_conta, ))
    resultado = cursor.fetchone()
    if resultado:
        window_ask_id.close()
        window_client.show()
        menu_cliente()
    else:
        QMessageBox.information(window_ask_id, "Erro",
                                "Conta não encontrada")


def alt_status():
    # Obtendo linha selecionada
    linha = window_alt_status.tableWidget.currentRow()
    # Obtendo valor selecionado na comboBox
    status = window_alt_status.comboBox.currentText()
    # Obtendo id da conta
    id_conta = window_alt_status.tableWidget.item(linha, 0).text()
    id_conta = int(id_conta)

    # Alterando status da conta
    cursor.execute(
        "UPDATE usuario_web SET status = %s WHERE id_conta = %s;", (status, id_conta, ))
    window_alt_status.close()
    alt_status_window()
    db.commit()


def alt_status_window():
    global id_conta
    window_alt_status.show()

    # Obtendo status dos usuários web e id da conta
    cursor.execute("SELECT status, id_conta from usuario_web;")
    resultado = cursor.fetchall()
    if resultado:
        window_alt_status.tableWidget.setRowCount(len(resultado) - 1)
        # Obtendo id de cliente de cada conta
        posicao = -1
        for status, conta in resultado:
            posicao += 1
            if conta == id_conta:  # Conta de administrador
                posicao -= 1
                continue
            # Obtendo id de cliente de cada conta
            cursor.execute("SELECT id_cliente from conta where id = %s;",
                           (conta, ))
            id_cliente = cursor.fetchone()
            id_cliente = id_cliente[0]
            # Obtendo nome de cada cliente
            cursor.execute("SELECT nome from cliente where id = %s;",
                           (id_cliente, ))
            nome = cursor.fetchone()
            nome = nome[0]

            # Inserindo dados na tabela
            window_alt_status.tableWidget.setItem(
                posicao, 0, QtWidgets.QTableWidgetItem(str(conta)))
            window_alt_status.tableWidget.setItem(
                posicao, 1, QtWidgets.QTableWidgetItem(str(nome)))
            window_alt_status.tableWidget.setItem(
                posicao, 2, QtWidgets.QTableWidgetItem(str(status)))

        header = window_alt_status.tableWidget.horizontalHeader()
        header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)


def hist_ver_itens():
    # Obtendo id do pedido
    id_pedido = window_hist.tableWidget.item(
        window_hist.tableWidget.currentRow(), 0).text()
    id_pedido = int(id_pedido)

    # Obtendo itens do pedido
    cursor.execute(
        "SELECT car_cat.quantidade, catalogo.nome FROM catalogo INNER JOIN car_cat ON catalogo.id = car_cat.id_catalogo WHERE car_cat.pedido = %s;",
        (id_pedido, ))
    itens = cursor.fetchall()
    if itens:
        window_det_ped.show()
        window_det_ped.tableWidget.setRowCount(len(itens))
        for item in itens:
            quantidade = item[0]
            nome = item[1]
            window_det_ped.tableWidget.setItem(
                itens.index(item), 0, QtWidgets.QTableWidgetItem(str(nome)))
            window_det_ped.tableWidget.setItem(
                itens.index(item), 1, QtWidgets.QTableWidgetItem(str(quantidade)))

            header = window_det_ped.tableWidget.horizontalHeader()
            header.setSectionResizeMode(
                0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(
                1, QtWidgets.QHeaderView.ResizeToContents)


def historico_compras():
    global id_conta

    # Obtendo id do carrinho
    cursor.execute(
        "Select id from carrinho where id_conta = %s;", (id_conta,))
    id_carrinho = cursor.fetchone()
    id_carrinho = id_carrinho[0]

    # Obtendo id dos pedidos e data
    cursor.execute(
        "SELECT id, data from pedido where id_conta = %s;", (id_conta,))
    pedidos = cursor.fetchall()
    if pedidos:
        window_hist.show()
        window_hist.tableWidget.setRowCount(len(pedidos))
        for pedido in pedidos:
            id_pedido = pedido[0]
            data = pedido[1]
            # Obtendo produtos do pedido
            cursor.execute(
                "SELECT car_cat.quantidade, catalogo.preco FROM catalogo INNER JOIN car_cat ON catalogo.id = car_cat.id_catalogo WHERE car_cat.id_carrinho = %s and car_cat.pedido = %s;",
                (id_carrinho, id_pedido))
            resultado = cursor.fetchall()

            # Obtendo quantidade de itens
            cursor.execute(
                "SELECT COUNT(*) FROM car_cat WHERE id_carrinho = %s and pedido = %s;",
                (id_carrinho, id_pedido))
            qtd_itens = cursor.fetchone()
            qtd_itens = qtd_itens[0]

            # Status do pedido
            cursor.execute(
                "SELECT status from pedido where id = %s;", (id_pedido,))
            status = cursor.fetchone()
            status = status[0]

            if resultado:
                # Adicionando dados dos pedidos à tabela e quantidade de itens
                for quantidade, preco in resultado:
                    total = 0
                    total += preco * quantidade
                    window_hist.tableWidget.setItem(
                        pedidos.index(pedido), 0, QtWidgets.QTableWidgetItem(str(id_pedido)))
                    window_hist.tableWidget.setItem(
                        pedidos.index(pedido), 1, QtWidgets.QTableWidgetItem(str(status)))
                    window_hist.tableWidget.setItem(
                        pedidos.index(pedido), 2, QtWidgets.QTableWidgetItem(str(total)))
                    window_hist.tableWidget.setItem(
                        pedidos.index(pedido), 3, QtWidgets.QTableWidgetItem(str(qtd_itens)))
                    window_hist.tableWidget.setItem(
                        pedidos.index(pedido), 4, QtWidgets.QTableWidgetItem(str(data)))

                header = window_hist.tableWidget.horizontalHeader()
                header.setSectionResizeMode(
                    0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(
                    1, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(
                    2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(
                    3, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(
                    4, QtWidgets.QHeaderView.ResizeToContents)
    else:
        QMessageBox.about(window_client, "Erro", "Nenhum pedido encontrado.")


def realiza_pedido():
    global id_conta
    data = date.today()
    # Obtendo id do carrinho
    cursor.execute(
        "SELECT id from carrinho where id_conta = %s;", (id_conta,))
    id_carrinho = cursor.fetchall()
    id_carrinho = id_carrinho[0][0]

    # Obtendo valor total da compra
    cursor.execute(
        "SELECT catalogo.preco, car_cat.quantidade FROM catalogo INNER JOIN car_cat ON catalogo.id = car_cat.id_catalogo WHERE car_cat.id_carrinho = %s and car_cat.pedido = -1;",
        (id_carrinho,))
    resultado = cursor.fetchall()
    total = 0
    for preco, quantidade in resultado:
        total += preco * quantidade

    cursor.execute(
        "INSERT INTO pedido (valor_total, id_conta, valor_a_pagar, data) VALUES (%s, %s, %s, %s);",
        (total, id_conta, total, data))

    id_pedido = cursor.lastrowid
    # Alterando o id_pedido na tabela car_cat onde o numero do pedido é -1, logo a compra foi efetuada e o carrinho volta a ser vazio
    cursor.execute(
        "UPDATE car_cat SET pedido = %s WHERE id_carrinho = %s and pedido = -1;",
        (id_pedido, id_carrinho))

    # Alterando status do pedido para "aguardando pagamento"
    cursor.execute(
        "UPDATE pedido SET status = 'aguardando pagamento' WHERE id = %s;",
        (id_pedido,))

    QMessageBox.information(window_client, "Sucesso",
                            "Pedido realizado com sucesso")
    window_ver_carrinho.close()
    atualiza_label_itens(id_carrinho)
    db.commit()


def atualiza_label_itens(id_carrinho):
    # atualizando label de quantidade de itens no carrinho
    cursor.execute(
        "SELECT quantidade FROM car_cat WHERE id_carrinho = %s and pedido = -1;",
        (id_carrinho,))
    resultado = cursor.fetchall()
    quantidade = 0
    for valor in resultado:
        quantidade += valor[0]
    window_client.qtd_carrinho.setText(f"{quantidade}")


def carrinho_cliente():
    global id_conta
    cursor.execute(
        "SELECT id from carrinho where id_conta = %s;", (id_conta,))
    id_carrinho = cursor.fetchall()

    # Verificando itens do carrinho
    cursor.execute(
        "SELECT catalogo.nome, car_cat.quantidade, catalogo.preco FROM catalogo INNER JOIN car_cat ON catalogo.id = car_cat.id_catalogo WHERE car_cat.id_carrinho = %s and car_cat.pedido = -1;",
        (id_carrinho[0][0],))
    resultado = cursor.fetchall()
    if not resultado:
        QMessageBox.about(window_client, "Erro",
                          "Não há produtos no carrinho")
        return

    window_ver_carrinho.show()
    window_ver_carrinho.itens_carrinho.setRowCount(len(resultado))
    for nome, quantidade, preco in resultado:
        window_ver_carrinho.itens_carrinho.setItem(
            resultado.index((nome, quantidade, preco)), 0, QtWidgets.QTableWidgetItem(nome))
        window_ver_carrinho.itens_carrinho.setItem(
            resultado.index((nome, quantidade, preco)), 1, QtWidgets.QTableWidgetItem(str(quantidade)))
        window_ver_carrinho.itens_carrinho.setItem(
            resultado.index((nome, quantidade, preco)), 2, QtWidgets.QTableWidgetItem(str(preco)))

    # alterando tamanho da coluna de acordo com o conteúdo
    header = window_ver_carrinho.itens_carrinho.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    # Obtendo total do carrinho
    cursor.execute(
        "SELECT SUM(catalogo.preco * car_cat.quantidade) FROM catalogo INNER JOIN car_cat ON catalogo.id = car_cat.id_catalogo WHERE car_cat.id_carrinho = %s and car_cat.pedido = -1;",
        (id_carrinho[0][0],))
    total = cursor.fetchone()
    window_ver_carrinho.total_carrinho.setText(f"Total: R${str(total[0])}")


def adicionar_carrinho():
    global id_conta
    # Obtendo id do carrinho
    cursor.execute(
        "SELECT id from carrinho where id_conta = %s;", (id_conta,))
    id_carrinho = cursor.fetchall()
    id_carrinho = id_carrinho[0][0]

    # Obtendo id do produto da linha selecionada
    linha = window_client.table_produtos.currentRow()
    id_produto = window_client.table_produtos.item(linha, 0).text()

    # Verificando se o produto já está no carrinho
    cursor.execute(
        "SELECT id_catalogo FROM car_cat WHERE id_carrinho = %s and id_catalogo = %s and pedido = -1;",
        (id_carrinho, id_produto))
    resultado = cursor.fetchall()
    quantidade = 1
    if resultado:
        # Verificando a quantidade do produto no carrinho
        cursor.execute(
            "SELECT quantidade FROM car_cat WHERE id_carrinho = %s and id_catalogo = %s and pedido = -1;",
            (id_carrinho, id_produto))
        quantidade_atual = cursor.fetchone()
        quantidade += quantidade_atual[0]

        # Atualizando quantidade do produto no carrinho
        cursor.execute(
            "UPDATE car_cat SET quantidade = %s WHERE id_carrinho = %s and id_catalogo = %s and pedido = -1;",
            (quantidade, id_carrinho, id_produto))
    else:
        # Adicionando produto ao carrinho
        cursor.execute(
            "INSERT INTO car_cat (id_carrinho, id_catalogo, quantidade, pedido) VALUES (%s, %s, %s, %s);",
            (id_carrinho, id_produto, quantidade, -1))
    atualiza_label_itens(id_carrinho)
    db.commit()


def menu_cliente():
    global id_conta
    # mostrar produtos disponíveis no catálogo
    cursor.execute("SELECT id, nome, cor, preco FROM catalogo;")
    resultado = cursor.fetchall()
    if not resultado:
        QMessageBox.about(window_client, "Volte mais tarde",
                          "Não há produtos disponíveis")
        return

    #  obtendo quantidade de produtos
    cursor.execute(
        "SELECT COUNT(*) FROM catalogo;")
    quantidade = cursor.fetchone()
    quantidade = quantidade[0]
    window_client.table_produtos.setRowCount(quantidade)

    for id, nome, cor, preco in resultado:
        # f"Nome: {nome}, Preço: R${preco}"
        window_client.table_produtos.setItem(
            resultado.index((id, nome, cor, preco)), 0, QtWidgets.QTableWidgetItem(str(id)))
        window_client.table_produtos.item(
            resultado.index((id, nome, cor, preco)), 0).setTextAlignment(Qt.Qt.AlignCenter)
        window_client.table_produtos.setItem(
            resultado.index((id, nome, cor, preco)), 1, QtWidgets.QTableWidgetItem(nome))
        window_client.table_produtos.item(
            resultado.index((id, nome, cor, preco)), 1).setTextAlignment(Qt.Qt.AlignCenter)
        window_client.table_produtos.setItem(
            resultado.index((id, nome, cor, preco)), 2, QtWidgets.QTableWidgetItem(cor))
        window_client.table_produtos.setItem(
            resultado.index((id, nome, cor, preco)), 3, QtWidgets.QTableWidgetItem(f"R${preco}"))

    # alterando tamanho da coluna de acordo com o conteúdo
    header = window_client.table_produtos.horizontalHeader()
    header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
    header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

    # Obtendo id do carrinho
    cursor.execute(
        "SELECT id from carrinho where id_conta = %s;", (id_conta,))
    id_carrinho = cursor.fetchall()
    id_carrinho = id_carrinho[0][0]
    atualiza_label_itens(id_carrinho)


def login():
    global id_conta
    email = window.input_login.text()
    senha = window.input_senha.text()
    cursor.execute(
        "SELECT senha from usuario_web where email = %s;", (email,))
    resultado = cursor.fetchall()
    if resultado:
        senha_banco = resultado[0][0]
        senha_banco = senha_banco.encode('utf-8')
        if check_password(senha, senha_banco):
            pass
        else:
            QMessageBox.information(window, "Erro", "Senha incorreta")
            return
    else:
        QMessageBox.information(window, "Erro", "Usuário não encontrado")
        return

    cursor.execute(
        "SELECT id_conta from usuario_web where email = %s;", (email,))
    resultado = cursor.fetchall()
    if resultado:
        if email == "adm@adm":
            id_conta = resultado[0][0]
            window_menu_adm.show()
            window.close()
        else:
            id_conta = resultado[0][0]
            # Verificando se usário está com status ativo
            cursor.execute(
                "SELECT status from usuario_web where id_conta = %s;", (id_conta,))
            status = cursor.fetchall()
            status = status[0][0]
            if status.lower() == "ativo":
                window_client.show()
                window.close()
                menu_cliente()
            else:
                QMessageBox.information(window, "Erro",
                                        f"Usuário {status}, entre em contato com o administrador")
    else:
        QMessageBox.about(window, "Erro", "Login ou senha incorretos")


def logout():
    window.show()
    window_client.close()


def display_edit_info():
    window_client.close()
    global id_conta
    # Preenchendo campos com informações do usuário
    cursor.execute(
        "SELECT id_cliente from conta where id = %s;", (id_conta,))
    id_cliente = cursor.fetchall()
    id_cliente = id_cliente[0][0]
    cursor.execute("SELECT nome, cpf, tel1, tel2, bairro, cidade, estado from cliente where id = %s;",
                   (id_cliente,))
    resultado = cursor.fetchall()
    window_edit_info.nome_input.setText(resultado[0][0])
    window_edit_info.nome_input.setReadOnly(True)
    window_edit_info.cpf_input.setText(resultado[0][1])
    window_edit_info.cpf_input.setReadOnly(True)
    window_edit_info.cel_input.setText(str(resultado[0][2]))
    if resultado[0][3]:
        window_edit_info.res_input.setText(str(resultado[0][3]))
    window_edit_info.bairro_input.setText(resultado[0][4])
    window_edit_info.cidade_input.setText(resultado[0][5])
    # Alterando valor do combobox
    index = window_edit_info.comboBox.findText(resultado[0][6])
    window_edit_info.comboBox.setCurrentIndex(index)

    window_edit_info.show()


def edit_info():
    global id_conta
    # obtendo id do cliente
    cursor.execute(
        "SELECT id_cliente from conta where id = %s;", (id_conta,))
    id_cliente = cursor.fetchall()
    id_cliente = id_cliente[0][0]
    # obtendo informações do cliente
    tel1 = window_edit_info.cel_input.text()
    tel2 = window_edit_info.res_input.text()
    bairro = window_edit_info.bairro_input.text()
    cidade = window_edit_info.cidade_input.text()
    estado = window_edit_info.comboBox.currentText()
    # atualizando informações do cliente
    if tel1.isdigit() and bairro and cidade and estado:
        bairro = bairro.title()
        cidade = cidade.title()
        if tel2.isdigit():
            cursor.execute("UPDATE cliente SET tel1 = %s, tel2 = %s, bairro = %s, cidade = %s, estado = %s where id = %s;",
                           (tel1, tel2, bairro, cidade, estado, id_cliente))
        else:
            cursor.execute("UPDATE cliente SET tel1 = %s, bairro = %s, cidade = %s, estado = %s where id = %s;",
                           (tel1, bairro, cidade, estado, id_cliente))
        window_client.show()
        window_edit_info.close()
        db.commit()
    else:
        QMessageBox.warning(window_edit_info, "Erro",
                            "Verifique os dados inseridos")


def cad_usr_web():
    email = window_cad_usr_web.email_input.text()
    senha = window_cad_usr_web.senha_input.text()
    hash = hash_password(senha)
    hash = hash.decode("utf-8")
    if email and senha:
        # Verificando se email já existe no sistema
        cursor.execute(
            "SELECT email from usuario_web where email = %s;", (email,))
        resultado = cursor.fetchall()
        # print(resultado)
        if resultado:
            QMessageBox.about(window_cad_usr_web, "Erro",
                              "E-mail já cadastrado")
        else:
            cursor.execute(
                "INSERT INTO usuario_web (email, senha, id_conta) VALUES (%s, %s, %s);",
                (email, hash, id_conta))

            # Criando carrinho para a conta, se for não for usuário web, carrinho é vinculado à administração
            cursor.execute(
                "INSERT INTO carrinho (id_conta, login_web) VALUES (%s, %s);", (id_conta, email))
            window_cad_cliente.close()
            window.close()
            window_cad_usr_web.close()
            db.commit()
            menu_cliente()
            window_client.show()
        # zerando campos
    window_cad_usr_web.email_input.setText("")
    window_cad_usr_web.senha_input.setText("")


def cad_cliente():
    global id_conta

    cpf = window_cad_cliente.cpf_input.text()
    nome = window_cad_cliente.nome_input.text()
    tel = window_cad_cliente.cel_input.text()
    tel2 = window_cad_cliente.res_input.text()
    cidade = window_cad_cliente.cidade_input.text()
    bairro = window_cad_cliente.bairro_input.text()
    estado = window_cad_cliente.comboBox.currentText()

    if (cpf.isdigit() and (len(cpf) == 11)) and nome and (tel.isdigit() and (len(tel) >= 9)) and cidade and bairro:
        # verificando se o cpf já existe
        cursor.execute("SELECT cpf FROM cliente WHERE cpf = %s;", (cpf,))
        resultado = cursor.fetchall()
        if resultado:
            QMessageBox.about(window_cad_cliente, "Erro", "CPF já cadastrado")
        else:
            cidade = cidade.title()
            bairro = bairro.title()
            # Verficando se foi inserido um telefone residencial
            if tel2.isdigit():
                cursor.execute(
                    "INSERT INTO cliente (cpf, nome, tel1, tel2, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s, %s);",
                    (cpf, nome, tel, tel2, bairro, cidade, estado))
            else:
                cursor.execute(
                    "INSERT INTO cliente (cpf, nome, tel1, bairro, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s);",
                    (cpf, nome, tel, bairro, cidade, estado))
            # Criando conta para cliente
            cursor.execute("select id from cliente where cpf = %s;", (cpf,))
            id_cliente = cursor.fetchone()
            cursor.execute(
                "INSERT INTO conta (id_cliente) VALUES (%s);", (id_cliente))
            id_conta = cursor.lastrowid
            # Verificando se cliente deseja ser usuário Web
            if window_cad_cliente.checkBox.isChecked():
                window_cad_usr_web.show()
                window_cad_cliente.close()
            else:
                # Carrinho vinculado à adm por meio do valor default
                cursor.execute(
                    "INSERT INTO carrinho (id_conta) VALUES (%s);", (id_conta,))
                window_cad_cliente.close()
                window.close()
                db.commit()
                menu_cliente()
                window_client.show()
    else:
        QMessageBox.warning(window_cad_cliente, "Erro",
                            "Verifique os dados inseridos")

    # zerando campos
    window_cad_cliente.cpf_input.setText("")
    window_cad_cliente.nome_input.setText("")
    window_cad_cliente.cel_input.setText("")
    window_cad_cliente.res_input.setText("")
    window_cad_cliente.cidade_input.setText("")
    window_cad_cliente.bairro_input.setText("")
    window_cad_cliente.comboBox.setCurrentIndex(0)


app = QtWidgets.QApplication([])

# Carregando os arquivos .ui
window = uic.loadUi('UI/form.ui')
window_client = uic.loadUi('UI/new_client.ui')
window_cad_cliente = uic.loadUi('UI/cadastro.ui')
window_ver_carrinho = uic.loadUi('UI/ver_carrinho.ui')
window_cad_usr_web = uic.loadUi('UI/cad_usr_web.ui')
window_menu_adm = uic.loadUi('UI/menu_adm.ui')
window_ask_id = uic.loadUi('UI/ask_id.ui')
window_hist = uic.loadUi('UI/hist.ui')
window_det_ped = uic.loadUi('UI/det_ped.ui')
window_alt_status = uic.loadUi('UI/alt_status.ui')
window_cad_prod = uic.loadUi('UI/cad_prod.ui')
window_pagamento = uic.loadUi('UI/pagamento.ui')
window_relatorio = uic.loadUi('UI/estatisticas.ui')
window_filter = uic.loadUi('UI/filter.ui')
window_edit_info = uic.loadUi('UI/edit_info.ui')

# adicionando ícones às janelas
window.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_client.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_cad_cliente.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_ver_carrinho.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_cad_usr_web.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_menu_adm.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_ask_id.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_hist.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_det_ped.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_alt_status.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_cad_prod.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_pagamento.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_relatorio.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_filter.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))
window_edit_info.setWindowIcon(QtGui.QIcon('Imgs/icon.png'))

window.show()

# Conectando os botões com as funções
window.pushButton.clicked.connect(login)
window.commandLinkButton.clicked.connect(window_cad_cliente.show)
window_cad_cliente.pushButton.clicked.connect(cad_cliente)
window_client.ver_carrinho.clicked.connect(carrinho_cliente)
window_client.adc_carrinho.clicked.connect(adicionar_carrinho)
window_client.real_pgmt.clicked.connect(conf_window_pagamento)
window_client.actionSair.triggered.connect(logout)
window_client.action_edit.triggered.connect(display_edit_info)
window_cad_usr_web.pushButton.clicked.connect(cad_usr_web)
window_ver_carrinho.fecha_carrinho.clicked.connect(realiza_pedido)
window_client.ver_hist.clicked.connect(historico_compras)
window_hist.ver_itens.clicked.connect(hist_ver_itens)
window_menu_adm.btn_alt.clicked.connect(alt_status_window)
window_alt_status.alt_sel.clicked.connect(alt_status)
window_menu_adm.btn_real.clicked.connect(window_ask_id.show)
window_ask_id.pushButton.clicked.connect(realiza_pedido_adm)
window_menu_adm.btn_cad.clicked.connect(window_cad_prod.show)
window_menu_adm.btn_est.clicked.connect(gerar_relatorio)
window_cad_prod.pushButton.clicked.connect(cad_prod)
window_pagamento.pushButton.clicked.connect(realizar_pagamento)
window_relatorio.pushButton.clicked.connect(window_filter.show)
window_filter.pushButton.clicked.connect(filtro)
window_edit_info.pushButton.clicked.connect(edit_info)
window_filter.actionpedidos.triggered.connect(ordenar_pedidos)
window_filter.actionPor_valor_gasto.triggered.connect(ordenar_valor)


app.exec_()
