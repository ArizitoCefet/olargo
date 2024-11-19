from flask import Blueprint, render_template, request, redirect, flash
from models import Pedido, Cliente
from database import db

bp_pedido = Blueprint('pedidos', __name__, template_folder='templates')

@bp_pedido.route('/')
def index():
    dados = Pedido.query.all()
    return render_template('pedido.html', pedidos=dados)

@bp_pedido.route('/add')
def add():
    clientes = Cliente.query.all()
    return render_template('pedido_add.html', clientes=clientes)

@bp_pedido.route('/save', methods=['POST'])
def save():
    id_cliente = request.form.get('id_cliente')
    valor_total = request.form.get('valor_total')
    data = request.form.get('data')
    
    if id_cliente and valor_total and data:
        bd_pedido = Pedido(id_cliente=id_cliente, valor_total=valor_total, data=data)
        db.session.add(bd_pedido)
        db.session.commit()
        flash('Pedido salvo com sucesso!')
        return redirect('/pedidos')
    else:
        flash('Preencha todos os campos!')
        return redirect('/pedidos/add')

@bp_pedido.route("/remove/<int:id>")
def remove(id):
    pedido = Pedido.query.get(id)
    if pedido:
        db.session.delete(pedido)
        db.session.commit()
        flash('Pedido removido com sucesso!')
    else:
        flash('Pedido não encontrado!')
    return redirect("/pedidos")

@bp_pedido.route("/edita/<int:id>")
def edita(id):
    pedido = Pedido.query.get(id)
    clientes = Cliente.query.all()
    if pedido:
        return render_template("pedido_edita.html", pedido=pedido, clientes=clientes)
    else:
        flash("Pedido não encontrado!")
        return redirect("/pedidos")

@bp_pedido.route("/editasave", methods=['POST'])
def editasave():
    id = request.form.get('id')
    id_cliente = request.form.get('id_cliente')
    valor_total = request.form.get('valor_total')
    data = request.form.get('data')
    
    if id and id_cliente and valor_total and data:
        pedido = Pedido.query.get(id)
        if pedido:
            pedido.id_cliente = id_cliente
            pedido.valor_total = valor_total
            pedido.data = data
            db.session.commit()
            flash('Pedido atualizado com sucesso!')
            return redirect('/pedidos')
        else:
            flash('Pedido não encontrado!')
            return redirect('/pedidos')
    else:
        flash('Dados incompletos.')
        return redirect("/pedidos")
