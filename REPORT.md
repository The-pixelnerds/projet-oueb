# Rapport de projet

## liens utiles

- code source: [github.com/TheGeekMax/projet-oueb](https://github.com/TheGeekMax/projet-oueb)

- demo en ligne: [projet-oueb.fr](https://projet-oueb.fr)

## choix techniques


- Hébergement du projet sur github
    - permet de pouvoir travailler en parallèle sur le projet sans avoir de conflit

- Authentification intégrée à django
    - chiffrement des mots de passe
    - session ID (pour rester connecté entre les pages du site)

- Système de requêtes à intervalle de temps régulier
    - éviter de rafraîchir la page pour afficher les nouveaux messages

- système d'administration en 2 parties 
    - une générale qui s'applique à chaque utilisateur (ex: créer un salon, supprimer un salon, ect.)
    - spécifique à chaque salon et à chaque utilisateur (ex: écrire dans le salon, supprimer des messages, ect.)

- Gestion des emojis
    - remplacer les emojis textuels en emoticône (ex: :-\) en son equivalent lors de l'envoi du message)

- Possibilité de créer un administrateur avec la commande suivante : 
    ```bash
    python3 manage.py createadminuser <username>
    ```

    - afin d'éviter de modifier la base donnée directement    

- magnifique page 404 pour informer gentillement les internautes qu'ils ne sont pas sur la bonne page

## difficultés rencontrées

// TODO