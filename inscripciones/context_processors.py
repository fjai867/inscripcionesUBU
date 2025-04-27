def usuario_en_cabecera(request):
    """
    Context processor para agregar el nombre de usuario al contexto si está autenticado.
    """
    username = request.session.get('username')
    return {'cabecera_usuario': username}