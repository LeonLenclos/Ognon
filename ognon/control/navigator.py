"""Provide a Reader class to navigate into Animation"""
from threading import Timer

class Navigator():
    """Allow to navigate into one Animation."""
    def __init__(self, ogn_project):
        self.ogn_project = ogn_project
        # a timers dict for Timer objects. Keys are cursors
        self.timers = {}

    # Déplacer ? Suprimer ??? :
    #
    # def current_onion_frms(self):
    #     if not self.is_playing:
    #         prev = self.constrain_film_index(self.cursor - 1)
    #         next = self.constrain_film_index(self.cursor + 1)
    #         if prev == next == self.cursor:
    #             return []
    #         elif prev == next:
    #             return [self.anim[prev]]
    #         else:
    #             return [self.anim[prev], self.anim[next]]

    def run(self, cursor):
        if cursor.playing:
            self.next_frm(cursor)

    def auto_run(self, cursor):
        self.run(cursor)
        if cursor.playing:
            fps = self.ogn_project.get_config('play', 'fps', int)
            self.timers[cursor] = Timer(1/fps, self.auto_run, [cursor])
            self.timers[cursor].start()
        else:
            self.timers[cursor] = None

    def play(self, cursor):
        """Permet de lire ou de stopper l'anim"""
        cursor.playing = not cursor.playing
        print(self.ogn_project.get_config('play', 'auto_run', bool))

        if cursor.playing and self.ogn_project.get_config('play', 'auto_run', bool):
            self.auto_run(cursor)

    def prev_frm(self, cursor):
        """Permet d'acceder à la frm précédente"""
        cursor.set_frm_idx_rel(-1)

    def next_frm(self, cursor):
        """Permet d'acceder à la frm suivante"""
        cursor.set_frm_idx_rel(+1)

    def first_frm(self, cursor):
        """Permet d'acceder à la frm suivante"""
        cursor.set_frm_idx(0)

    def last_frm(self, cursor):
        """Permet d'acceder à la frm précédente"""
        cursor.set_frm_idx(-1)

    def go_to_frm(self, cursor, i):
        """Permet d'acceder à une frm i"""
        cursor.set_frm_idx(i)
