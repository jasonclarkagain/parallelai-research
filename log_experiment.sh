#!/bin/bash
echo "🔬 PARALLELAI RESEARCH EXPERIMENT LOGGER"
echo "========================================"

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <experiment_id> <query>"
    echo "Example: $0 pilot_001 'Analyze Mirai botnet'"
    exit 1
fi

EXPERIMENT_ID="$1"
QUERY="$2"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="experiments/experiment_${EXPERIMENT_ID}_${TIMESTAMP}.md"

echo "Starting experiment: $EXPERIMENT_ID"
echo "Query: $QUERY"
echo "Log: $LOG_FILE"

# Create the log file with metadata
cat > "$LOG_FILE" << METADATA
# ParallelAI Research Experiment
**Experiment ID:** $EXPERIMENT_ID  
**Researcher:** Jason Clark (ORCID: 0009-0005-3020-9694)  
**Date:** $(date -I)  
**Time:** $(date +%H:%M:%S)  
**GitHub Repo:** https://github.com/jasonclarkagain/parallelai  
**Tool Version:** $(git log --oneline -1 | cut -d' ' -f1)

## Research Query
\`\`\`
$QUERY
\`\`\`

## AI Responses
METADATA

echo "🔄 Querying AI providers..."
echo "\n## Multi-Provider Analysis" >> "$LOG_FILE"

# Run parallelai-simple and capture output
if [ -f "./parallelai-simple" ]; then
    ./parallelai-simple --all "$QUERY" 2>&1 | tee -a "$LOG_FILE"
else
    echo "❌ parallelai-simple not found in current directory"
    echo "Downloading from main repo..."
    cp ../parallelai/parallelai-simple . 2>/dev/null || \
    wget -q https://raw.githubusercontent.com/jasonclarkagain/parallelai/main/parallelai-simple
    chmod +x parallelai-simple
    ./parallelai-simple --all "$QUERY" 2>&1 | tee -a "$LOG_FILE"
fi

# Add conclusion section
cat >> "$LOG_FILE" << FOOTER

## Research Notes
- **Methodology:** Comparative multi-LLM analysis
- **Reproducibility:** Script available at https://github.com/jasonclarkagain/parallelai-research
- **Ethical Considerations:** Analysis for defensive security research only
- **Limitations:** AI models may have knowledge cutoff dates

## Next Research Steps
1. Validate findings with traditional analysis tools
2. Expand comparison to additional malware families
3. Submit findings for peer review

---
*This experiment was conducted using ParallelAI Research Edition*
*ORCID: 0009-0005-3020-9694 | GitHub: jasonclarkagain*
FOOTER

echo ""
echo "✅ Experiment logged to: $LOG_FILE"
echo "📊 To view: cat $LOG_FILE | head -50"
