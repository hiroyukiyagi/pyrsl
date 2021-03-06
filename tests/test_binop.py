# encoding: utf-8
# Copyright (C) 2015 John Törnblom

from utils import RSLTestCase
from utils import evaluate_docstring


class TestBinaryOperation(RSLTestCase):

    @evaluate_docstring
    def test_plus(self, rc):
        '.exit 1 + 1'
        self.assertEqual(2, rc)
        
    @evaluate_docstring
    def test_minus(self, rc):
        '.exit 1 - 1'
        self.assertEqual(0, rc)

    @evaluate_docstring
    def test_minus_with_unary_minus(self, rc):
        '.exit 1 - -1'
        self.assertEqual(2, rc)
        
    @evaluate_docstring
    def test_multiplication(self, rc):
        '.exit 2 * 2'
        self.assertEqual(4, rc)
        
    @evaluate_docstring
    def test_division(self, rc):
        '.exit 10 / 2'
        self.assertEqual(5, rc)
        
    @evaluate_docstring
    def test_less_true(self, rc):
        '.exit 0 < 1'
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_less_false(self, rc):
        '.exit 0 < 0'
        self.assertFalse(rc)
        
    @evaluate_docstring
    def test_less_equal_true(self, rc):
        '.exit 1 <= 1'
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_less_equal_false(self, rc):
        '.exit 2 <= 1'
        self.assertFalse(rc)
        
    @evaluate_docstring
    def test_not_equal_false(self, rc):
        '.exit 1 != 1'
        self.assertFalse(rc)
    
    @evaluate_docstring
    def test_great_equal_false(self, rc):
        '.exit 1 >= 2'
        self.assertFalse(rc)
        
    @evaluate_docstring
    def test_great_equal_true(self, rc):
        '.exit 3 >= 2'
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_not_equal_true(self, rc):
        '.exit 0 != 1'
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_equal_false(self, rc):
        '.exit 0 == 1'
        self.assertFalse(rc)
        
    @evaluate_docstring
    def test_equal_true(self, rc):
        '.exit 1 == 1'
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_grouped(self, rc):
        '''
        .assign x = (1 + 1)
        .exit x
        '''
        self.assertEqual(2, rc)
        
    @evaluate_docstring
    def test_chained(self, rc):
        '''
        .assign x = (1 + 1) + 1
        .exit x
        '''
        self.assertEqual(3, rc)

    @evaluate_docstring
    def test_chained_with_unary(self, rc):
        '''
        .assign x = not (1 == 1)
        .exit x
        '''
        self.assertEqual(False, rc)

    @evaluate_docstring
    def test_and_true(self, rc):
        '''
        .exit True and True
        '''
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_and_false(self, rc):
        '''
        .exit True and False
        '''
        self.assertFalse(rc)
        
    @evaluate_docstring
    def test_or_true(self, rc):
        '''
        .exit True or False
        '''
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_or_false(self, rc):
        '''
        .exit False or False
        '''
        self.assertFalse(rc)
        
    @evaluate_docstring
    def test_or_without_spaces(self, rc):
        '''
        .assign x = (True)or(False)
        .exit x
        '''
        self.assertTrue(rc)
        
    @evaluate_docstring
    def test_and_without_spaces(self, rc):
        '''
        .assign x = (True)AND(True)
        .exit x
        '''
        self.assertTrue(rc)
        
    def test_pipe(self):
        self.metamodel.define_class('A', [('Name', 'string')])

        text = '''
        .create object instance a1 of A
        .create object instance a2 of A
        .create object instance a3 of A
        .assign a1.Name = "A1"
        .assign a2.Name = "A2"
        .assign a3.Name = "A3"
        
        .select any a1_set from instances of A where (selected.Name == "A1")
        .select any a2_set from instances of A where (selected.Name == "A2")
        
        .assign a_set = a1_set | a2_set
        .exit cardinality a_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(2, rc)
    
        text = '''
        
        .select any a1_set from instances of A where (selected.Name == "A1")
        .select many a_set from instances of A
        
        .assign a_set = a1_set | a_set
        .exit cardinality a_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(3, rc)
        
    def test_ampesand(self):
        self.metamodel.define_class('A', [('Name', 'string')])

        text = '''
        .create object instance a1 of A
        .create object instance a2 of A
        .create object instance a3 of A
        .assign a1.Name = "A1"
        .assign a2.Name = "A2"
        .assign a3.Name = "A3"
        
        .select any a1_set from instances of A where (selected.Name == "A1")
        .select any a2_set from instances of A where (selected.Name == "A2")
        
        .assign a_set = a1_set & a2_set
        .exit cardinality a_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(0, rc)
    
        text = '''
        .select many not_a1_set from instances of A where (selected.Name != "A1")
        .select many not_a2_set from instances of A where (selected.Name != "A2")
        
        .assign a3_set = not_a1_set & not_a2_set
        .exit cardinality a3_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(1, rc)
        
    def test_instance_plus_instance(self):
        self.metamodel.define_class('A', [('Name', 'string')])

        text = '''
        .create object instance a1 of A
        .create object instance a2 of A
        .assign a1.Name = "A1"
        .assign a2.Name = "A2"
        
        .assign a_set = a1 + a2
        .exit cardinality a_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(2, rc)
        
    def test_instance_minus_instance(self):
        self.metamodel.define_class('A', [('Name', 'string')])

        text = '''
        .create object instance a1 of A
        .create object instance a2 of A
        .assign a1.Name = "A1"
        .assign a2.Name = "A2"
        
        .assign a_set = a1 - a2
        .exit cardinality a_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(1, rc)
        
    def test_instance_minus_same_instance(self):
        self.metamodel.define_class('A', [('Name', 'string')])

        text = '''
        .create object instance a1 of A
        .assign a1.Name = "A1"
        
        .assign a_set = a1 - a1
        .exit cardinality a_set
        '''
        rc = self.eval_text(text)
        self.assertEqual(0, rc)
        
