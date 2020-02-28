import time

import numpy as np
import cv2
import multiprocessing as mp

colorir = (0, 255, 255)  # amarelo


class point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def new_zero(self):
        return point(0, 0)

    def to_array(self):
        return [self.x, self.y]

    def copy(self, pointn):
        self.x = pointn.x
        self.y = pointn.y
    def debug(self):
        return ("x:"+str(self.x)+"y:"+str(self.y))

class triangle:
    # import point
    left_point = point.new_zero(point)  # ponto esquerdo do triangulo
    right_point = point.new_zero(point)  # ponto direito do triangulo
    center_point = point.new_zero(point)  # ponto central do triangulo

    def __init__(self, left: point, right: point, center: point):  # função de preenchimento do triangulo
        self.left_point = left
        self.right_point = right
        self.center_point = center

    def to_array(self):
        return [self.left_point, self.right_point, self.center_point]

    def to_int_array(self):
        return [self.left_point.to_array(), self.right_point.to_array(), self.center_point.to_array()]
    def debug(self):
        print("left_point:"+str(self.left_point.debug())+"right_point:"+str(self.right_point.debug())+"center_point:"+str(self.center_point.debug()))

class square:
    # import point
    inf_esquerdo = point.new_zero(point)  # ponto inferior esquerdo do quadrado
    inf_direito = point.new_zero(point)  # ponto inferior direito do quadrado
    sup_esquerdo = point.new_zero(point)  # ponto superior esquerdo do quadrado
    sup_direito = point.new_zero(point)  # ponto superior direito do quadrado

    def __init__(self, inf_esquerdo_new: point, inf_direito_new: point, sup_esquerdo_new: point,
                 sup_direito_new: point):  # create_from_points
        self.inf_esquerdo = inf_esquerdo_new
        self.inf_direito = inf_direito_new
        self.sup_esquerdo = sup_esquerdo_new
        self.sup_direito = sup_direito_new

    def create_from_size(size):  # create from size
        novo_quadrado = square(point(0, 0), point(size, 0), point(0, size), point(size, size))
        novo_quadrado.debug()
        return novo_quadrado

    def to_array(self):  # get all the points from the square
        return [self.inf_esquerdo, self.inf_direito, self.sup_esquerdo, self.sup_direito]

    def to_int_array(self):  # get all values from each point into square
        return [self.inf_esquerdo.to_array(), self.inf_direito.to_array(), self.sup_esquerdo.to_array(),
                self.sup_direito.to_array()]
    def debug(self):
        print("sup_esquerdo"+str(self.sup_esquerdo.debug())+"sup_direito"+str(self.sup_direito.debug())+"inf_esquerdo"+str(self.inf_esquerdo.debug())+"inf_direito"+str(self.inf_direito.debug()))


class sierpinski_sequencial:  # class to work with the sierpinski triangle fractal
    def __init__(self):
        self.pool = mp.Pool(mp.cpu_count())
    def sierpinski_triangles_creator(self,triangle_original: triangle):  # primeira posicao=x,segunda posicao = y
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
        new_tri = np.array(
            [triangle_1.left_point.to_array(), triangle_1.right_point.to_array(), triangle_1.center_point.to_array(),
             triangle_1.left_point.to_array()], np.int32)
        new_tri = new_tri.reshape((-1, 1, 2))
        img = cv2.polylines(img, [new_tri], False, colorir, 3)
        return img

    def draw_all_triangles_from_list(self, img, triangle_list):
        for i in triangle_list:
            img = self.draw_triangle(img, i)
        return img

    def add_depth_from_triangle(self, triangle_list):  # add three triangles inside each triangle from list
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
        triangle_list = self.sierpinski_triangles_creator(self.get_triangle_from_square(square.create_from_size(size)))
        for i in range(0, depth):
            triangle_list = self.add_depth_triangle(triangle_list)

        return triangle_list

    def create_depths_from_triangle(self, triangle: triangle, depth):
        triangle_list = self.sierpinski_triangles_creator(triangle)
        for i in range(0, depth):
            triangle_list = self.add_depth_from_triangle(triangle_list)
        return triangle_list

    def generate_baseimage(self,size):
        new_img = np.ones((size, size, 3))
        return new_img

    def get_triangle_from_square(self,square: square):
        new_triangle = triangle(square.inf_esquerdo, square.inf_direito,
                                point((square.sup_esquerdo.x + square.sup_direito.x) / 2, (square.sup_esquerdo.y)))
        return new_triangle

    def get_square_from_triangle(self,triangle: triangle):
        new_square = square(triangle.left_point, triangle.right_point,
                            point(triangle.left_point.x, triangle.center_point.y),
                            point(triangle.right_point.x, triangle.center_point.y))
        return new_square

    def show_img_debug(self, size, depth):  # mostra imagem a partir do algoritimo de
        list_triangles = self.create_depths_from_triangle(self.get_triangle_from_square(square.create_from_size(size)),
                                                          depth)
        self.debug_triangle_list(list_triangles)
        imagem_branco = self.generate_baseimage(size)
        print("white generated")
        imagem = self.draw_all_triangles_from_list(sierpinski_sequencial, imagem_branco, list_triangles)
        print("image generated")
        cv2.imshow("test", imagem)  # working parcially

    def show_img(self, size, depth):  # mostra imagem a partir do algoritimo de
        imagem_branco = self.generate_baseimage(size)
        print("imagem_branco")
        list_triangles = self.create_depths_from_triangle(self.get_triangle_from_square(square.create_from_size(size)),depth)

        print("lista gerada")
        imagem = self.draw_all_triangles_from_list( imagem_branco, list_triangles)
        print("imagem pronta")
        cv2.imshow("test", imagem)  # testing
        cv2.waitKey()

    def save_img(self, name, size, depth,mostrar=True):  # mostra imagem a partir do algoritimo de
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
        for j in triangulo.to_int_array():
            print(j)
        print("fim")

    def debug_triangle_list(self, triangle_list: triangle):
        loop = 1
        for i in triangle_list:
            print("triangulo " + str(loop))
            self.debug_triangle(i)
            loop += 1

    def debug_triangle_list_generate_son(self, triangle_list: triangle):
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


# para testar a exibição inicial

tamanho=5000
profundidade=6
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
for profundidade in range(0,11):
    sierpinski.save_img("sierpinsky_"+str(profundidade),tamanho, profundidade,mostrar=False)  # testing
