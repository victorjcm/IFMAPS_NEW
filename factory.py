from models import Evento, Sala, Laboratorio

class EventoFactory:
    @staticmethod
    def create(tipo, titulo, descricao, imagem=None, capacidade=None, equipamentos=None):
        """
        Cria e retorna uma nova instância de Evento, Sala ou Laboratório.

        Args:
            tipo (str): O tipo do item (evento, sala, laboratorio).
            titulo (str): O título do item.
            descricao (str): A descrição do item.
            imagem (str, optional): O caminho da imagem do item. Default é None.
            capacidade (int, optional): Capacidade da sala. Apenas para salas.
            equipamentos (str, optional): Equipamentos do laboratório. Apenas para laboratórios.

        Returns:
            Evento | Sala | Laboratorio: Uma nova instância do tipo correspondente.
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

        # Criação do objeto correspondente
        if tipo == "evento":
            return Evento(titulo=titulo, descricao=descricao, imagem=imagem)
        elif tipo == "sala":
            return Sala(titulo=titulo, descricao=descricao, imagem=imagem, capacidade=capacidade)
        elif tipo == "laboratorio":
            return Laboratorio(titulo=titulo, descricao=descricao, imagem=imagem, equipamentos=equipamentos)
        else:
            raise ValueError("Tipo de item desconhecido")
