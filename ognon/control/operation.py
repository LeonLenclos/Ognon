import tkinter.simpledialog
import tkinter.filedialog


def operation(*args, **kwargs):
    """décorateur des opération

    args = on indique dabord les arguments dont la fonction a besoin
            - sous la forme d'une string renseigant le type d'information
            - ou d'un tuple renseigant le type d'information et une description
    kwargs = on indique ensuite des informations comme
            - name = le nom de l'opération
            - shortcut = le racourci souhaité"""
    def _operation(fun):
        # l'espace de nom de la fonction sera désormais occupé par un objet Operation
        return Operation(fun, *args, **kwargs)
    return _operation


class Operation():
    """operation est l'objet qui sert a gérer toute les fonctions proches de l'uttilisateur

    range toutes fonction dans un dictionnaire (Operation.dic)
    connait leur nom, leur racourci,
    range dans target quel argument "self" doit etre envoyé (à quelle objet appartient la fonction)
    demande les valeurs des arguments a l'uttilisateur si tous les arguments ne sont pas passés"""

    # dic contient la liste des fonctions opérations sous la forme
    # {
    #   module_name_1 = {
    #                      fonction_name_1 = fonction1 ;
    #                      fonction_name_2 = fonction2
    #                    } ;
    #   module_name_2 = {
    #                      fonction_name_1 = fonction1 ;
    #                      fonction_name_2 = fonction2 ;
    #                      fonction_name_3 = fonction3
    #                    }
    # }
    dic = {}

    def __init__(self, fun, *args, **kwargs):
        # Le nom et le shortcut sont passés par le décorateur
        self.name = "NONE"
        self.shortcut = ""
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'shortcut' in kwargs:
            self.shortcut = kwargs['shortcut']
        
        # un tuple contenant les arguments necessaire
        # (renseignés sous la forme d'une str ou d'un tuple de deux str ou d'un tuple de deux str + une var par deffaut)
        self.args_required = args
        # la fonction originale
        self._fun = fun
        # l'objet dont la fonction est une méthode
        self.target = None

        # on rempli Operation.dic
        if fun.__module__ not in Operation.dic:
            # on cree une nouvelle case module si elle n'est pas encore créé
            Operation.dic[fun.__module__] = {}
        # on met self dedans
        Operation.dic[fun.__module__][fun.__name__] = self

    def __get__(self, obj, objtype):
        """Support instance methods."""
        # J'avoue que je sais pas trop comment ça marche mais ça permet de pouvoir uttiliser call
        # meme alors que ces fonctions sont enfait des méthodes
        import functools
        return functools.partial(self.__call__, obj)

    def __call__(self, *args):
        """fun() est identique à fun.__call__()
        c'est donc cette methode qui est appelée lorsque j'appelle ma fonction"""
        # trois possibilités :

        # 1- tous les arguments necessaire sont la sauf self
        if len(args) == len(self.args_required):
            # on fait passer self.target puis tous les arguments
            return self._fun(self.target, *args)

        # 2- tous les arguments necessaire sont la
        elif len(args) == len(self.args_required) + 1:
            # on fait passer tous les arguments
            return self._fun(*args)

        # 3- rien n'est la (aie aie aie)
        else:
            #on cree une liste d'arguments commençant par self.target
            args_asked = list()
            args_asked.append(self.target)
            #on uttilise ce bol pour annuler l'appel de la fonction s'il y a un soucis
            function_callable = True
            for a in self.args_required:
                #pour chaque argument on demande à l'uttilisateur une valeur
                ask_for_result = self.ask_for(a)
                if ask_for_result is None:
                    # s'il clique sur annuler on annule
                    function_callable = False
                    break
                # on ajoute la valeur à la liste d'arguments
                args_asked.append(ask_for_result)
            #si tout s'est bien passé on passe tous les arguments
            if function_callable:
                return self._fun(*tuple(args_asked))

    def ask_for(self, infos):
        """cree une pop-up qui demande une valeur a l'uttilisateur
        infos peut etre une str renseigant le type voulu
        ou un tuple renseigant le type voulu et un message"""
        type_asked = ""
        message = ""
        deffaut = ""

        # si c'est un tuple on recupere dans des var separées le type et le message
        if isinstance(infos, tuple):
            type_asked = infos[0]
            message = infos[1]
            if len(infos) > 2:
                deffaut = infos[2]
        #sinon on recupere le type et on entre un message vide
        else:
            type_asked = infos
            message = ""

        # la c'est a améliorer... mais en gros en fonction du type c'est une fenetre differente qui s'ouvre
        if type_asked == "int":
            return tkinter.simpledialog.askinteger(self.name, message, initialvalue=deffaut)
        elif type_asked == "str":
            return tkinter.simpledialog.askstring(self.name, message, initialvalue=deffaut)
        elif type_asked == 'directory':
            return tkinter.filedialog.askdirectory() + "/"
        elif type_asked == 'save_file_png':
            return tkinter.filedialog.asksaveasfilename(defaultextension="png", initialfile="image")
        elif type_asked == 'save_file_ogn':
            return tkinter.filedialog.asksaveasfilename(defaultextension="ogn", initialfile="projet")
        elif type_asked == 'open_file_ogn':
            return tkinter.filedialog.askopenfilename()
