import time

import imageio as imageio
import numpy as np
import cv2
from modelagem_comum import square,triangle,point
colorir = (0, 255, 255)  # amarelo




class sierpinski_sequencial:  # class to work with the sierpinski triangle fractal
    """classe onde sera executado o processamento do fractal de sierpinsky"""
    def sierpinski_triangles_creator(self,triangle_original: triangle):  # primeira posicao=x,segunda posicao = y
        """
        função que gera os triangulos filhos de um triangulo dado posteriormente,el gera mais uma camada da profundidade de pontos,apenas retorno um array com os 3 triangulos resultantes,devido ao modo de funcionamento
        do fractal só com isso é possivel de se criar o triangulo que o originou
        :param triangle_original: um triangle
        :return: array de  3 triangle
        """
        [left_point, right_point, center_point] = [triangle_original.left_point, triangle_original.right_point,
                                                   triangle_original.center_point]
        largura_total = (right_point.x - left_point.x)
        largura_filho = largura_total / 2
        distancia_centro_filho = largura_filho / 2
        altura_base = left_point.y
        altura_total = (center_point.y - altura_base)
        altura_filho = altura_total / 2

        triangle_1 = triangle(  # triangulo esquerdo
            point(left_point.x, left_point.y),  # ponto esquerdo
            point(left_point.x + largura_filho, altura_base)  # ponto direito
            , point(left_point.x + distancia_centro_filho, altura_base + altura_filho)  # ponto central
        )

        triangle_2 = triangle(  # triangulo direito
            point(left_point.x + largura_filho, altura_base),  # ponto esquerdo
            point(right_point.x, right_point.y),  # ponto direito
            point(center_point.x + distancia_centro_filho, altura_base + altura_filho)  # ponto central
        )

        triangle_3 = triangle(  # triangulo central
            point(left_point.x + distancia_centro_filho, altura_base + altura_filho),  # ponto esquerdo
            point(center_point.x + distancia_centro_filho, altura_base + altura_filho),  # ponto direito
            point(center_point.x, center_point.y)  # ponto superior
        )

        return [triangle_1, triangle_2, triangle_3]

    def draw_triangle(self,img, triangle_1: triangle):  # draw the triangle into the input image and return the ploted image
        """
        desenha um triangulo na imagem base passada para a funcao
        :param img: imagem base em cima da qual será aplicado o fractal
        :param triangle_1: desenha o triangulo dentro da imagem,usando os dados da classe triangle para isso
        :return: imagem com triangulo inserido nela
        """
        new_tri = np.array(
            [triangle_1.left_point.to_array(), triangle_1.right_point.to_array(), triangle_1.center_point.to_array(),
             triangle_1.left_point.to_array()], np.int32)
        new_tri = new_tri.reshape((-1, 1, 2))
        img = cv2.polylines(img, [new_tri], False, colorir, 3)
        return img

    def draw_all_triangles_from_list(self, img, triangle_list):
        """
        desenha todos os triangulos de uma lista de triangulos na imagem dada
        :param img: imagem base em cima da qual será aplicado o fractal
        :param triangle_list: lista de objetos da classe triangle
        :return: imagem com os triangulos desenhados
        """
        for i in triangle_list:
            img = self.draw_triangle(img, i)
        return img

    def add_depth_from_triangle(self, triangle_list):  # add three triangles inside each triangle from list
        """
        adiciona uma nova camada de profundidade ao fractal ao chamar a função sierpinski_triangles_creator para cada triangulo de um array de triangulos
        :param triangle_list:
        :return: novo array com os novos triangulos
        """
        new_triangle_list = []
        for triangle in triangle_list:
            # print(triangle.to_int_array())
            new_triangles = self.sierpinski_triangles_creator(triangle)
            # print(new_triangles)
            for ntriangles in new_triangles:
                # print(ntriangles.to_int_array())
                new_triangle_list.append(ntriangles)
        return new_triangle_list

    def create_depths_from_size(self, size, depth):
        """
        cria o fractal calculando automaticamente todos os triangulos a partir das dimensões e da profundidade desejada
        :param size: dimensões da imagem de saida,que sera um quadrado
        :param depth: quantidade de camadas de proifundidade do fractal
        :return: lista de triangulos calculados a partir dos parametros passados
        """
        triangle_list = self.sierpinski_triangles_creator(self.get_triangle_from_square(square.create_from_size(size)))
        for i in range(0, depth):
            triangle_list = self.add_depth_triangle(triangle_list)

        return triangle_list

    def create_depths_from_triangle(self, triangle: triangle, depth):
        """
        cria as camadas de profundidade do triangulo,gerando a quantidade de camas igual a variavel depth
        :param triangle: objeto primario do tipo triangle
        :param depth: numero de camadas de profundidade
        :return: array de triangulos novos gerados a partir de um triangulo dado
        """
        triangle_list = self.sierpinski_triangles_creator(triangle)
        for i in range(0, depth):
            triangle_list = self.add_depth_from_triangle(triangle_list)
        return triangle_list

    def generate_baseimage(self,size):
        """
        gera uma nova imagem em branco de formato quadrado e lados iguais a dimensão passada
        :param size: tamanho do lado do quadrado
        :return: uma nova imagem em branco
        """
        new_img = np.ones((size, size, 3))
        return new_img

    def get_triangle_from_square(self,square: square):
        """
        gera um triangulo a partir de um quadrado
        :param square: quadrado do qual um triangulo deve ser gerado
        :return: um triangulo isóceles com lado igual ao lado do quadrado
        """
        new_triangle = triangle(square.inf_esquerdo, square.inf_direito,
                                point((square.sup_esquerdo.x + square.sup_direito.x) / 2, (square.sup_esquerdo.y)))
        return new_triangle

    def get_square_from_triangle(self,triangle: triangle):
        """
        gera um quadrado a partir de um triangulo isóceles com lado igual ao lado do triangulo
        :param triangle: triangulo isoceles
        :return: quadrado
        """
        new_square = square(triangle.left_point, triangle.right_point,
                            point(triangle.left_point.x, triangle.center_point.y),
                            point(triangle.right_point.x, triangle.center_point.y))
        return new_square

    def show_img_debug(self, size, depth):  # mostra imagem a partir do algoritimo de
        """
        mostra a imagem com dados de debug
        :param size: tamanho da imagem que será gerada usando a funcao generate_baseimage
        :param depth: profundidade do fractal usado para debug
        :return: print de debug e imagem nova com fractal
        """
        list_triangles = self.create_depths_from_triangle(self.get_triangle_from_square(square.create_from_size(size)),
                                                          depth)
        self.debug_triangle_list(list_triangles)
        imagem_branco = self.generate_baseimage(size)
        print("white generated")
        imagem = self.draw_all_triangles_from_list(sierpinski_sequencial, imagem_branco, list_triangles)
        print("image generated")
        cv2.imshow("test", imagem)  # working parcially

    def show_img(self, size, depth):  # mostra imagem a partir do algoritimo de
        """
        mostra imagem fractal gerada a partir de um quadrado de lado passado pelo parametro e profundidade igual a variavel depth
        :param size: lado da imagem de saida
        :param depth: profundidade da imagem gerada
        :return:mostra a imagem gerada
        """
        imagem_branco = self.generate_baseimage(size)
        print("imagem_branco")
        list_triangles = self.create_depths_from_triangle(self.get_triangle_from_square(square.create_from_size(size)),
                                                          depth)
        print("lista gerada")
        imagem = self.draw_all_triangles_from_list( imagem_branco, list_triangles)
        print("imagem pronta")
        cv2.imshow("test", imagem)  # testing
        cv2.waitKey()

    def save_img(self, name, size, depth,mostrar=True):  # mostra imagem a partir do algoritimo de
        """
        gera uma imagem e salva
        :param name:nome do arquivo de saida,será do tipo jpg
        :param size: tamanho do lado da imagem
        :param depth: profundidade do fractal
        :param mostrar:se deve exibir a imagem após gerar
        :return:arquivo de saida com o fractal gerado
        """
        imagem_branco = self.generate_baseimage(size)
        print("imagem_branco")
        list_triangles = self.create_depths_from_triangle(self.get_triangle_from_square(square.create_from_size(size)),
                                                          depth)
        print("lista gerada")
        imagem = self.draw_all_triangles_from_list(imagem_branco, list_triangles)
        print("imagem pronta")
        cv2.imwrite("./" + name + ".jpg", imagem)
        print("imagem salva")
        if mostrar:
            cv2.imshow("./" + name + ".jpg", imagem)
            cv2.waitKey()

    def debug_triangle(self,triangulo: triangle):
        """
        exibe os dados de um triangulo para debug
        :param triangulo: triangulo que será debugado
        :return:debug do triangulo
        """
        triangulo.debug()

    def debug_triangle_list(self, triangle_list: triangle):
        """
        debuga todos os triangulos de uma lista de triangulos
        :param triangle_list: lista dos triangulos que será debugada
        :return:print de todos os dados do triangulo
        """
        loop = 1
        for i in triangle_list:
            print("triangulo " + str(loop))
            self.debug_triangle(i)
            loop += 1

    def debug_triangle_list_generate_son(self, triangle_list: triangle):
        """
        debuga todos os triangulos gerados usango o sierpinski_triangles_creator
        :param triangle_list: lista dos triangulos originais
        :return: debug dos filhos criados
        """
        loop = 1
        for i in triangle_list:
            print("triangulo " + str(loop))
            self.debug_triangle(i)
            loop2 = 1
            lista_filhos = self.sierpinski_triangles_creator(i)
            for j in lista_filhos:
                print("filho " + str(loop2) + " do triangulo " + str(loop))
                self.debug_triangle(j)
                loop2 += 1
            print("\n\n")
            loop += 1

    def create_gif(self,tamanho, profundidade_max, frames_renderizador=None, name=None, duration=None):
        """
        "cria o gif a partir da execução da função draw all triangles from list
        :param tamanho: dimensoes do quadrado de tamanho do gif
        :param profundiade_max: total de vezes que a recursão deve ser executada
        :param frames_renderizador:podem ser passados todos os frames do gif usando o array , util quando a função de gif for ser usada multiplas vezes para economizar processamento ou se as dimensões nao forem em quadrado
        :param name:nome do arquivo gif que sera salvo
        :param duration: tempo que cada frame sera exibido , dado em segundos
        :return: arquivo gif salvo no lugar definido pelo parametro name
        """
        frames = []
        sierpinski = sierpinski_sequencial()
        if duration == None:
            duration = 0.4
        if frames_renderizador == None:
            for profundidade in range(0, profundidade_max):
                frames.append(self.draw_all_triangles_from_list(self.generate_baseimage(tamanho),
                                                                      self.create_depths_from_triangle(
                                                                          self.get_triangle_from_square(
                                                                              square.create_from_size(tamanho)),
                                                                          profundidade)).astype(np.uint8))
        else:
            frames = frames_renderizador
        if name == None:
            name = "gif_automatica_0_" + str(profundidade_max) + "_delay" + str(delay)
        imageio.mimsave(name + ".gif", frames, format='GIF', duration=duration)
        print("arquivo " + name + " criado com sucesso")
