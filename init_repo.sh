#!/bin/bash
# Script d'initialisation du repository Git pour SafeWay
# Réalisé par dylanecodeur

echo "🚀 Initialisation du repository Git pour SafeWay"
echo "================================================"

# Vérifier si Git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Initialiser Git si pas déjà fait
if [ ! -d .git ]; then
    echo "📦 Initialisation de Git..."
    git init
    echo "✅ Git initialisé"
else
    echo "✅ Git déjà initialisé"
fi

# Ajouter tous les fichiers
echo "📝 Ajout des fichiers..."
git add .

# Faire le commit initial
echo "💾 Création du commit initial..."
git commit -m "Initial commit: SafeWay v1.0.0

🚗 Système d'assistance à la conduite basé sur l'IA

Fonctionnalités:
- Détection de fatigue, distraction et comportements dangereux
- Utilisation de YOLOv11 et MediaPipe
- Alertes multi-modales (visuel, sonore, vocal)
- Système d'entraînement personnalisé
- Documentation complète FR/EN

Réalisé par dylanecodeur"

echo ""
echo "✅ Repository initialisé avec succès!"
echo ""
echo "📤 Prochaines étapes:"
echo "1. Créez un repository sur GitHub: https://github.com/new"
echo "2. Nom: SafeWay"
echo "3. Visibilité: Public"
echo "4. Exécutez:"
echo "   git remote add origin https://github.com/dylanecodeur/SafeWay.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "📖 Voir PUBLISH.md pour les instructions détaillées"

