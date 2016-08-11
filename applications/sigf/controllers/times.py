# -*- coding: utf-8 -*-
# tente algo como
#@auth.requires(auth.has_membership('usuarios') or auth.has_membership('admin'))
def cadastrar():
   


    form = ''
    rows = SQLFORM.grid(((db.t_time)),#Select que filtra o grid
        searchable=False, #Busca com query
        fields=[
                 db.t_time.f_nome,db.t_time.f_qtd_jogadores,
               ],  #Campos visiveis
        deletable=False, #Botao de deletar
        paginate=10, #Numero de items da paginacao
        create=False, #Permite inserir novos dados
        editable=False,
        maxtextlength=100, #permite definir a quantidade máxima de caracteres do atributo
        field_id=db.t_time.id,
        csv=False, #Botao de exportar para csv
        user_signature=True
        )
    if not request.args:
        #form = A(I(_class='icon-plus'),'Localizar',_href=URL("plantonista", "novo_admin"),_class="btn btn-default")
        form = A(I(_class='icon-plus'))

    return dict(form = form, rows = rows)
