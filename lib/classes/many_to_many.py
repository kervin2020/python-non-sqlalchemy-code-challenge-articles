class Article:
    all = []
    
    def __init__(self, author, magazine, title):
        # Validation des types
        if not isinstance(author, Author):
            raise Exception("Author must be of type Author")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be of type Magazine")
        if not isinstance(title, str):
            raise Exception("Title must be of type str")
        if not (5 <= len(title) <= 50):
            raise Exception("Title must be between 5 and 50 characters, inclusive")
        
        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)
        
        # Ajouter l'article aux listes de l'auteur et du magazine
        author._articles.append(self)
        magazine._articles.append(self)
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Author must be of type Author")
        # Retirer de l'ancien auteur
        if hasattr(self, '_author') and self._author:
            self._author._articles.remove(self)
        # Ajouter au nouvel auteur
        self._author = value
        value._articles.append(self)
    
    @property
    def magazine(self):
        return self._magazine
    
    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be of type Magazine")
        # Retirer de l'ancien magazine
        if hasattr(self, '_magazine') and self._magazine:
            self._magazine._articles.remove(self)
        # Ajouter au nouveau magazine
        self._magazine = value
        value._articles.append(self)
    
    @property
    def title(self):
        return self._title
    
    # Le titre ne peut pas être modifié après l'initialisation
    def __setattr__(self, name, value):
        if name == 'title' and hasattr(self, '_title'):
            # Ignorer silencieusement les tentatives de modification
            return
        super().__setattr__(name, value)
        
class Author:
    all_authors = []
    
    def __init__(self, name):
        if not isinstance(name, str):
            raise Exception("Name must be of type str")
        if len(name) <= 0:
            raise Exception("Name must be longer than 0 characters")
        
        self._name = name
        self._articles = []
        Author.all_authors.append(self)
    
    @property
    def name(self):
        return self._name
    
    # Le nom ne peut pas être modifié après l'initialisation
    def __setattr__(self, name, value):
        if name == 'name' and hasattr(self, '_name'):
            # Ignorer silencieusement les tentatives de modification
            return
        super().__setattr__(name, value)

    def articles(self):
        return self._articles.copy()

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self._articles:
            return None
        return list(set(article.magazine.category for article in self._articles))

class AllMagazinesDescriptor:
    def __get__(self, obj, objtype=None):
        return objtype.all_magazines
    
    def __set__(self, obj, value):
        objtype = type(obj) if obj is not None else Magazine
        objtype.all_magazines = value

class Magazine:
    all_magazines = []
    all = AllMagazinesDescriptor()
    
    def __init__(self, name, category):
        if not isinstance(name, str):
            raise Exception("Name must be of type str")
        if not (2 <= len(name) <= 16):
            raise Exception("Name must be between 2 and 16 characters, inclusive")
        if not isinstance(category, str):
            raise Exception("Category must be of type str")
        if len(category) <= 0:
            raise Exception("Category must be longer than 0 characters")
        
        self._name = name
        self._category = category
        self._articles = []
        Magazine.all.append(self)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            return  # Ignorer silencieusement les types invalides
        if not (2 <= len(value) <= 16):
            return  # Ignorer silencieusement les longueurs invalides
        self._name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            return  # Ignorer silencieusement les types invalides
        if len(value) <= 0:
            return  # Ignorer silencieusement les longueurs invalides
        self._category = value

    def articles(self):
        return self._articles.copy()

    def contributors(self):
        return list(set(article.author for article in self._articles))

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def contributing_authors(self):
        author_counts = {}
        for article in self._articles:
            author = article.author
            author_counts[author] = author_counts.get(author, 0) + 1
        
        contributing = [author for author, count in author_counts.items() if count > 2]
        return contributing if contributing else None
    
    @classmethod
    def top_publisher(cls):
        magazines = cls.all  # Utiliser all au lieu de all_magazines
        if not magazines:
            return None
        
        # Vérifier s'il y a des articles
        magazines_with_articles = [mag for mag in magazines if mag.articles()]
        if not magazines_with_articles:
            return None
        
        return max(magazines_with_articles, key=lambda mag: len(mag.articles()))