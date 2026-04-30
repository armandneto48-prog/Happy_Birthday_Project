import numpy as np
import math
import os
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, ColorClip, concatenate_videoclips
import moviepy.video.fx as fx

# Configurações Globais
L, A = 1920, 1080

def gerar_bloco_cinema():
    print("Carregando Abertura de Cinema...")
    try:
        # Carrega o GIF e garante que preenche a tela
        gif = (VideoFileClip("cinema_gif.gif")
               .with_effects([fx.Resize(width=L)])
               .with_duration(5)) # Duração fixa de 5 segundos
        return gif
    except Exception as e:
        print(f"Erro no GIF: {e}")
        return ColorClip(size=(L, A), color=(0,0,0)).with_duration(2)

def gerar_bloco_ti():
    print("Criando Galeria de TI com transições...")
    duracao_img = 3
    transicao = 1.0
    arquivos = ["it1.webp", "it2.jpg", "it3.jpg", "it4.jpg"]
    clips = []

    for nome in arquivos:
        if os.path.exists(nome):
            clip = (ImageClip(nome)
                    .with_duration(duracao_img)
                    .with_effects([fx.Resize(height=A)])
                    .with_position("center"))
            clips.append(clip)

    # Lógica de sobreposição para o efeito Slide
    resultado = [clips[0]]
    tempo_acumulado = clips[0].duration
    
    for i in range(1, len(clips)):
        inicio = tempo_acumulado - transicao
        clip_movel = clips[i].with_start(inicio).with_effects([
            fx.SlideIn(duration=transicao, side="left")
        ])
        resultado.append(clip_movel)
        tempo_acumulado = inicio + clips[i].duration
            
    return CompositeVideoClip(resultado, size=(L, A))

def gerar_bloco_final_animado():
    print("Criando Animação Principal (Pai & Filho)...")
    duracao = 8
    terco = L // 3

    # SEÇÃO 1: FOTO ORIGINAL
    fundo_esq = (ImageClip("foto1.jpg")
                 .with_duration(duracao)
                 .with_effects([fx.Resize(height=A)])
                 .with_position((0, 0)))
    
    def flutuar(t):
        return (100, int(400 + 30 * math.sin(2 * math.pi * 0.5 * t)))

    personagem = (ImageClip("foto2.png")
                  .with_duration(duracao)
                  .with_effects([fx.Resize(width=400)])
                  .with_position(flutuar))

    # SEÇÃO 2: ECOSSISTEMA TI CENTRALIZADO
    img_it = ImageClip("it_ecossystem.jpg").with_duration(duracao)
    img_it = img_it.with_effects([fx.Resize(height=A)])
    x1 = (img_it.size[0] // 2) - (terco // 2)
    fundo_centro = (img_it.with_effects([fx.Crop(x1=x1, y1=0, x2=x1+terco, y2=A)])
                    .with_position((terco, 0)))

    def pular(t):
        return (terco + 200, int(750 - abs(120 * math.sin(math.pi * 1.5 * t))))

    animal = (ImageClip("cat.webp").with_duration(duracao)
              .with_effects([fx.Resize(width=180)])
              .with_position(pular))

    try:
        txt = (ImageClip("texto.png").with_duration(duracao)
               .with_effects([fx.Resize(width=400)])
               .with_position((terco + 120, 150)))
    except:
        txt = ColorClip(size=(1,1), color=(0,0,0)).with_duration(duracao)

    # SEÇÃO 3: SELVA
    fundo_dir = ColorClip(size=(terco, A), color=(34, 139, 34)).with_duration(duracao).with_position((terco*2, 0))
    pista = ColorClip(size=(terco, 40), color=(139, 69, 19)).with_duration(duracao).with_position((terco*2, 850))

    def andar(t):
        x = ((t % 4) / 4) * (terco - 150)
        return (int(terco * 2 + x), 650)

    gato = (ImageClip("cat.webp").with_duration(duracao)
            .with_effects([fx.Resize(width=200)])
            .with_position(andar))

    return CompositeVideoClip([fundo_esq, personagem, fundo_centro, animal, txt, fundo_dir, pista, gato], size=(L, A))

if __name__ == "__main__":
    # 1. Gerar os pedaços
    bloco1 = gerar_bloco_cinema()
    bloco2 = gerar_bloco_ti()
    bloco3 = gerar_bloco_final_animado()

    # 2. Unir tudo sequencialmente
    print("\n--- Iniciando Fusão Final ---")
    video_final = concatenate_videoclips([bloco1, bloco2, bloco3], method="compose")

    # 3. Output
    video_final.write_videofile("PROJETO_FINAL_COMPLETO.mp4", fps=24, codec="libx264")
    print("\nPARABÉNS! O seu filme está pronto: PROJETO_FINAL_COMPLETO.mp4")