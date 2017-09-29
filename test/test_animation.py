import unittest
import sys

sys.path.append('..')
import animation


class AnimationTest(unittest.TestCase):

    def setUp(self):
        """SetUp un objet animation avec quelques frms"""
        self.a = animation.Animation()
        self.a.add_frm(0)
        self.a.add_frm(0)
        self.a.add_frm(0)
        self.a.clone_frm(0)

    def test_len(self):
        """test si len(a) correspond bien a len de l'attribut _film"""
        self.assertEqual(len(self.a), len(self.a._film))

    def test_getitem(self):
        """test si a[i] correspond bien a a._frms[a._film[i]]
        test si une erreur est bien levée si on cherche à atteindre un ellement qui n'existe pas"""
        self.assertIs(self.a[0], self.a._frms[self.a._film[0]])
        self.assertIs(self.a[len(self.a)-1], self.a._frms[self.a._film[len(self.a)-1]])
        self.assertRaises(IndexError, self.a.__getitem__, len(self.a))

    def test_iter(self):
        """test si la boucle for f in a fonctionne"""
        i = 0
        for f in self.a:
            i += 1
            self.assertIn(f, self.a._frms)
        self.assertEqual(len(self.a), i)

    def test_add_frm(self):
        """test si la longueur de a augmente d'un quand on ajoute une frm"""
        l1 = len(self.a)
        self.a.add_frm(len(self.a) - 1)
        l2 = len(self.a)
        self.assertEqual(l1 + 1, l2)

    def test_clone_frm(self):
        """test si le clonage cree bien deux clones
        test si une erreur est bien levée quand on veut cloner une frm qui n'existe pas"""
        self.a.clone_frm(0)
        self.assertIs(self.a[0], self.a[1])
        self.assertRaises(IndexError, self.a.clone_frm, len(self.a))

    def test_copy_frm(self):
        """test si le copiage ne cree pas deux clones
        test si une erreur est bien levée quand on tente de copier une frm qui n'existe pas"""
        self.a.copy_frm(0)
        self.assertIsNot(self.a[0], self.a[1])
        self.assertRaises(IndexError, self.a.copy_frm, len(self.a))

    def test_move_frm_to(self):
        """test si une frm deplacee est bien deplacee
        test si une erreur est bien levée quand on tente de deplacer une frm qui n'existe pas"""
        f = self.a[2]
        self.a.move_frm_to(2, 1)
        self.assertIs(self.a[1], f)
        self.assertRaises(IndexError, self.a.move_frm_to, len(self.a), 0)

    def test_del_frm(self):
        """test si la longueur de a diminue d'1 quand on supprime une frm
        test si une erreur est bien levée quand on tente de supprimer une frm qui n'existe pas"""
        l1 = len(self.a)
        self.a.del_frm(0)
        l2 = len(self.a)
        self.assertEqual(l1 - 1, l2)
        self.assertRaises(IndexError, self.a.del_frm, len(self.a))

    # CLASS FRM À FAIRE
