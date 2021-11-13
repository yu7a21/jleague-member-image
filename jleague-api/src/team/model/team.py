from config.db_config import db

class Team(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    short_name = db.Column(db.String(50), nullable=False)
    league = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)

    def convert_color_str_to_tuple(self) -> tuple:
        """
        カンマ区切りになっているRGBを(r,g,b)のタプルで返す

        :return: RGB
        :rtype: tuple
        """
        #カンマでばらしてintに変換、一旦listにする
        color_list = [int(color) for color in self.color.split(",")]
        return (color_list[0], color_list[1], color_list[2])