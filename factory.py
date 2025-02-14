from models import Evento

class EventoFactory:
    @staticmethod
    def create_evento(tipo, titulo, descricao, imagem=None):
        """
        Cria e retorna uma nova instância de Evento.

        Args:
            tipo (str): O tipo do evento (evento, sala, laboratorio).
            titulo (str): O título do evento.
            descricao (str): A descrição do evento.
            imagem (str, optional): O caminho da imagem do evento. Default é None.

        Returns:
            Evento: Uma nova instância de Evento.
        """
        # Validação de dados
        if not titulo or not descricao or not tipo:
            raise ValueError("Título, descrição e tipo são obrigatórios")

        # Validação de comprimento
        if len(titulo) > 150:
            raise ValueError("O título não pode exceder 150 caracteres")
        if len(descricao) > 1000:
            raise ValueError("A descrição não pode exceder 1000 caracteres")

        # Validação de tipo
        tipos_validos = ['evento', 'sala', 'laboratorio']
        if tipo not in tipos_validos:
            raise ValueError(f"Tipo inválido. Os tipos válidos são: {', '.join(tipos_validos)}")

        # Criação do evento
        return Evento(titulo=titulo, descricao=descricao, tipo=tipo, imagem=imagem)