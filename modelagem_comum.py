
class point:
    """
    classe equivalente aos pontos de um grafico 2d
    :param x: coordenada x
    :param y: coordenada y
    """
    x = 0
    y = 0

    def __init__(self, x, y):
        """
        classe equivalente aos pontos de um grafico 2d
        :param x: coordenada x
        :param y: coordenada y
        """
        self.x = x
        self.y = y

    def new_zero(self):
        """
        cria um novo ponto zerado
        :return: novo ponto
        """
        return point(0, 0)

    def to_array(self):
        """
        retorna um array com os pontos,sendo [x,y]
        :return: [x,y]
        """
        return [self.x, self.y]

    def copy(self, pointn):
        """
        copia um ponto
        :param pointn: ponto que será copiado
        :return: uma copia do ponto passado
        """
        self.x = pointn.x
        self.y = pointn.y
    def debug(self):
        """
        debug do ponto
        :return: print(x:'valueofx'y:'valueofy')
        """
        return ("x:"+str(self.x)+"y:"+str(self.y))

class triangle:
    """
    classe representando um triangulo
    :param left_point: ponto esquerdo do triangulo
    :param right_point: ponto direito do triangulo
    :param center_point: ponto central do triangulo
    """
    # import point
    left_point = point.new_zero(point)  # ponto esquerdo do triangulo
    right_point = point.new_zero(point)  # ponto direito do triangulo
    center_point = point.new_zero(point)  # ponto central do triangulo

    def __init__(self, left: point, right: point, center: point):  # função de preenchimento do triangulo
        """
        gera um triangulo a partir de 3 pontos
        :param left_point: ponto esquerdo do triangulo
        :param right_point: ponto direito do triangulo
        :param center_point: ponto central do triangulo
        """
        self.left_point = left
        self.right_point = right
        self.center_point = center

    def to_array(self):
        """
        retorna um array de pontos com os pontos do triangulo
        :return:   [left_point, right_point, center_point]
        """
        return [self.left_point, self.right_point, self.center_point]

    def to_int_array(self):
        """
        retorna uma matriz com os valores das coordenadas de cada ponto dentro de um array
        :return: [left_point[x,y], right_point[x,y], center_point[x,y]]
        """
        return [self.left_point.to_array(), self.right_point.to_array(), self.center_point.to_array()]
    def debug(self):
        """
        debug dos pontos do triangulo usando a função de debug de point
        :return:   print("left_point:"+str(self.left_point.debug())+"right_point:"+str(self.right_point.debug())+"center_point:"+str(self.center_point.debug()))
        """
        print("left_point:"+str(self.left_point.debug())+"right_point:"+str(self.right_point.debug())+"center_point:"+str(self.center_point.debug()))

class square:
    """
       função que representa um quadrado
       :param inf_esquerdo: ponto inferior esquerdo do quadrado
       :param inf_direito: ponto inferior direito do quadrado
       :param sup_esquerdo: ponto superior esquerdo do quadrado
       :param sup_direito: ponto superior direito do quadrado
           """
    # import point
    inf_esquerdo = point.new_zero(point)  # ponto inferior esquerdo do quadrado
    inf_direito = point.new_zero(point)  # ponto inferior direito do quadrado
    sup_esquerdo = point.new_zero(point)  # ponto superior esquerdo do quadrado
    sup_direito = point.new_zero(point)  # ponto superior direito do quadrado

    def __init__(self, inf_esquerdo_new: point, inf_direito_new: point, sup_esquerdo_new: point,
                 sup_direito_new: point):  # create_from_points
        """
        gera um quadrado a partir de 4 pontos
        :param inf_esquerdo_new: ponto inferior esquerdo do quadrado
        :param inf_direito_new: ponto inferior direito do quadrado
        :param sup_esquerdo_new: ponto superior esquerdo do quadrado
        :param sup_direito_new: ponto superior direito do quadrado
        """
        self.inf_esquerdo = inf_esquerdo_new
        self.inf_direito = inf_direito_new
        self.sup_esquerdo = sup_esquerdo_new
        self.sup_direito = sup_direito_new

    def create_from_size(self,size):  # create from size
        """
        cria um quadrado a partir do tamanho do lado suponto seus pontos de origem sendo 0,0
        :param size: lado do quadrado
        :return: um quadrado novo
        """
        novo_quadrado = square(point(0, 0), point(size, 0), point(0, size), point(size, size))
        novo_quadrado.debug()
        return novo_quadrado

    def to_array(self):  # get all the points from the square
        """
        retorna um array de pontos com os pontos do quadrado
        :return: [inf_esquerdo, inf_direito, sup_esquerdo, sup_direito]
        """
        return [self.inf_esquerdo, self.inf_direito, self.sup_esquerdo, self.sup_direito]

    def to_int_array(self):  # get all values from each point into square
        """
        retorna uma matriz com os valores das coordenadas de cada ponto dentro de um array
        :return:  [inf_esquerdo[x,y], inf_direito[x,y], sup_esquerdo[x,y], sup_direito[x,y]]
        """
        return [self.inf_esquerdo.to_array(), self.inf_direito.to_array(), self.sup_esquerdo.to_array(),
                self.sup_direito.to_array()]
    def debug(self):
        """
        debug dos pontos do triangulo usando a função de debug de point
        :return: print("sup_esquerdo"+str(self.sup_esquerdo.debug())+"sup_direito"+str(self.sup_direito.debug())+"inf_esquerdo"+str(self.inf_esquerdo.debug())+"inf_direito"+str(self.inf_direito.debug()))
        """
        print("sup_esquerdo"+str(self.sup_esquerdo.debug())+"sup_direito"+str(self.sup_direito.debug())+"inf_esquerdo"+str(self.inf_esquerdo.debug())+"inf_direito"+str(self.inf_direito.debug()))

