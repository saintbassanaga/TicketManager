# Guide de Collaboration Git - TicketManager

Pour que nous puissions travailler ensemble sans casser le code des autres, voici les règles à suivre :

## 1. Structure des Branches
*   **main** : C'est la branche de production. Le code doit toujours y être fonctionnel. On ne travaille JAMAIS directement sur `main`.
*   **Branches personnelles** : Chaque collaborateur doit créer une branche à son nom pour travailler sur ses tâches.
    *   Format : `nom-du-collaborateur/nom-de-la-tache`
    *   Exemples : `ngah/auth-api`, `dave/orders-logic`, `saintbassanaga/core-models`

## 2. Cycle de Travail Quotidien
Avant de commencer à travailler :
```sh
git checkout main
git pull origin main
```

Pour commencer une nouvelle tâche :
```sh
git checkout -b votre-nom/nom-de-la-tache
```

## 3. Commits et Push
Faites des commits réguliers avec des messages clairs (en français ou anglais, mais restez cohérents).
```sh
git add .
git commit -m "feat: ajout de la logique de validation des tickets"
git push origin votre-nom/nom-de-la-tache
```

## 4. Pull Requests (PR) et Merge
*   Une fois votre tâche terminée et poussée sur GitHub, ouvrez une **Pull Request** vers la branche `main`.
*   **Règle d'or** : Au moins une autre personne doit valider la PR avant le merge.
*   Si vous avez des conflits, réglez-les sur votre branche locale en fusionnant `main` dedans avant de merger la PR.

## 5. Cas Particulier : Django Migrations
*   Si vous modifiez `models.py`, vous **devez** inclure les fichiers générés dans `ticketmanager/migrations/` dans votre commit.
*   Si vous récupérez le code d'un collègue, faites toujours :
    ```sh
    python manage.py migrate
    ```

## 6. Communication
*   Signalez sur le groupe quand vous ouvrez une PR.
*   Si vous touchez à un fichier sur lequel quelqu'un d'autre travaille, prévenez-le !
