
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

