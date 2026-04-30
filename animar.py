from moviepy.editor import ImageClip, CompositeVideoClip

def criar_animacao():
    # 1. Carregar as imagens
    # Usaremos a foto original como fundo e a sem fundo como sobreposição
    fundo = ImageClip("foto1.jpg").set_duration(5)
    pessoas = ImageClip("foto2.png").set_duration(5)

    # 2. Configurar o tamanho (ex: 1080p ou tamanho da foto original)
    largura, altura = fundo.size

    # 3. Criar efeito de Zoom/Movimento no Fundo
    # O fundo vai crescer levemente (de 100% para 110% do tamanho)
    fundo_animado = fundo.resize(lambda t: 1 + 0.02*t).set_position('center')

    # 4. Criar efeito de movimento nas Pessoas (Frente)
    # Elas vão se mover levemente para cima para dar vida
    pessoas_animadas = pessoas.resize(lambda t: 1 + 0.04*t).set_position('center')

    # 5. Juntar tudo
    video_final = CompositeVideoClip([fundo_animado, pessoas_animadas], size=(largura, altura))

    # 6. Salvar o vídeo
    print("Renderizando o vídeo de homenagem...")
    video_final.write_videofile("homenagem_pai.mp4", fps=24)

if __name__ == "__main__":
    criar_animacao()