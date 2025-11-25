#!/bin/bash
# Script de publication automatique sur GitHub
# Réalisé par dylanecodeur

echo "🚀 Publication de SafeWay sur GitHub"
echo "===================================="

REPO_NAME="SafeWay"
USERNAME="dylanecodeur"
REPO_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

# Vérifier si le remote existe déjà
if git remote get-url origin &>/dev/null; then
    echo "✅ Remote 'origin' existe déjà"
    CURRENT_URL=$(git remote get-url origin)
    echo "   URL actuelle: $CURRENT_URL"
    
    read -p "Voulez-vous utiliser cette URL? (o/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[OoYy]$ ]]; then
        git remote remove origin
        git remote add origin "$REPO_URL"
        echo "✅ Remote mis à jour vers: $REPO_URL"
    fi
else
    echo "📡 Ajout du remote GitHub..."
    git remote add origin "$REPO_URL"
    echo "✅ Remote ajouté: $REPO_URL"
fi

# Vérifier si le repository existe sur GitHub
echo ""
echo "📋 Instructions pour créer le repository sur GitHub:"
echo "=================================================="
echo ""
echo "1. Allez sur: https://github.com/new"
echo "2. Repository name: SafeWay"
echo "3. Description: 🚗 AI-powered driver assistance system for fatigue and distraction detection | Système d'assistance à la conduite basé sur l'IA"
echo "4. Visibilité: ✅ Public"
echo "5. NE COCHEZ PAS 'Add a README file' (on en a déjà un)"
echo "6. NE COCHEZ PAS 'Add .gitignore' (on en a déjà un)"
echo "7. Cliquez sur 'Create repository'"
echo ""
read -p "Appuyez sur Entrée une fois le repository créé sur GitHub... " -r
echo ""

# Pousser vers GitHub
echo "📤 Publication sur GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ ✅ ✅ PUBLICATION RÉUSSIE! ✅ ✅ ✅"
    echo ""
    echo "🌐 Votre projet est maintenant disponible sur:"
    echo "   https://github.com/${USERNAME}/${REPO_NAME}"
    echo ""
    echo "📝 Prochaines étapes:"
    echo "   1. Ajoutez des topics sur GitHub: ai, driver-assistance, computer-vision, yolo, mediapipe"
    echo "   2. Créez une release v1.0.0 (optionnel)"
    echo "   3. Partagez le projet! 🚀"
    echo ""
else
    echo ""
    echo "❌ Erreur lors de la publication"
    echo ""
    echo "Vérifiez que:"
    echo "  1. Le repository existe sur GitHub"
    echo "  2. Vous avez les permissions d'écriture"
    echo "  3. Vous êtes authentifié (git config --global user.name)"
    echo ""
    echo "Ou publiez manuellement:"
    echo "  git push -u origin main"
    echo ""
fi

