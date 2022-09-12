# Ahmed Ali (101181126)
# SYSC 2100 Lab 6/Assignment 1

# An implementation of ADT Polynomial that uses a singly-linked list as the
# underlying data structure.

# A polynomial consists of 0 or more terms, with each term consisting of a
# coefficient and an exponent. Coefficients are integers, and terms with zero
# coefficients are not stored in the linked list. Exponents are non-negative
# integers.

from typing import Any

__author__ = 'bailey'
__version__ = '1.00'
__date__ = 'February 21, 2022'

"""
History:
1.00 Feb. 21, 2022 - Initial release.
"""

class Polynomial:

    class TermNode:
        def __init__(self, coefficient: int, exponent: int) -> None:
            """Initialize this node to represent a polynomial term with the
            given coefficient and exponent.

            Raise ValueError if the coefficent is 0 or if the exponent
            is negative.
            """
            if coefficient == 0:
                raise ValueError("TermNode: zero coefficient")
            if exponent < 0:
                raise ValueError("TermNode: negative exponent")

            self.coeff = coefficient
            self.exp = exponent
            self.next = None

    def __init__(self, coefficient: int = None, exponent: int = 0) -> None:
        """Initialize this Polynomial with a single term constructed from the
        coefficient and exponent.

        If one argument is given, the term is a constant coefficient
        (the exponent is 0).
        If no arguments are given, the Polynomial has no terms.

        # Polynomial with no terms:
        >>> p = Polynomial()
        >>> print(p._head)
        None
        >>> print(p._tail)
        None

        # Polynomial with one term (a constant):
        >>> p = Polynomial(12)
        >>> p._head.coeff
        12
        >>> p._head.exp
        0
        >>> print(p._head.next)
        None

        # Polynomial with one term:
        >>> p = Polynomial(12, 2)
        >>> p._head.coeff
        12
        >>> p._head.exp
        2
        >>> print(p._head.next)
        None
        """
        # A polynomial is stored as a singly linked list. Each node stores
        # one term, with the nodes ordered in descending order, based on the
        # exponent. (The head node is the term with the highest exponent,
        # and the tail node is the term with the lowest exponent.)
        if coefficient is None and exponent == 0:
            self._head = None
        else:
            self._head = Polynomial.TermNode(coefficient, exponent)
        self._tail = self._head

    def __str__(self) -> str:
        """Return a string representation of this polynomial.

        # Polynomial with no terms:
        >>> p = Polynomial()
        >>> str(p)
        ''

        # Polynomial with one term (a constant):
        >>> p = Polynomial(12)
        >>> str(p)
        '12'

        # Polynomials with one term:
        >>> p = Polynomial(12, 1)
        >>> str(p)
        '12x'

        >>> p = Polynomial(12, 2)
        >>> str(p)
        '12x^2'

        # See __add__ for string representations of polynomials with
        # more than one term.
        """
        polyStr = ""
        if self._head is None:
            return polyStr
        node = self._head
        polyStr += str(node.coeff)
        if node.exp >= 1:
            polyStr += "x"
        if node.exp > 1:
            polyStr += "^" + str(node.exp)
        node = node.next
        while (node != None):
            if node.coeff > 0:
                polyStr += "+"
            polyStr += str(node.coeff)
            if node.exp >= 1:
                polyStr += "x"
            if node.exp > 1:
                polyStr += "^" + str(node.exp)
            node = node.next
        return polyStr

    def __repr__(self) -> str:
        """Return the same string as __str__."""
        return str(self)

    def degree(self) -> int:
        """Return this polynomial's degree.

        Raise ValueError if the polynomial has no terms.

        >>> p = Polynomial(12, 2)
        >>> p.degree()
        2
        """
        if self._head is not None:
            return self._head.exp
        return 0

    def evaluate(self, x: float) -> float:
        """Evaluate the polynomial at x and return the result.

        Raise ValueError if the polynomial has no terms.

        >>> p = Polynomial(12, 2)
        >>> p.evaluate(3)
        108.0
        """
        node = self._head
        result = 0
        while (node is not None):
            result += pow(x, node.exp) * node.coeff
            node = node.next
        return result

    def __add__(self, rhs: 'Polynomial') -> 'Polynomial':
        """ Return a new Polynomial containing the sum of this polynomial
        and rhs.

        Raise ValueError if either polynomial has no terms.

        >>> p1 = Polynomial(12, 2)
        >>> p2 = Polynomial(-3, 1)
        >>> p3 = Polynomial(7)
        >>> p1 + p2
        12x^2-3x

        >>> p1 + p3
        12x^2+7

        >>> p1 + p2 + p3  # Equivalent to (p1 + p2) + p3
        12x^2-3x+7

        >>> p2 = Polynomial(3, 1)
        >>> p1 + p2 + p3
        12x^2+3x+7
        """
        nodeSelf = self._head
        nodeRhs = rhs._head
        result = Polynomial()
        nodeResult = result._head

        while (nodeRhs != None or nodeSelf != None):
            if nodeSelf == None or nodeSelf.exp < nodeRhs.exp:
                if nodeResult == None:
                    result._head = Polynomial.TermNode(
                        nodeRhs.coeff, nodeRhs.exp)
                    nodeResult = result._head
                else:
                    nodeResult.next = Polynomial.TermNode(
                        nodeRhs.coeff, nodeRhs.exp)
                    nodeResult = nodeResult.next
                nodeRhs = nodeRhs.next
            elif nodeRhs == None or nodeSelf.exp > nodeRhs.exp:
                if nodeResult == None:
                    result._head = Polynomial.TermNode(
                        nodeSelf.coeff, nodeSelf.exp)
                    nodeResult = result._head
                else:
                    nodeResult.next = Polynomial.TermNode(
                        nodeSelf.coeff, nodeSelf.exp)
                    nodeResult = nodeResult.next
                nodeSelf = nodeSelf.next
            elif nodeSelf.exp == nodeRhs.exp:
                if nodeSelf.coeff + nodeRhs.coeff != 0:
                    if nodeResult == None:
                        result._head = Polynomial.TermNode(
                            nodeSelf.coeff + nodeRhs.coeff, nodeRhs.exp)
                        nodeResult = result._head
                    else:
                        nodeResult.next = Polynomial.TermNode(
                            nodeSelf.coeff + nodeRhs.coeff, nodeRhs.exp)
                        nodeResult = nodeResult.next
                nodeRhs = nodeRhs.next
                nodeSelf = nodeSelf.next
        return result

    def __mul__(self, rhs: 'Polynomial') -> 'Polynomial':
        """ Return a new Polynomial containing the product of this polynomial
        and rhs.

        Raise ValueError if either polynomial has no terms.

        >>> p1 = Polynomial(12, 2)
        >>> p2 = Polynomial(-3, 1)
        >>> p3 = Polynomial(7)
        >>> poly = p1 + p2 + p3
        >>> poly
        12x^2-3x+7

        >>> p4 = Polynomial(2, 1)
        >>> p4 * poly
        24x^3-6x^2+14x
        """
        nodeRhs = rhs._head
        result = Polynomial()

        while (nodeRhs != None):
            nodeSelf = self._head
            nodeResult = result._head
            while (nodeSelf != None):
                if nodeResult == None:
                    result._head = Polynomial.TermNode(
                        nodeSelf.coeff * nodeRhs.coeff, nodeSelf.exp + nodeRhs.exp)
                    nodeResult = result._head
                else:
                    expo = nodeSelf.exp + nodeRhs.exp
                    while (nodeResult != None and nodeResult.next != None and expo < nodeResult.next.exp):
                        nodeResult = nodeResult.next
                    if nodeResult.next != None and nodeResult.next.exp == expo:
                        coef = nodeSelf.coeff * nodeRhs.coeff + nodeResult.next.coeff
                        if coef != 0:
                            nodeResult.next = Polynomial.TermNode(coef, expo)
                        else:
                            nodeResult.next = nodeResult.next.next
                    else:
                        temp = nodeResult.next
                        nodeResult.next = Polynomial.TermNode(
                            nodeSelf.coeff * nodeRhs.coeff, expo)
                        nodeResult = nodeResult.next
                        nodeResult.next = temp
                nodeSelf = nodeSelf.next
            nodeRhs = nodeRhs.next
        return result


if __name__ == '__main__':
    poly = Polynomial(5, 2)  # Polynomial with term 5x^2
    print(poly)
    print(poly.degree())
    print(poly.evaluate(3))
    # assert poly.degree() == 2  # Polynomial's degree is 2
    #assert abs(poly.evaluate(3) - 45.0) < 0.0001
    poly = Polynomial(5)
    print(poly)
    print(poly.degree())
    print(poly.evaluate(3))
    poly = Polynomial(5, 1)
    print(poly)
    print(poly.degree())
    print(poly.evaluate(3))
    poly = Polynomial(5, 0)
    print(poly)
    print(poly.degree())
    print(poly.evaluate(3))
    poly = Polynomial()
    print(poly)
    print(poly.degree())
    print(poly.evaluate(3))

    p1 = Polynomial(12, 2)
    p2 = Polynomial(-3, 1)
    p3 = Polynomial(7)
    p12 = p1 + p2
    print(p12)
    p13 = p1 + p3
    p123 = p12 + p3  # Equivalent to (p1 + p2) + p3
    p2 = Polynomial(3, 1)
    p123 = p1 + p2 + p3
    p12mp123 = p12 * p123
    print(p12mp123)
