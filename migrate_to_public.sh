#!/bin/bash
echo "📦 Migrating Research Content to Public Repository"
echo "================================================"

# Ensure we're in research repo
cd ~/parallelai-research

echo ""
echo "1. Copying research documents..."
cp ~/parallelai/RESEARCH_PORTFOLIO.md .
cp ~/parallelai/test_orcid_access.sh .

echo ""
echo "2. Creating public documentation..."
cat > TOOL_OVERVIEW.md << 'TOOL_EOF'
# ParallelAI Tool Overview
[Content from above]
TOOL_EOF

echo ""
echo "3. Checking docs/ directory..."
if [ -d "~/parallelai/docs" ]; then
    echo "Found docs/. Checking contents..."
    ls ~/parallelai/docs/
    echo "Review these files - move research papers, keep manuals private"
fi

echo ""
echo "4. Reviewing requirements.txt for dependencies..."
if [ -f "~/parallelai/requirements.txt" ]; then
    echo "Dependencies found. These can typically be public."
    cp ~/parallelai/requirements.txt .
fi

echo ""
echo "✅ Migration ready. Files to add to research repo:"
git status --porcelain

echo ""
echo "📋 NEXT STEPS:"
echo "1. Review the files above"
echo "2. Add with: git add ."
echo "3. Commit: git commit -m 'Add research migration'"
echo "4. Push: git push origin main"
echo "5. Then make main repo private in GitHub settings"
