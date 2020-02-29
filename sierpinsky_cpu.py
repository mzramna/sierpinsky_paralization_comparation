# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 14:17:39 2018

@author: migue
"""

import numpy as np
import cv2
from numba import jit, float32
from modelagem_comum import square,triangle,point

colorir = (0, 255, 255)  # amarelo


class sierpinski_CPU:  # class to work with the sierpinski triangle fractal
    @jit('void(float32,float32,float32,float32,float32,float32)', target='cpu', parallel=True)
    def sierpinski_triangles_creator(self,left_point_x, left_point_y, right_point_x, right_point_y, center_point_x,
                                     center_point_y):
        largura_total = float32(0.0)
        largura_total = float32(right_point_x - left_point_x)
        largura_filho = largura_total / 2
        distancia_centro_filho = largura_filho / 2
        altura_base = left_point_y
        altura_total = center_point_y - altura_base
        altura_filho = altura_total / 2

        triangle_1 = np.array([  # triangulo esquerdo
            left_point_x, left_point_y,  # ponto esquerdo
            left_point_x + largura_filho, altura_base  # ponto direito
            , left_point_x + distancia_centro_filho, altura_base + altura_filho  # ponto central
        ], dtype=np.float32)

        triangle_2 = np.array([  # triangulo direito
            left_point_x + largura_filho, altura_base,  # ponto esquerdo
            right_point_x, right_point_y,  # ponto direito
            center_point_x + distancia_centro_filho, altura_base + altura_filho  # ponto central
        ], dtype=np.float32)

        triangle_3 = np.array([  # triangulo central
            left_point_x + distancia_centro_filho, altura_base + altura_filho,  # ponto esquerdo
            center_point_x + distancia_centro_filho, altura_base + altura_filho,  # ponto direito
            center_point_x, center_point_y  # ponto superior
        ], dtype=np.float32)

        return np.array([triangle_1, triangle_2, triangle_3], dtype=np.float32)

    def draw_triangle(self,img, triangle_1):  # draw the triangle into the input image and return the ploted image
        new_tri = np.array(
            [[triangle_1[0], triangle_1[1]], [triangle_1[2], triangle_1[3]], [triangle_1[4], triangle_1[5]],
             [triangle_1[0], triangle_1[1]]], np.float32)
        new_tri = new_tri.reshape((-1, 1, 2))
        img = cv2.polylines(img, [new_tri], False, colorir, 3)
        return img

    def draw_all_triangles_from_list(self, img, triangle_list):
        for i in triangle_list:
            img = self.draw_triangle(img, i)
        return img

    @jit('void(object,float32[:])', target='cpu', parallel=True)
    def add_depth_from_triangle(self, triangle_list):  # add three triangles inside each triangle from list
        new_triangle_list = []
        for triangle_1 in triangle_list:
            # print(triangle.to_int_array())
            new_triangles = self.sierpinski_triangles_creator(triangle_1[0], triangle_1[1], triangle_1[2],
                                                              triangle_1[3], triangle_1[4], triangle_1[5])
            # print(new_triangles)
            for ntriangles in new_triangles:
                # print(ntriangles.to_int_array())
                new_triangle_list.append(ntriangles)
        return new_triangle_list

    @jit('void(object,float32[:],int32)', target='cpu', parallel=True)
    def create_depths_from_triangle(self, triangle_1, depth):
        triangle_list = []
        triangle_list = self.sierpinski_triangles_creator(triangle_1[0], triangle_1[1], triangle_1[2], triangle_1[3],
                                                          triangle_1[4], triangle_1[5])
        for i in range(0, depth):
            triangle_list = np.array(self.add_depth_from_triangle(triangle_list), dtype=np.float32)
        return triangle_list

    def generate_baseimage(size):
        new_img = np.zeros((size, size, 3), dtype=np.float32)
        return new_img

    def create_triangle_from_size(size: float):
        new_triangle = np.array([0.0, 0.0, size, 0.0, size / 2, size], dtype=np.float32)
        return new_triangle

    def show_img_debug(self, size, depth):  # mostra imagem a partir do algoritimo de
        list_triangles = self.create_depths_from_triangle(self.create_triangle_from_size(size), depth)
        self.debug_triangle_list(list_triangles)
        imagem_branco = self.generate_baseimage(size)
        print("white generated")
        imagem = self.draw_all_triangles_from_list(imagem_branco, list_triangles)
        print("image generated")
        cv2.imshow("test", imagem)  # working parcially

    def show_img(self, size, depth):  # mostra imagem a partir do algoritimo de
        imagem_branco = self.generate_baseimage(size)
        print("imagem_branco")
        triangle = self.create_triangle_from_size(size)
        list_triangles = self.create_depths_from_triangle(triangle, depth)
        print("lista gerada")
        imagem = self.draw_all_triangles_from_list(imagem_branco, list_triangles)
        print("imagem pronta")
        cv2.imshow("test", imagem)  # testing

    def save_img(self, name, size, depth):  # mostra imagem a partir do algoritimo de
        imagem_branco = self.generate_baseimage(size)
        print("imagem_branco")
        new_square = self.create_square_from_size(size)
        list_triangles = self.create_depths_from_triangle(self.get_triangle_from_square(new_square), depth)
        print("lista gerada")
        imagem = self.draw_all_triangles_from_list(imagem_branco, list_triangles)
        print("imagem pronta")
        cv2.imshow("./" + name + ".jpg", imagem)
        cv2.imwrite("./" + name + ".jpg", imagem)

    def debug_triangle(self,triangulo):
        for j in triangulo:
            print(j)
        print("fim")

    def debug_triangle_list(self, triangle_list):
        loop = 1
        for i in triangle_list:
            print("triangulo " + str(loop))
            self.debug_triangle(i)
            loop += 1

        #    def debug_triangle_list_generate_son(self,triangle_list):
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
cv2.imshow("test", sierpinski_CPU.draw_triangle(sierpinski_CPU.generate_baseimage(25),
                                                sierpinski_CPU.get_triangle_from_square(
                                                    square.create_from_size(25))))  # working
# cv2.imshow("test",self.draw_triangle_from_square(self.generate_baseimage(400),square.create_from_size(400)))#working
# new_triangles=self.sierpinski_triangles_creator(self.get_triangle_from_square(square.create_from_size(200)))
# for i in new_triangles:
#    for j in i.to_int_array():
#        print(j)
#    print("fim")
# self.debug_triangle_list_generate_son(new_triangles)#working
sierpinski_CPU.show_img(1000, 6)  # testing
cv2.waitKey()
