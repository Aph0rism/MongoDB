# Atelier MongoDB – Projet NoSQL

Ce dépôt contient l’ensemble des travaux réalisés par **Dimitri Brancourt**, **Mattéo Vocanson** et **Flavio Nunes** dans le cadre de l’atelier sur MongoDB et les bases de données orientées documents.

## Objectifs pédagogiques

- Comprendre les principes d’une base de données orientée document
- Déployer MongoDB selon différents modes : standalone, replica set
- Intégrer MongoDB dans une application (ici, Python)
- Documenter toutes les étapes dans `docs/rapport.md`
- Versionner le projet et le partager en ligne

## Structure du projet

```plaintext
atelier-mongodb/
├── mongo/
│   ├── standalone/               # Déploiement MongoDB standalone
│   ├── replicaset/               # Déploiement MongoDB replica set
├── integration/
│   └── python/
│       └── tests/                # Scripts d’intégration et tests avec MongoDB
└── README.md                     # Ce fichier
```


## Technologies utilisées

- [MongoDB](https://www.mongodb.com/)
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/) et [pymongo](https://pymongo.readthedocs.io/en/stable/)
- [MongoDB Compass](https://www.mongodb.com/products/compass) / [mongosh](https://www.mongodb.com/docs/mongodb-shell/)


---

# Rapport de l’atelier MongoDB

## Partie 1 – MongoDB Standalone

### Méthode de déploiement

- Utilisation de Docker Compose pour lancer un conteneur MongoDB (image officielle).
- Authentification activée grâce aux variables d’environnement.
- Script d’initialisation pour créer la base `testdb`, l’utilisateur `testuser` et des premiers documents.

#### Commandes

```bash
cd mongo/standalone
docker-compose up -d
docker logs mongo-standalone
```

### Création de l’utilisateur

- Fait via le script `init-mongo.js` (voir fichier)
- Utilisateur : `testuser` / Mot de passe : `testpass`

### Connexion à la base

- Méthode CLI :  
  `mongosh "mongodb://testuser:testpass@localhost:27017/testdb?authSource=testdb"`
- Méthode GUI :  
  Avec MongoDB Compass, même URI ou en remplissant les champs manuellement.

### Manipulation de données

- Insertion :  
  `db.testcoll.insertOne({name: "Zoe", age: 22})`
- Requête :  
  `db.testcoll.find({age: {$gt: 20}})`
- Update :  
  `db.testcoll.updateOne({name: "Zoe"}, {$set: {age: 23}})`
- Suppression :  
  `db.testcoll.deleteOne({name: "Zoe"})`

Résultat :  
On retrouve les documents injectés au démarrage et ceux ajoutés en tests.

### Problèmes rencontrés

- Port déjà utilisé ➔ modifier le port dans le docker-compose.
- Authentification échouée ➔ bien vérifier la base d’authentification (`authSource`).

---

## Partie 2 – MongoDB Replica Set

### Configuration

- 3 instances MongoDB via Docker Compose (ports 27018–27020)
- Script d’initialisation du Replica Set : `init-replica.js`

#### Commandes

```bash
cd mongo/replicaset
docker-compose up -d
# Vérifier que tous les conteneurs sont up
docker ps

# Initialiser le Replica Set (si ce n'est pas automatique avec le script)
docker exec -it replicaset-mongo1-1 mongosh --eval "rs.initiate({
  _id: 'rs0',
  members: [
    { _id: 0, host: 'mongo1:27017' },
    { _id: 1, host: 'mongo2:27017' },
    { _id: 2, host: 'mongo3:27017' }
  ]
})"
# ou attendre que le script init-replica.js s’exécute automatiquement
```

### Vérification

```bash
docker exec -it mongo1 mongosh
> rs.status()
```
Vérifier PRIMARY et SECONDARY dans la sortie.

### Manipulation

- **Insertion sur PRIMARY :**
  - Se connecter sur mongo1 :
    ```bash
    docker exec -it mongo1 mongosh
    ```
  - Utiliser/tester la base et insérer un document :
    ```js
    use testdb
    db.testcoll.insertOne({ nom: "alice", age: 22 })
    db.testcoll.find()
    ```

- **Lecture sur SECONDARY :**
  utiliser une connexion directe avec `--readPreference` :
    ```bash
    docker exec -it mongo2 mongosh --host mongo2:27017
    db.getMongo().setReadPref("secondary")
    OU
    mongosh "mongodb://localhost:27019/testdb?replicaSet=rs0&readPreference=secondary"

    use testdb
    db.testcoll.find()
    ```

- **Exemple de connexion URI depuis l’extérieur (client graphique ou mongosh local) :**
    ```
    mongodb://testuser:testpass@localhost:27018,localhost:27019,localhost:27020/testdb?replicaSet=rs0&readPreference=secondary
    ```

### Explication des modes

- Write : toujours sur PRIMARY
- Read : possible sur SECONDARY avec readPreference

## Partie 3 – Intégration dans une application (Python)

### Dépendances

```
pymongo==4.8.0
dnspython==2.6.1
```

### Code de connexion

Voir : [`integration/python/main.py`](../integration/python/main.py)

Explication de l’URI :

- Connexion locale :  
  `mongodb://testuser:testpass@localhost:27017/testdb?authSource=testdb`
- Connexion réplicat :  
  `mongodb://testuser:testpass@localhost:27018,localhost:27019,localhost:27020/testdb?replicaSet=rs0`
- Possibilité d’ajouter TLS/SSL, options d’auth, etc.

### Actions réalisées

- Insertion, requête, update, suppression
- Affichage des outputs dans la console

### Résultats des tests

- Capture d’écran de la console (voir annexes)
- Test automatisé dans `tests/test_basic.py`

---

## Annexes et ressources

- [Documentation officielle MongoDB](https://www.mongodb.com/docs/)
- [Docker Hub MongoDB](https://hub.docker.com/_/mongo)
- [PyMongo](https://pymongo.readthedocs.io/)