# para testar a exibição inicial
tamanho=10000
profundidade_max=7
sierpinski=sierpinski_sequencial()
#cv2.imshow("test", sierpinski.draw_triangle(sierpinski.generate_baseimage(tamanho),sierpinski.get_triangle_from_square(square.create_from_size(tamanho))))  # working
#cv2.waitKey()
#cv2.imshow("test",sierpinski.draw_triangle(sierpinski.generate_baseimage(400),sierpinski.get_triangle_from_square(square.create_from_size(400))))#working
#time.sleep(3)
# new_triangles=self.sierpinski_triangles_creator(self.get_triangle_from_square(square.create_from_size(200)))
# for i in new_triangles:
#    for j in i.to_int_array():
#        print(j)
#    print("fim")
# sierpinski_sequencial.debug_triangle_list_generate_son(new_triangles)#working
# for profundidade in range(0,11):
#     sierpinski.save_img("sierpinsky_"+str(profundidade),tamanho, profundidade,mostrar=False)  # testing
frames=[]
for profundidade in range(0, profundidade_max):
    frames.append(sierpinski.draw_all_triangles_from_list(sierpinski.generate_baseimage(tamanho),
                                                          sierpinski.create_depths_from_triangle(
                                                              sierpinski.get_triangle_from_square(
                                                                  square.create_from_size(tamanho)),
                                                              profundidade)).astype(np.uint8))
for i in range(4,11):
    delay=0+i/10
    sierpinski.create_gif(tamanho=tamanho,profundidade_max=profundidade_max,duration=delay,name="gif_automatica_0_"+str(profundidade_max)+"_delay"+str(delay),frames_renderizador=frames)