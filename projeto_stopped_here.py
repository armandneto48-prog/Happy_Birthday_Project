import numpy as np
import math
import os
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, ColorClip, concatenate_videoclips, AudioFileClip
import moviepy.video.fx as fx

# 1. CONFIGURAÇÕES GLOBAIS
L, A = 1920, 1080

# 2. BLOCO 1: CINEMA
def gerar_bloco_cinema():
    print("Carregando Abertura de Cinema...")
    try:
        gif = (VideoFileClip("cinema_gif.gif")
               .with_effects([fx.Resize(width=L)])
               .with_duration(5))
        return gif
    except Exception as e:
        print(f"Erro no GIF: {e}")
        return ColorClip(size=(L, A), color=(0,0,0)).with_duration(2)

# 3. BLOCO 2: GALERIA TI
def gerar_bloco_ti():
    print("Criando Galeria de TI...")
    duracao_img = 3
    transicao = 1.0
    
    def carregar_foto(nome):
        if os.path.exists(nome):
            return (ImageClip(nome)
                    .with_duration(duracao_img)
                    .with_effects([fx.Resize(width=L)]) 
                    .with_position(("center", "center")))
        return ColorClip(size=(L, A), color=(0,0,0)).with_duration(duracao_img)

    c1 = carregar_foto("it1.webp")
    c2 = carregar_foto("it2.jpg").with_start(2.0).with_effects([fx.SlideIn(duration=transicao, side="left")])
    c3 = carregar_foto("it3.jpg").with_start(4.0).with_effects([fx.SlideIn(duration=transicao, side="left")])
    c4 = carregar_foto("it4.jpg").with_start(6.0).with_effects([fx.SlideIn(duration=transicao, side="left")])

    return CompositeVideoClip([c1, c2, c3, c4], size=(L, A))

# 4. BLOCO 3: ANIMAÇÃO FINAL
def gerar_bloco_final_animado():
    print("Criando Animação Principal (Pai & Filho)...")
    duracao = 8
    terco = L // 3

    # SEÇÃO 1: ESQUERDA
    fundo_esq = (ImageClip("foto1.jpg").with_duration(duracao)
                 .with_effects([fx.Resize(height=A)]).with_position((0, 0)))
    
    def flutuar(t):
        return (100, int(400 + 30 * math.sin(2 * math.pi * 0.5 * t)))

    personagem = (ImageClip("foto2.png").with_duration(duracao)
                  .with_effects([fx.Resize(width=400)]).with_position(flutuar))

    # SEÇÃO 2: CENTRO
    if os.path.exists("it_ecossystem.webp"):
        img_it = ImageClip("it_ecossystem.webp").with_duration(duracao)
    else:
        img_it = ColorClip(size=(terco, A), color=(20,20,20)).with_duration(duracao)
    
    img_it = img_it.with_effects([fx.Resize(height=A)])
    x1 = (img_it.size[0] // 2) - (terco // 2)
    fundo_centro = (img_it.with_effects([fx.Crop(x1=x1, y1=0, x2=x1+terco, y2=A)])
                    .with_position((terco, 0)))

    def pular(t):
        return (terco + 200, int(750 - abs(120 * math.sin(math.pi * 1.5 * t))))

    animal = (ImageClip("cat.webp").with_duration(duracao)
              .with_effects([fx.Resize(width=180)]).with_position(pular))

    # SEÇÃO 3: DIREITA
    fundo_dir = ColorClip(size=(terco, A), color=(34, 139, 34)).with_duration(duracao).with_position((terco*2, 0))
    pista = ColorClip(size=(terco, 40), color=(139, 69, 19)).with_duration(duracao).with_position((terco*2, 850))

    def andar(t):
        x = ((t % 4) / 4) * (terco - 150)
        return (int(terco * 2 + x), 650)

    gato_dir = (ImageClip("cat.webp").with_duration(duracao)
                .with_effects([fx.Resize(width=200)]).with_position(andar))

    # MENSAGENS DE TEXTO
    tempo_texto = 4 
    def criar_msg(nome, pos, width):
        if os.path.exists(nome):
            return (ImageClip(nome).with_duration(duracao - tempo_texto)
                    .with_start(tempo_texto).with_effects([fx.Resize(width=width)])
                    .with_position(pos))
        return ColorClip(size=(width, 80), color=(50, 50, 50)).with_start(tempo_texto).with_duration(duracao-tempo_texto).with_position(pos)

    msg_meio = criar_msg("msg_pai.png", (terco + 150, 450), 300)
    msg_dir = criar_msg("msg_programadores.png", (terco * 2 + 50, 550), 350)

    return CompositeVideoClip([fundo_esq, personagem, fundo_centro, animal, fundo_dir, pista, gato_dir, msg_meio, msg_dir], size=(L, A))

# 5. EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    bloco1 = gerar_bloco_cinema()
    bloco2 = gerar_bloco_ti()
    bloco3 = gerar_bloco_final_animado()

    print("\n--- Iniciando Fusão Final ---")
    video_final = concatenate_videoclips([bloco1, bloco2, bloco3], method="compose")

    try:
        audio = AudioFileClip("music.mp3.mp3").with_duration(video_final.duration)
        video_final = video_final.with_audio(audio)
        print("Áudio sincronizado!")
    except:
        print("Aviso: music.mp3.mp3 não encontrada. Vídeo sem som.")

    video_final.write_videofile("PROJETO_FINAL_COMPLETO.mp4", fps=24, codec="libx264")
    print("\nPROJETO CONCLUÍDO!")