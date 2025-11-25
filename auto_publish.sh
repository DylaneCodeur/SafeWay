#!/bin/bash
# Script de publication automatique complète sur GitHub
# Réalisé par dylanecodeur

REPO_NAME="SafeWay"
USERNAME="dylanecodeur"
DESCRIPTION="🚗 AI-powered driver assistance system for fatigue and distraction detection | Système d'assistance à la conduite basé sur l'IA"

echo "🚀 Publication automatique de SafeWay sur GitHub"
echo "================================================"
echo ""

# Vérifier si GitHub CLI est installé
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI détecté"
    echo ""
    echo "🔐 Vérification de l'authentification..."
    if gh auth status &> /dev/null; then
        echo "✅ Authentifié sur GitHub"
        echo ""
        echo "📦 Création du repository sur GitHub..."
        gh repo create "$REPO_NAME" \
            --public \
            --description "$DESCRIPTION" \
            --source=. \
            --remote=origin \
            --push
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ ✅ ✅ PUBLICATION RÉUSSIE! ✅ ✅ ✅"
            echo ""
            echo "🌐 Repository créé et publié:"
            echo "   https://github.com/${USERNAME}/${REPO_NAME}"
            echo ""
            echo "📝 Prochaines étapes:"
            echo "   1. Ajoutez des topics sur GitHub"
            echo "   2. Créez une release v1.0.0 (optionnel)"
            exit 0
        fi
    else
        echo "⚠️  Non authentifié. Authentifiez-vous avec: gh auth login"
    fi
fi

# Fallback: Instructions manuelles
echo ""
echo "📋 Instructions pour publication manuelle:"
echo "=========================================="
echo ""
echo "1️⃣  Créer le repository sur GitHub:"
echo "   👉 https://github.com/new"
echo "   - Nom: $REPO_NAME"
echo "   - Description: $DESCRIPTION"
echo "   - Visibilité: Public ✅"
echo "   - Ne cochez RIEN d'autre"
echo ""
echo "2️⃣  Une fois créé, exécutez ces commandes:"
echo ""
echo "   git remote add origin https://github.com/${USERNAME}/${REPO_NAME}.git"
echo "   git push -u origin main"
echo ""
echo "Ou utilisez le script interactif:"
echo "   ./publish_to_github.sh"
echo ""

