class Expr:
	pass


class Binary(Expr):
	def __init__(self, left, operator, right):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visit_Binary_expr(self)


class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visit_Grouping_expr(self)


class Literal(Expr):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visit_Literal_expr(self)


class Unary(Expr):
	def __init__(self, operator, right):
		self.operator = operator
		self.right = right

	def accept(self, visitor):
		return visitor.visit_Unary_expr(self)


class Conditional(Expr):
	def __init__(self, condition, then_jump, else_jump):
		self.condition = condition
		self.then_jump = then_jump
		self.else_jump = else_jump

	def accept(self, visitor):
		return visitor.visit_Conditional_expr(self)
