import unittest
import importlib.util
import os


def load_trello_module():
    path = os.path.join(os.path.dirname(__file__), "Trello .py")
    spec = importlib.util.spec_from_file_location("trello_mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TrelloUnitTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_trello_module()
        self.app = self.mod.Trello()
        # fresh board and user for tests
        self.board = self.app.createBoard("work")
        self.user = self.app.userService.addUser("Gaurav", "gaurav@workat.tech")

    def test_create_board_and_url(self):
        self.assertIsNotNone(self.board.id)
        self.assertEqual(self.board.url, f"/board/{self.board.id}")
        self.assertEqual(self.board.privacy, self.mod.BoardPrivacy.PUBLIC)

    def test_add_user_and_member(self):
        added = self.app.addUserToBoard(self.board.id, self.user.userId)
        self.assertTrue(added)
        b = self.mod.boardDao.findById(self.board.id)
        self.assertIn(self.user.userId, b.members)
        # now remove member
        removed = self.app.removeUserFromBoard(self.board.id, self.user.userId)
        self.assertTrue(removed)
        b2 = self.mod.boardDao.findById(self.board.id)
        self.assertFalse(b2.members.get(self.user.userId))

    def test_create_list_and_card_and_show(self):
        lst = self.app.createList(self.board.id, "Mock Interviews")
        self.assertIsNotNone(lst.id)
        self.assertEqual(lst.name, "Mock Interviews")

        # change list name
        ok_name = self.app.changeListName(lst.id, "Mock Interviews - Applied")
        self.assertTrue(ok_name)
        lst2 = self.mod.listDao.findById(lst.id)
        self.assertEqual(lst2.name, "Mock Interviews - Applied")

        # create a card in the list and expect returned card
        card = self.app.createCard(lst.id, "abcd@gmail.com")
        self.assertIsNotNone(card.id)
        # verify list contains card
        list_info = self.app.showList(lst.id)
        self.assertIn("cards", list_info)
        self.assertTrue(len(list_info["cards"]) >= 1)
        card_id = list_info["cards"][0]["id"]
        card_info = self.app.showCard(card_id)
        self.assertEqual(card_info["name"], "abcd@gmail.com")

        # change card name and description
        self.assertTrue(self.app.setCardName(card_id, "abcde@gmail.com"))
        self.assertTrue(self.app.setCardDescription(card_id, "At 7PM"))
        card_info2 = self.app.showCard(card_id)
        self.assertEqual(card_info2["name"], "abcde@gmail.com")
        self.assertEqual(card_info2["description"], "At 7PM")

        # assign and unassign
        self.assertTrue(self.app.assignCard(card_id, self.user.userId))
        card_info3 = self.app.showCard(card_id)
        self.assertTrue(len(card_info3["assigned Users"]) >= 1)
        self.assertTrue(self.app.unassignCard(card_id, self.user.userId))

    def test_delete_board_cascades(self):
        # create a list and a card to ensure cascade delete
        self.app.createList(self.board.id, "Tmp")
        b = self.mod.boardDao.findById(self.board.id)
        list_ids = [lid for lid, present in b.lists.items() if present]
        lst_id = list_ids[0]
        self.app.createCard(lst_id, "to-delete@example.com")
        # now delete board
        ok = self.app.deleteBoard(self.board.id)
        self.assertTrue(ok)
        # boardDao.findById returns False when missing (decorator behavior)
        self.assertFalse(self.mod.boardDao.findById(self.board.id))

    def test_move_card_between_lists(self):
        l1 = self.app.createList(self.board.id, "List A")
        l2 = self.app.createList(self.board.id, "List B")
        card = self.app.createCard(l1.id, "move-me@example.com")
        # move card
        moved = self.app.moveCard(card.id, l2.id)
        self.assertTrue(moved)
        # verify card now in l2 and not active in l1
        l1r = self.mod.listDao.findById(l1.id)
        l2r = self.mod.listDao.findById(l2.id)
        self.assertFalse(l1r.cards.get(card.id))
        self.assertTrue(l2r.cards.get(card.id))


if __name__ == "__main__":
    unittest.main()
