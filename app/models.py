from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from setup import bcrypt,db, validates


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    powers = db.relationship('Power', secondary='hero_powers', back_populates='heroes')
    serialize_rules = ('-powers.heroes')


# add any models you may need. 
class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    heroes = db.relationship('Hero', secondary='hero_powers', back_populates='powers')

    @validates('description')
    def validate_description(self, key, desc):
        if desc == None or len(desc) <= 20:
            raise ValueError("Description must be at least 20 characters long")
        return desc
    
    serialize_rules = ('-heroes.powers')

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('strength')
    def validate_self(self, key, strength):
        if strength != 'Strong' and strength != 'Weak' and strength != 'Average':
            raise ValueError("Strength can only be described as Strong, Weak or Average")
        return strength
