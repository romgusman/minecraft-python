from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from random import choice
import os

app = Ursina(borderless=False, vsync=True, fullscreen=False)
window.size = (1280, 720)

# Lista de texturas disponíveis
available_textures = ['grass', 'dirt', 'stone', 'ground']

# Carregar texturas válidas
textures = {}
for texture in available_textures:
    texture_path = f"{texture}.png"
    if os.path.isfile(texture_path):
        textures[texture] = load_texture(texture_path)  # Adiciona à lista se existir
    else:
        print(f"Texture '{texture}.png' not found.")

chunk_size = 18  # Tamanho do chunk em blocos (raio)
max_blocks = 1024  # Limite máximo de blocos

# Armazenar blocos
blocks = {}
last_player_position = (0, 0, 0)  # Para verificar movimento do jogador

def generate_blocks(player_position):
    global last_player_position

    # Verifica se o jogador se moveu significativamente
    if (abs(player_position.x - last_player_position[0]) < 1 and
            abs(player_position.z - last_player_position[2]) < 1):
        return

    last_player_position = (player_position.x, player_position.y, player_position.z)

    start_x = int(player_position.x) - chunk_size
    end_x = int(player_position.x) + chunk_size
    start_z = int(player_position.z) - chunk_size
    end_z = int(player_position.z) + chunk_size

    # Gerar blocos apenas nas novas posições
    for x in range(start_x, end_x + 1):
        for z in range(start_z, end_z + 1):
            # Verifica se a posição já tem um bloco
            if (x, z) not in blocks:  # Apenas gera se não existir
                if textures:  # Verifica se a lista de texturas não está vazia
                    texture_name = choice(list(textures.keys()))
                    block = Entity(model='cube', position=(x, 0, z), texture=textures[texture_name], scale=(1, 1, 1))
                    block.collider = 'box'  # Adiciona um colisor a cada bloco
                    blocks[(x, z)] = block  # Armazena o bloco no dicionário
                    print(f"Block generated at {(x, 0, z)} with texture '{texture_name}'")  # Depuração
            else:
                # Se o bloco já existe, atualize a textura se necessário
                block = blocks[(x, z)]
                if block.texture not in textures.values():  # Verifica se a textura é válida
                    new_texture_name = choice(list(textures.keys()))
                    block.texture = textures[new_texture_name]
                    print(f"Block at {(x, z)} updated with new texture '{new_texture_name}'")  # Depuração

    # Remover blocos fora do alcance
    for key in list(blocks.keys()):
        block = blocks[key]
        if abs(block.x - player_position.x) > chunk_size or abs(block.z - player_position.z) > chunk_size:
            destroy(block)  # Destroi o bloco
            del blocks[key]  # Remove o bloco do dicionário
            print(f"Block destroyed at {key}")  # Depuração

    # Limitar o número total de blocos
    if len(blocks) > max_blocks:
        oldest_block = next(iter(blocks))  # Pega o primeiro bloco no dicionário
        destroy(blocks[oldest_block])  # Destroi o bloco
        del blocks[oldest_block]  # Remove do dicionário
        print(f"Block limit reached, removed block at {oldest_block}")  # Depuração

def update():
    generate_blocks(player.position)

# Criar a luz
light = DirectionalLight(parent=scene, rotation=(45, -45, 0))
light.look_at((0, -1, 0))

# Criar o jogador
player = FirstPersonController()
player.position = (0, 1, 0)  # Posicionar acima do centro da área de blocos

# Adicionar um bloco de chão
ground_block = Entity(model='plane', position=(0, 0, 0), texture='ground', scale=(20, 1, 20))
ground_block.collider = 'box'

# Gera os blocos iniciais
generate_blocks(player.position)

app.run()
