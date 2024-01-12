# Rapport de projet

## liens utiles

- code source: [github.com/TheGeekMax/projet-oueb](https://github.com/TheGeekMax/projet-oueb)

- demo en ligne: [projet-oueb.fr](https://projet-oueb.fr)

## choix techniques


- Hébergement du projet sur github
    - permet de pouvoir travailler en parallèle sur le projet sans avoir de conflit

- Hébergement de la version web sur AlwaysData
    - configuration des DNS avec cloudflare (permettant de lier [projet-oueb.fr](https://projet-oueb.fr) au site)
    - assurant le fonctionnement du site 24h/24

- Authentification intégrée à django
    - chiffrement des mots de passe
    - session ID (pour rester connecté entre les pages du site)

- Système de requêtes à intervalle de temps régulier
    - éviter de rafraîchir la page pour afficher les nouveaux messages et nouveaux salons

- système d'administration en 2 parties :
    - une générale qui s'applique à chaque utilisateur (ex: créer un salon, supprimer un salon, ect.)
    - spécifique à chaque salon et à chaque utilisateur (ex: écrire dans le salon, supprimer des messages, ect.)

- Gestion des emojis
    - remplacer les emojis textuels en emoticône (ex: :-) en son équivalent lors de l'envoi du message)

- Possibilité de créer un administrateur avec la commande suivante : 
    ```bash
    python3 manage.py createadminuser <username>
    ```

    - afin d'éviter de modifier la base donnée directement    

- magnifique page 404 pour informer gentiment les internautes qu'ils ne sont pas sur la bonne page

## difficultés rencontrées

- Implémentation des permisions
    - faire les conditions dans les différentes vues afin de rediriger l'utilisateur/l'interdire de faire certaines actions
    - pouvoir modifier les permissions de manière intuitive avec un formulaire explicite
    - la création de la commande "createadminuser" permettant l'ajout de nouveaux admins

- compréhension et adaptation des fonctions natives de django
    - le système d'authentification mis en place avec la modification des différentes valeurs (mot de passe, ajout de valeurs supplémentaire comme la description)


- les premiers merges via github
    - la compatibilité des différentes parties, créant des conflit d'un point de vue du code

- la mise en production du site
    - problèmes avec les différentes sécurité mises en place par django, empêchant la connexion et l'envoi de formulaire de fonctionner normalement
    - Alwaysdata qui fait parfois des caprices sans aucune raison valable

- le css et la mise en page du site 
    - avoir une mise en page correcte correspondant a un site de chat en ligne
    - avoir une erreur 404 digne de ce nom ( [la page erreur 404](https://projet-oueb.fr/404) )
    - ergonomie simplifiée pour l'utilisateur (prêt pour les handicapés)
    - thème jour/nuit, permettant de s'adapter a tout les choix (même on sait que tout le monde choisira le thème sombre)