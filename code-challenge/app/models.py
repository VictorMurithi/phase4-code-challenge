from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationship: A hero can have multiple powers
    hero_powers = db.relationship('HeroPower', back_populates='hero')

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # Relationship: A power can be associated with multiple heroes
    power_heroes = db.relationship('HeroPower', back_populates='power')

    # Validation: description must be present and at least 20 characters long
    @validates('description')
    def validate_description(self, key, description):
        if len(description.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return description

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


    # Relationship: A hero power belongs to one hero
    hero = db.relationship('Hero', back_populates='hero_powers')

    # Relationship: A hero power belongs to one power
    power = db.relationship('Power', back_populates='power_heroes')

    # Validation: strength must be one of 'Strong', 'Weak', 'Average'
    @validates('strength')
    def validate_strength(self, key, strength):
        allowed_strengths = ['Strong', 'Weak', 'Average']
        if strength not in allowed_strengths:
            raise ValueError("Strength must be one of 'Strong', 'Weak', 'Average'.")
        return strength
