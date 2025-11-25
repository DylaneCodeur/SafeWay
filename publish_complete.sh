#!/bin/bash
# Publication complète automatique sur GitHub
# Réalisé par dylanecodeur

REPO_NAME="SafeWay"
USERNAME="dylanecodeur"
DESCRIPTION="🚗 AI-powered driver assistance system for fatigue and distraction detection | Système d'assistance à la conduite basé sur l'IA"

echo "🚀 Publication complète de SafeWay sur GitHub"
echo "=============================================="
echo ""

# Vérifier si un token GitHub est disponible
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "📝 Pour publier automatiquement, vous avez besoin d'un token GitHub."
    echo ""
    echo "Option 1: Créer un token (recommandé)"
    echo "   1. Allez sur: https://github.com/settings/tokens"
    echo "   2. Generate new token (classic)"
    echo "   3. Cochez 'repo' (accès complet aux repositories)"
    echo "   4. Copiez le token"
    echo "   5. Exécutez: export GITHUB_TOKEN=votre_token"
    echo "   6. Relancez ce script"
    echo ""
    echo "Option 2: Publication manuelle (plus simple)"
    echo "   Suivez les instructions dans COMMANDES_PUBLICATION.txt"
    echo ""
    read -p "Voulez-vous continuer avec la publication manuelle? (o/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[OoYy]$ ]]; then
        cat COMMANDES_PUBLICATION.txt
        exit 0
    else
        exit 1
    fi
fi

# Créer le repository via l'API GitHub
echo "📦 Création du repository sur GitHub via API..."
echo ""

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/user/repos \
    -d "{
        \"name\": \"$REPO_NAME\",
        \"description\": \"$DESCRIPTION\",
        \"private\": false,
        \"auto_init\": false
    }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Repository créé avec succès!"
    echo ""
    
    # Ajouter le remote et pousser
    echo "📡 Configuration du remote..."
    git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git" 2>/dev/null || \
    git remote set-url origin "https://github.com/${USERNAME}/${REPO_NAME}.git"
    
    echo "📤 Publication du code..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ ✅ ✅ PUBLICATION COMPLÈTE RÉUSSIE! ✅ ✅ ✅"
        echo ""
        echo "🌐 Repository disponible sur:"
        echo "   https://github.com/${USERNAME}/${REPO_NAME}"
        echo ""
        echo "📝 Prochaines étapes:"
        echo "   1. Ajoutez les topics sur GitHub"
        echo "   2. Créez une release v1.0.0 (optionnel)"
        echo ""
    else
        echo "❌ Erreur lors du push. Vérifiez vos permissions."
    fi
elif [ "$HTTP_CODE" = "422" ]; then
    echo "⚠️  Le repository existe déjà sur GitHub"
    echo ""
    echo "📡 Connexion au repository existant..."
    git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git" 2>/dev/null || \
    git remote set-url origin "https://github.com/${USERNAME}/${REPO_NAME}.git"
    
    echo "📤 Publication du code..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ ✅ ✅ CODE PUBLIÉ AVEC SUCCÈS! ✅ ✅ ✅"
        echo ""
        echo "🌐 Repository: https://github.com/${USERNAME}/${REPO_NAME}"
    fi
else
    echo "❌ Erreur lors de la création du repository"
    echo "Code HTTP: $HTTP_CODE"
    echo "Réponse: $BODY"
    echo ""
    echo "💡 Utilisez la méthode manuelle (voir COMMANDES_PUBLICATION.txt)"
fi

